import altair as alt
import pandas as pd


class AltAirLogPlot(object):
    @classmethod
    def plot_log_df(cls, df):
        chart = alt.Chart(df).mark_circle(size=60).encode(
            x='GR',
            y='DEPT',
            color='GR',
            tooltip=['DEPT', 'GR']
        ).interactive()
        print('here')