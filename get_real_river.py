import osmnx as ox
import geopandas as gpd

ox.settings.overpass_url = 'https://lz4.overpass-api.de/api/interpreter'
try:
    waterways = ox.features_from_bbox(bbox=(85.285, 27.675, 85.305, 27.695), tags={'waterway': 'river'})
    print(f"Fetched {len(waterways)} real waterways.")
    waterways.to_file("data/waterways.geojson", driver="GeoJSON")
except Exception as e:
    print(f"lz4 failed: {e}")

try:
    buildings = ox.features_from_bbox(bbox=(85.285, 27.675, 85.305, 27.695), tags={'building': True})
    print(f"Fetched {len(buildings)} real buildings.")
    for col in buildings.columns:
        if isinstance(buildings[col].iloc[0], list):
            buildings[col] = buildings[col].astype(str)
    buildings.to_file("data/buildings.geojson", driver="GeoJSON")
except Exception as e:
    print(f"lz4 failed buildings: {e}")
