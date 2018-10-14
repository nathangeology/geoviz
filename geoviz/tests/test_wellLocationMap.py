from unittest import TestCase
from geoviz import LoadShpData
from geoviz import WellLocationMap
import pkg_resources


class TestWellLocationMap(TestCase):
    def setUp(self):
        self.filename = pkg_resources.resource_filename("geoviz", "sample_data/loc_npd_ea_wells.shp")
        self.test_data = LoadShpData.get_data(self.filename)

    def test_create_map_plot(self):
        chart = WellLocationMap.create_map_plot(self.test_data)
        chart.serve()
        print('here')
