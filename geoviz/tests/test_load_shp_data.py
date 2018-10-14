from unittest import TestCase
import pkg_resources
from geoviz import LoadShpData


class TestLoadShpData(TestCase):
    def setUp(self):
        self.filename = pkg_resources.resource_filename("geoviz", "sample_data/loc_npd_ea_wells.shp")

    def test_get_data(self):
        df = LoadShpData.get_data(self.filename)
        self.assertEqual(df.shape[0], 1855)
