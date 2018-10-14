import altair as alt
from vega_datasets import data


class WellLocationMap(object):
    @classmethod
    def create_map_plot(cls, df):
        countries = alt.topo_feature(data.world_110m.url, 'countries')

        base = alt.Chart(countries).mark_geoshape(
            fill='#666666',
            stroke='white'
        ).properties(
            width=600,
            height=400
        )
        projections = ['mercator']
        charts = [base.project(proj).properties(title=proj)
                  for proj in projections]

        map_chart_data = alt.Chart(df).mark_geoshape().project('mercator')

        return map_chart_data

