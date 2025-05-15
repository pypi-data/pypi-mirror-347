from ipyleaflet import Map, DrawControl, WidgetControl, TileLayer, WMSLayer
from ipywidgets import (
    Dropdown,
    Button,
    Output,
    VBox,
    FileUpload,
    Label,
    ToggleButtons,
    HBox,
)
import geopandas as gpd
import zipfile
import io
import os
import tempfile
import json
import pandas as pd
import matplotlib.pyplot as plt
from .analysis import clip_raster_to_geometry, calculate_landcover_stats, compare_years
from .registry import LANDCOVER_DB


def build_gui(map_obj: Map, raster_options: dict = {}, pixel_size=30):
    output = Output()
    chart_output = Output()
    draw_roi = {}
    uploaded_roi = {}
    last_stats = None

    # ==== TILE/WMS DATASET SELECTION ====
    dataset_dropdown = Dropdown(
        options=list(LANDCOVER_DB.keys()), description="Dataset:"
    )

    year_dropdown = Dropdown(description="Year:")
    add_layer_btn = Button(description="Add Layer to Map", button_style="primary")

    def update_years(*args):
        selected = dataset_dropdown.value
        dataset = LANDCOVER_DB[selected]
        if dataset["source"] == "tile":
            year_dropdown.options = list(dataset["years"].keys())
        elif dataset["source"] == "wms":
            year_dropdown.options = list(dataset["layers"].keys())

    dataset_dropdown.observe(update_years, names="value")
    update_years()

    @add_layer_btn.on_click
    def add_raster_layer(b):
        dataset = dataset_dropdown.value
        year = year_dropdown.value
        info = LANDCOVER_DB[dataset]

        # Remove previous land cover layers
        for layer in list(map_obj.layers):
            if isinstance(layer, (TileLayer, WMSLayer)) and layer.name.startswith(
                "LandCover"
            ):
                map_obj.remove_layer(layer)

        if info["source"] == "tile":
            url = info["years"][year]["url"]
            label = info["years"][year]["label"]
            tile_layer = TileLayer(url=url, name=f"LandCover: {label}", opacity=0.7)
            map_obj.add_layer(tile_layer)

        elif info["source"] == "wms":
            wms_url = info["url"]
            layer_id = str(info["layers"][year])  # Ensure string format
            wms_layer = WMSLayer(
                url=wms_url,
                layers=layer_id,
                format="image/png",
                transparent=True,
                attribution="Esri",
                name=f"LandCover: {dataset} {year}",
                opacity=0.7,
            )
            map_obj.add_layer(wms_layer)

    # ==== ANALYSIS MODE ====
    mode_selector = ToggleButtons(
        options=["Single Year", "Compare Two Years"], description="Mode:"
    )

    raster_dropdown_1 = Dropdown(options=raster_options, description="Raster 1:")
    raster_dropdown_2 = Dropdown(options=raster_options, description="Raster 2:")
    raster_dropdown_2.layout.display = "none"

    def handle_mode_change(change):
        if change["new"] == "Compare Two Years":
            raster_dropdown_2.layout.display = ""
        else:
            raster_dropdown_2.layout.display = "none"

    mode_selector.observe(handle_mode_change, names="value")

    # ==== ROI INPUTS ====
    upload_label = Label("Or upload ROI:")
    upload_widget = FileUpload(accept=".geojson,.zip", multiple=False)
    draw_control = DrawControl(polyline={}, circlemarker={})

    @draw_control.on_draw
    def handle_draw(target, action, geo_json):
        nonlocal draw_roi
        draw_roi = geo_json
        output.clear_output()
        with output:
            print("ROI updated from drawing.")

    def handle_upload(change):
        nonlocal uploaded_roi
        uploaded_file = next(iter(upload_widget.value.values()))
        content = uploaded_file["content"]
        name = uploaded_file["metadata"]["name"]

        try:
            if name.endswith(".geojson"):
                gdf = gpd.read_file(io.BytesIO(content))
            elif name.endswith(".zip"):
                with tempfile.TemporaryDirectory() as tmpdir:
                    zip_path = os.path.join(tmpdir, name)
                    with open(zip_path, "wb") as f:
                        f.write(content)
                    with zipfile.ZipFile(zip_path, "r") as z:
                        z.extractall(tmpdir)
                    shp_files = [
                        os.path.join(tmpdir, f)
                        for f in os.listdir(tmpdir)
                        if f.endswith(".shp")
                    ]
                    if not shp_files:
                        raise ValueError("No .shp file found in ZIP.")
                    gdf = gpd.read_file(shp_files[0])
            else:
                raise ValueError("Unsupported file format.")
            uploaded_roi = json.loads(gdf.to_json())["features"][0]
            output.clear_output()
            with output:
                print(f"ROI uploaded from: {name}")
        except Exception as e:
            output.clear_output()
            with output:
                print(f"Upload error: {e}")

    upload_widget.observe(handle_upload, names="value")

    # ==== ANALYSIS ====
    calculate_btn = Button(description="Calculate", button_style="success")
    export_btn = Button(description="Export CSV", button_style="info")
    chart_btn = Button(description="Show Chart", button_style="warning")

    @calculate_btn.on_click
    def calculate_handler(b):
        nonlocal last_stats
        roi_source = uploaded_roi if uploaded_roi else draw_roi
        if not roi_source:
            with output:
                output.clear_output()
                print("Please draw or upload an ROI first.")
            return

        gdf = gpd.GeoDataFrame.from_features([roi_source], crs="EPSG:4326")
        try:
            if mode_selector.value == "Single Year":
                raster_path = raster_dropdown_1.value
                arr, _ = clip_raster_to_geometry(raster_path, gdf)
                stats = calculate_landcover_stats(arr, pixel_size=pixel_size)
                output.clear_output()
                with output:
                    print("Land Cover Statistics:")
                    print(stats)
                last_stats = stats

            elif mode_selector.value == "Compare Two Years":
                raster1 = raster_dropdown_1.value
                raster2 = raster_dropdown_2.value
                arr1, _ = clip_raster_to_geometry(raster1, gdf)
                arr2, _ = clip_raster_to_geometry(raster2, gdf)
                stats1 = calculate_landcover_stats(arr1, pixel_size=pixel_size)
                stats2 = calculate_landcover_stats(arr2, pixel_size=pixel_size)
                change = compare_years(stats1, stats2)
                output.clear_output()
                with output:
                    print("Land Cover Change Statistics:")
                    print(change)
                last_stats = change

        except Exception as e:
            output.clear_output()
            with output:
                print(f"Error: {e}")

    @export_btn.on_click
    def export_csv_handler(b):
        if last_stats is not None:
            last_stats.to_csv("landcover_stats.csv", index=False)
            with output:
                print("CSV exported to: landcover_stats.csv")
        else:
            with output:
                print("Run analysis before exporting.")

    @chart_btn.on_click
    def chart_handler(b):
        if last_stats is not None:
            chart_output.clear_output()
            with chart_output:
                fig, ax = plt.subplots(figsize=(6, 4))
                if "percent" in last_stats.columns:
                    labels = last_stats.get("label", last_stats["class_value"])
                    ax.pie(last_stats["percent"], labels=labels, autopct="%1.1f%%")
                    ax.set_title("Land Cover Distribution")
                elif "percent_change" in last_stats.columns:
                    labels = last_stats.get("label", last_stats["class_value"])
                    ax.bar(labels, last_stats["percent_change"])
                    ax.set_title("Percent Change in Land Cover")
                    plt.xticks(rotation=45, ha="right")
                    plt.tight_layout()
                plt.show()
        else:
            with output:
                print("Run analysis before charting.")

    # ==== UI LAYOUT ====
    ui_elements = VBox(
        [
            dataset_dropdown,
            year_dropdown,
            add_layer_btn,
            mode_selector,
            raster_dropdown_1,
            raster_dropdown_2,
            upload_label,
            upload_widget,
            HBox([calculate_btn, export_btn, chart_btn]),
        ]
    )

    map_obj.add_control(draw_control)
    map_obj.add_control(WidgetControl(widget=ui_elements, position="topright"))
    map_obj.add_control(WidgetControl(widget=output, position="bottomright"))
    map_obj.add_control(WidgetControl(widget=chart_output, position="bottomleft"))

    return map_obj
