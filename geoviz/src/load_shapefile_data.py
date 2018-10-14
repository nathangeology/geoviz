import pandas as pd
import shapefile
from collections import defaultdict


class LoadShpData(object):
    @classmethod
    def get_data(cls, filename):
        sf = shapefile.Reader(filename)
        outputdict = defaultdict(list)
        fields = sf.fields
        for idx, shape in enumerate(list(sf.iterShapes())):
            points = shape.points
            points = points[0]
            outputdict['X'].append(points[0])
            outputdict['Y'].append(points[1])
            records = sf.record(idx)
            for idx2, record in enumerate(records):
                field_name = fields[idx2][0]
                outputdict[field_name].append(record)

        return pd.DataFrame(outputdict)
