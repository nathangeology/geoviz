import altair as alt
from vega_datasets import data
import geopandas as gpd

class WellLocationMap(object):
    @classmethod
    def create_map_plot(cls, df, background):
        geoframe = df.copy()
        ocean_shp = gpd.read_file(background)
        temp = ocean_shp[ocean_shp['NAME'] == 'North Sea']
        df = df[['X', 'Y', 'wlbWellbor']]
        minY = df['Y'].min()
        maxY = df['Y'].max()
        minX = df['X'].min()
        maxX = df['X'].max()
        hover = alt.selection(type='single', on='mouseover', nearest=True,
                              fields=['X', 'Y'])
        df = alt.Chart(df).encode(
            longitude=alt.Longitude('X:Q'),
            latitude=alt.Latitude('Y:Q')
        )
        countries = alt.topo_feature(data.world_110m.url, 'countries')

        base = alt.Chart(countries).mark_geoshape(
            fill='#666666',
            stroke='white',
        ).properties(
            width=600,
            height=400
        )
        projections = ['mercator']
        charts = [base.project(proj).properties(title=proj)
                  for proj in projections]

        map_chart_data = df.mark_point().encode(
            color=alt.value('black'),
            size=alt.value(0.5),

        ).project('mercator').add_selection(hover)

        text = df.mark_text(dy=-5, align='right').encode(
            alt.Text('wlbWellbor', type='nominal'),
            opacity=alt.condition(~hover, alt.value(0), alt.value(1))
        )
        return charts[0] + map_chart_data + text

