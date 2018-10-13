from unittest import TestCase
from geoviz import LoadLasData
from geoviz import AltAirLogPlot
import pkg_resources


class TestAltAirLogPlot(TestCase):
    def setUp(self):
        self.filename = pkg_resources.resource_filename("geoviz", "sample_data/7_1-1.las")
        self.test_data = LoadLasData(self.filename)

    def test_plot_log_df(self):
        AltAirLogPlot.plot_log_df(self.test_data)
        print('here')
