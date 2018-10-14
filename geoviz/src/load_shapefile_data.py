import pandas as pd
import shapefile
from collections import defaultdict
from osgeo import ogr, osr
import geopandas as gpd

class LoadShpData(object):
    @classmethod
    def get_data(cls, filename):
        data = gpd.read_file(filename)
        data = data.to_crs(epsg=4326)
        data['X'] = data['geometry'].x
        data['Y'] = data['geometry'].y
        return data
