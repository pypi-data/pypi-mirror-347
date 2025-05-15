import geopandas as gpd
import rasterio
import rasterio.mask
import numpy as np
import pandas as pd
from shapely.geometry import mapping


def clip_raster_to_geometry(raster_path, geometry):
    """Clip a raster to a given geometry.

    Args:
        raster_path (str): Path to the land cover raster file.
        geometry (GeoDataFrame or geometry): Polygon geometry to clip to.

    Returns:
        tuple: clipped raster array and metadata
    """
    if isinstance(geometry, gpd.GeoDataFrame):
        geometry = geometry.to_crs("EPSG:4326")
        features = [mapping(geom) for geom in geometry.geometry]
    else:
        features = [mapping(geometry)]

    with rasterio.open(raster_path) as src:
        out_image, out_transform = rasterio.mask.mask(src, features, crop=True)
        out_meta = src.meta.copy()
        out_meta.update(
            {
                "transform": out_transform,
                "height": out_image.shape[1],
                "width": out_image.shape[2],
            }
        )

    return out_image[0], out_meta


def calculate_landcover_stats(raster_array, pixel_size, class_names=None):
    """Calculate area and percent cover for each land cover type.

    Args:
        raster_array (np.ndarray): 2D array of land cover class values.
        pixel_size (float): Pixel size in meters (e.g., 30 for Landsat).
        class_names (dict): Optional lookup of class values to labels.

    Returns:
        DataFrame: Summary with class, area (sq. meters), and percent.
    """
    unique, counts = np.unique(raster_array[raster_array != 0], return_counts=True)
    total_pixels = counts.sum()
    pixel_area = pixel_size**2

    data = {
        "class_value": unique,
        "pixel_count": counts,
        "area_m2": counts * pixel_area,
        "percent": 100 * counts / total_pixels,
    }

    df = pd.DataFrame(data)

    if class_names:
        df["label"] = df["class_value"].map(class_names)
    return df[["class_value", "label", "area_m2", "percent"]] if "label" in df else df


def compare_years(df1, df2):
    """Compare land cover stats between two years.

    Args:
        df1 (DataFrame): Stats from year 1.
        df2 (DataFrame): Stats from year 2.

    Returns:
        DataFrame: Change stats (area and percent).
    """
    merged = pd.merge(df1, df2, on="class_value", suffixes=("_year1", "_year2"))
    merged["area_change_m2"] = merged["area_m2_year2"] - merged["area_m2_year1"]
    merged["percent_change"] = merged["percent_year2"] - merged["percent_year1"]
    return merged
