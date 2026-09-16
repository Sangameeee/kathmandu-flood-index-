import geopandas as gpd
import folium
import os
waterways = gpd.read_file("data/waterways.geojson")
waterways_utm = waterways.to_crs(epsg=32645)
mock_flood_utm = waterways_utm.buffer(80)
flood_extent = gpd.GeoDataFrame(geometry=[mock_flood_utm.to_crs(epsg=4326).geometry.union_all()], crs="EPSG:4326")
print(flood_extent.geometry.iloc[0].centroid)
print(waterways.geometry.iloc[0].centroid)
