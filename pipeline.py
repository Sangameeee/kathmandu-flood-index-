import os
import requests
import zipfile
import geopandas as gpd
import osmnx as ox
import pandas as pd
import folium
from shapely.geometry import Point

# Define directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# Configure osmnx
ox.settings.overpass_url = 'https://lz4.overpass-api.de/api/interpreter'
# If the above fails, you can try: 'https://overpass.kumi.systems/api/interpreter'

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Download UNOSAT Flood Shapefile
def download_flood_data():
    url = "https://unosat.org/static/unosat_filesystem/3993/FL20240928NPL_SHP.zip"
    zip_path = os.path.join(DATA_DIR, "FL20240928NPL_SHP.zip")
    
    if not os.path.exists(zip_path):
        print("Downloading UNOSAT flood data...")
        response = requests.get(url, stream=True)
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download complete.")
    
    extract_dir = os.path.join(DATA_DIR, "flood_shp")
    if not os.path.exists(extract_dir):
        print("Extracting shapefile...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print("Extraction complete.")
        
    return extract_dir

# 2. Pull OSM Data for Balkhu, Kathmandu
def fetch_osm_data():
    print(f"Fetching OSM building footprints for Balkhu area bounding box...")
    
    # Bounding box around Balkhu/Kalanki
    north, south, east, west = 27.695, 27.675, 85.305, 85.285
    # osmnx v2+ expects bbox as (north, south, east, west)
    bbox = (north, south, east, west)
    
    try:
        buildings = ox.features_from_bbox(bbox=bbox, tags={'building': True})
    except Exception as e:
        print(f"Error fetching buildings from bbox: {e}")
        buildings = gpd.GeoDataFrame()
        
    # Get rivers/waterways
    print("Fetching waterways...")
    try:
        waterways = ox.features_from_bbox(bbox=bbox, tags={'waterway': 'river'})
    except Exception as e:
        print(f"Error fetching waterways from bbox: {e}")
        waterways = gpd.GeoDataFrame()
        
    return buildings, waterways

if __name__ == "__main__":
    download_flood_data()
    buildings, waterways = fetch_osm_data()
    
    print(f"Fetched {len(buildings)} buildings and {len(waterways)} waterways.")
    
    # Clean column types for GeoJSON export (guard against empty DataFrames)
    if not buildings.empty:
        for col in buildings.columns:
            try:
                if isinstance(buildings[col].dropna().iloc[0], list):
                    buildings[col] = buildings[col].astype(str)
            except IndexError:
                pass
    if not waterways.empty:
        for col in waterways.columns:
            try:
                if isinstance(waterways[col].dropna().iloc[0], list):
                    waterways[col] = waterways[col].astype(str)
            except IndexError:
                pass

    buildings.to_crs(epsg=4326).to_file(os.path.join(DATA_DIR, "buildings.geojson"), driver="GeoJSON")
    waterways.to_crs(epsg=4326).to_file(os.path.join(DATA_DIR, "waterways.geojson"), driver="GeoJSON")
