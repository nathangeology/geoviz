import altair as alt
import pandas as pd


class AltAirLogPlot(object):
    df = None

    DTCSH = 70
    DTCMA = 55.8
    DTCW = 200
    #PHIS = (DTC - DTCMA) / (DTCW - DTCMA) / KCP
    def __init__(self, df):
        self.df = df

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
        class_instance = cls(df)
        df = class_instance._handle_log_names(df, log_names)
        df.sort_values(by=['DEPT'], inplace=True, ascending=True)
        df_unscaled = df.copy()
        df = class_instance._scale_data_for_plotting(df)
        df = class_instance._melt_df(df)

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
    def plot_quad_combo_tracks(cls, df):
        class_instance = cls(df)
        brush = alt.selection(type='interval', encodings=['y'])
        selector_track = class_instance.plot_GR_SP_selection_chart(brush)
        GR_SP_track = class_instance.plot_GR_SP(brush)
        porosity_track = class_instance.plot_porosity(brush)
        resistivity_track = class_instance.plot_resistivity_track(brush)
        return selector_track | GR_SP_track | resistivity_track | porosity_track

    def plot_GR_SP_selection_chart(self, brush, GR_str='GR', SP_str='SP') -> alt.Chart:
        df = self._handle_log_names(self.df, log_names=[GR_str, SP_str])
        df = self._melt_df(df)
        chart = alt.Chart(df).mark_line().encode(
            x=alt.X('value', axis=alt.Axis(title='Selector')),
            y=alt.Y('DEPT', sort='descending'),
            # x=alt.X('value:Q', axis=alt.Axis(title='Selector')),
            # y=alt.Y('DEPT:O', sort='ascending'),
            tooltip=['DEPT', 'value'],
            order='DEPT',
            color='variable'
        ).properties(
            width=100,
            height=600
        ).add_selection(brush)
        return chart

    def plot_GR_SP(self, brush, GR_str='GR', SP_str='SP')->alt.Chart:
        df = self._handle_log_names(self.df, log_names=[GR_str, SP_str])
        df = self._melt_df(df)

        color_scale = alt.Scale(
            domain=['SP', 'GR', 'RDEP', 'RMED', 'RSHA', 'RHOB', 'NPHI', 'DT', 'DTC'],
            range=['#B71C1C',
                   '#4A148C',
                   '#1A237E',
                   '#01579B',
                   '#004D40',
                   '#33691E',
                   '#F57F17',
                   '#E65100',
                   '#3E2723']
        )

        chart = alt.Chart(df).mark_line().encode(
            x=alt.X('value', axis=alt.Axis(title='SP GR')),
            y=alt.Y('DEPT', sort='descending', scale={'domain': brush.ref(), 'zero': True}),
            # x=alt.X('value:Q', axis=alt.Axis(title='SP GR')),
            # y=alt.Y('DEPT:O', sort='ascending', scale={'domain': brush.ref(), 'zero': True}),
            color=alt.Color('variable:N', legend=None, scale=color_scale),
            tooltip=['DEPT', 'value'],
            order='DEPT',
            opacity=alt.OpacityValue(0.8)
        ).properties(
            width=100,
            height=600
        )
        return chart

    def plot_resistivity_track(self, brush, deep_res_str='RDEP', med_res_str='RMED', shallow_res_str='RSHA')->alt.Chart:
        df = self._handle_log_names(self.df, log_names=[deep_res_str, med_res_str, shallow_res_str])
        df = self._melt_df(df)
        chart = alt.Chart(df).mark_line().encode(
            x=alt.X('value', axis=alt.Axis(title='Resistivity'), scale={'type': 'log'}),
            y=alt.Y('DEPT', sort='descending', scale={'domain': brush.ref(), 'zero': True}, axis=None),
            # x=alt.X('value:Q', axis=alt.Axis(title='Resistivity'), scale={'type': 'log'}),
            # y=alt.Y('DEPT:O', sort='ascending', scale={'domain': brush.ref(), 'zero': True}, axis=None),
            tooltip=['DEPT', 'value'],
            order='DEPT',
            color='variable',
            opacity=alt.OpacityValue(0.8)
        ).properties(
            width=100,
            height=600
        )
        return chart

    def plot_porosity(self, brush, density_str='RHOB', neutron_str='NPHI', sonic_str='DTC', lithology_dens=2.65)->alt.Chart:
        df = self._handle_log_names(self.df, log_names=[density_str, neutron_str, sonic_str])
        df['DPHI'] = (df[density_str] - lithology_dens)/(1-lithology_dens)
        df['PHIS'] = (df[sonic_str] - self.DTCMA) / (self.DTCW - self.DTCMA)
        df = self._handle_log_names(df, log_names=['NPHI', 'DPHI', 'PHIS'])
        df = self._melt_df(df)
        chart = alt.Chart(df).mark_line().encode(
            x=alt.X('value', axis=alt.Axis(title='Porosity')),
            y=alt.Y('DEPT', sort='descending', axis=None, scale={'domain': brush.ref(), 'zero': True}),
            # x=alt.X('value:Q', axis=alt.Axis(title='Porosity')),
            # y=alt.Y('DEPT:O', sort='ascending', axis=None, scale={'domain': brush.ref(), 'zero': True}),
            tooltip=['DEPT', 'value'],
            order='DEPT',
            color='variable',
            opacity=alt.OpacityValue(0.8)
        ).properties(
            width=100,
            height=600
        )
        return chart

    @staticmethod
    def _scale_data_for_plotting(df):
        for col in df:
            if col == 'DEPT':
                continue
            series = df[col]
            series = series / series.max()
            df[col] = series
        return df

    @staticmethod
    def _melt_df(df):
        return df.melt(id_vars=['DEPT'])


    @staticmethod
    def _handle_log_names(df, log_names=None):
        if log_names is not None:
            dept = df['DEPT']
            df = df[log_names]
            if 'DEPT' not in df:
                df['DEPT'] = dept
        return df
