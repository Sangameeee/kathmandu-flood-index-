import os
import geopandas as gpd
from shapely.geometry import Polygon, LineString
import numpy as np

# Define directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def generate_mock_data():
    print("Generating synthetic OSM data due to Overpass API unavailability...")
    
    # Bounding box around Balkhu/Kalanki
    north, south, east, west = 27.695, 27.675, 85.305, 85.285
    
    # 1. Generate realistic meandering synthetic river
    lats = np.linspace(north, south, 50)
    # create a meandering effect using sine waves
    lons = 85.295 + np.sin(np.linspace(0, 3 * np.pi, 50)) * 0.003 + np.sin(np.linspace(0, 7 * np.pi, 50)) * 0.001
    
    river_coords = list(zip(lons, lats))
    waterway = LineString(river_coords)
    waterways_gdf = gpd.GeoDataFrame(
        {'name': ['Bishnumati River'], 'waterway': ['river']},
        geometry=[waterway],
        crs="EPSG:4326"
    )
    waterways_gdf.to_file(os.path.join(DATA_DIR, "waterways.geojson"), driver="GeoJSON")
    print("Saved mock waterways.")
    
    # 2. Generate synthetic buildings (cluster them more realistically)
    buildings = []
    
    # Generate ~500 random buildings within the bounding box
    np.random.seed(42)
    lons_b = np.random.uniform(west, east, 500)
    lats_b = np.random.uniform(south, north, 500)
    
    # building types
    b_types = ['residential', 'commercial', 'school', 'hospital']
    b_probs = [0.8, 0.15, 0.03, 0.02]
    
    for i in range(500):
        # Create a small polygon (approx 10x10 meters -> 0.0001 deg)
        lon = lons_b[i]
        lat = lats_b[i]
        size = np.random.uniform(0.00005, 0.00015)
        poly = Polygon([
            (lon, lat),
            (lon + size, lat),
            (lon + size, lat + size),
            (lon, lat + size)
        ])
        b_type = np.random.choice(b_types, p=b_probs)
        buildings.append({
            'geometry': poly,
            'building': 'yes',
            'amenity': b_type if b_type != 'residential' else None,
            'osmid': 100000 + i
        })
        
    buildings_gdf = gpd.GeoDataFrame(buildings, crs="EPSG:4326")
    buildings_gdf.to_file(os.path.join(DATA_DIR, "buildings.geojson"), driver="GeoJSON")
    print(f"Saved {len(buildings)} mock buildings.")

if __name__ == "__main__":
    generate_mock_data()
