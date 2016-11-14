import plotly.plotly as py
import pandas as pd
from test import load_wave
from wave_6_dict import d

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
df = load_wave('WV6.dat')
df['COUNTRY'] = df.iloc[:,1].replace(d)
df = df.convert_objects(convert_numeric=True)
df_grouped = df.groupby('COUNTRY').mean().iloc[:,5]
py.sign_in('nordik91', 'zeqbxvvscf')
data = [ dict(
        type = 'choropleth', locationmode = 'country names',
        locations = pd.Series(df_grouped.index),
        #z = df['GDP (BILLIONS)'],
        z = df_grouped,
        text = pd.Series(df_grouped.index),
        colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
            [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            tickprefix = '$',
            title = 'friendship importance'),
      ) ]

layout = dict(
    title = 'friendship importance:\
            <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
            CIA World Factbook</a>',
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.iplot( fig, validate=False, filename='d3-world-map' )
