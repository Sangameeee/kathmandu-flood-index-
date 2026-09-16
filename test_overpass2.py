import requests
import geopandas as gpd
from shapely.geometry import Polygon, LineString

overpass_url = "https://overpass.kumi.systems/api/interpreter"
overpass_query = """
[out:json];
(
  way["building"](27.675,85.285,27.695,85.305);
);
out geom;
"""
print("Fetching from Overpass...")
response = requests.post(overpass_url, data={'data': overpass_query})
try:
    data = response.json()
    print("Got data. Elements:", len(data.get('elements', [])))
except Exception as e:
    print(response.text)
