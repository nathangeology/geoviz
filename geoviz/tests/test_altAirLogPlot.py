from unittest import TestCase
from geoviz import LoadLasData
from geoviz import AltAirLogPlot
import pkg_resources


class TestAltAirLogPlot(TestCase):
    def setUp(self):
        self.filename = pkg_resources.resource_filename("geoviz", "sample_data/7_1-1.las")
        self.test_data = LoadLasData.get_data(self.filename)

    def test_plot_log_df(self):
        chart = AltAirLogPlot.plot_log_df(self.test_data)
        chart.serve()
        print('here')

    def test_plot_multi_logs(self):
        chart = AltAirLogPlot.plot_multi_logs(self.test_data)
        chart.serve()
        print('here')

    def test_plot_multi_logs(self):
        chart = AltAirLogPlot.plot_multi_logs(self.test_data, ['GR', 'NPHI', 'RHOB'])
        chart.serve()
        print('here')

    def test_plot_quad_combo(self):
        chart = AltAirLogPlot.plot_quad_combo_tracks(self.test_data)
        chart.serve()
        print('here')


