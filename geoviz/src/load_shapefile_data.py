
import geopandas as gpd

class LoadShpData(object):
    @classmethod
    def get_data(cls, filename):
        data = gpd.read_file(filename)
        data = data.to_crs(epsg=4326)
        data['X'] = data['geometry'].x
        data['Y'] = data['geometry'].y
        return data
