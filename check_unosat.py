import geopandas as gpd
path = "data/flood_shp/FL20240928NPL_SHP/S1_20240929_FloodExtent_Gandaki_Lumbini_Bagmati_Madhesh.shp"
flood = gpd.read_file(path)
print("CRS:", flood.crs)
print("Bounds:", flood.total_bounds)
