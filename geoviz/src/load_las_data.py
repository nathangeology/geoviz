import altair as alt
import lasio
import pandas as pd


class LoadLasData(object):
    @classmethod
    def get_data(cls, filename):
        las_file = lasio.read(filename)
        return pd.DataFrame(data=las_file.data, index=las_file.index, columns=las_file.curvesdict.keys())
