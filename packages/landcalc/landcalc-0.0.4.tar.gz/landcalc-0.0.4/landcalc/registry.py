LANDCOVER_DB = {
    "NLCD (Esri WMS)": {
        "source": "wms",
        "url": "https://gis.apfo.usda.gov/arcgis/services/NRCS/US_NLCD/MapServer/WMSServer",
        "layers": {"2001": "5", "2006": "6", "2011": "7", "2016": "8", "2019": "9"},
        "pixel_size": 30,
    },
    "Global Land Cover (Esri)": {
        "source": "wms",
        "url": "https://services.arcgisonline.com/arcgis/services/World_Land_Cover/MapServer/WMSServer",
        "layers": {"2020": "0"},
        "pixel_size": 10,
    },
    "ESA Land Cover (Esri)": {
        "source": "wms",
        "url": "https://services.arcgisonline.com/arcgis/services/ESA_WorldCover_2020/MapServer/WMSServer",
        "layers": {"2020": "0"},
        "pixel_size": 10,
    },
}
