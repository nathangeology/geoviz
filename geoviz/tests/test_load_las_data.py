from unittest import TestCase
import pkg_resources
from geoviz import LoadLasData


class TestLoad_las_data(TestCase):
    def setUp(self):
        self.filename = pkg_resources.resource_filename("geoviz", "sample_data/7_1-1.las")

    def test_get_data(self):
        data = LoadLasData.get_data(self.filename)
        self.assertEqual(data.shape[0], 16230)

