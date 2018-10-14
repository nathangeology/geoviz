import altair as alt
import pandas as pd


class AltAirLogPlot(object):
    @classmethod
    def plot_log_df(cls, df):
        chart = alt.Chart(df).mark_line(interpolate='basis', orient='vertical').encode(
            x=alt.X('GR:Q', scale=alt.Scale(
                domain=(0, 100),
                clamp=True
            )),
            y='DEPT:Q',
            order='DEPT',
            fill='GR',
            tooltip=['DEPT', 'GR'],

        ).interactive(bind_x=False)
        return chart

    @classmethod
    def plot_multi_logs(cls, df, log_names=None):
        df = cls.handle_log_names(df, log_names)
        df.sort_values(by=['DEPT'], inplace=True, ascending=True)
        df = cls.melt_df(df)
        chart = alt.Chart(df).mark_line().encode(
            x=alt.X('value'),
            y=alt.Y('DEPT', sort='descending'),
            tooltip=['DEPT', 'value'],
            order='DEPT',
            column='variable',
            color='variable'
        ).properties(
            width=50,
            height=600
        ).interactive(bind_x=False)

        return chart

    @classmethod
    def multi_log_plot_version(cls, df, log_names=None):
        df = cls.handle_log_names(df, log_names)
        plot_list = [x for x in df.columns if x is not 'DEPT']
        chart1 = alt.Chart(df).mark_line().encode(
            alt.X(plot_list[0], type='quantitative'),
            alt.Y('DEPT', sort='descending', type='quantitative'),
            order='DEPT'
        ).properties(
            width=50,
            height=600
        ).interactive(bind_x=False)
        chart2 = alt.Chart(df).mark_line().encode(
            alt.X(plot_list[1], type='quantitative'),
            alt.Y('DEPT', sort='descending', axis=None, type='quantitative'),
            order='DEPT'
        ).properties(
            width=50,
            height=600
        ).interactive(bind_x=False)
        chart = alt.hconcat(chart1, chart2)
        return chart

    @classmethod
    def melt_df(cls, df):
        return df.melt(id_vars=['DEPT'])


    @classmethod
    def handle_log_names(cls, df, log_names=None):
        if log_names is not None:
            dept = df['DEPT']
            df = df[log_names]
            if 'DEPT' not in df:
                df['DEPT'] = dept
        return df
