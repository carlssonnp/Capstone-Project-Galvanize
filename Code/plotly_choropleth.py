import plotly.plotly as py
import pandas as pd
from country_dictionary import int_dic

def plot_choropleth(wave):
    wave = wave_class.wave_number
    if wave == 'All':
        time_period = '(1981-2014)'
    elif wave == 1:
        time_period = '(1981-1984)'
    elif wave == 2:
        time_period = '(1990-1994)'
    elif wave == 3:
        time_period = '(1995-1998)'
    elif wave == 4:
        time_period = '(1999-2004)'
    elif wave == 5:
        time_period = '(2005-2009)'
    else:
        time_period = '(2010-2014)'


    py.sign_in('nordik91', 'zeqbxvvscf')


    locations = pd.Series(wave.grouped_by_country.index)
    #locations = locations.drop(locations[(locations.country == 499) | (locations.country == 688)].index, axis = 0)
    locations1 = locations.replace(int_dic)
    locations2 = pd.Series(wave.grouped_by_country[1])
    wave_class.grouped_by_country.index = pd.Series(wave.grouped_by_country.index).replace(int_dic)
    texts =  ['\n' + str(l[0]) +  '\n\nHow important is God in your life?\n1 means not important, 10 means extremely important \nAverage score: '+ str(int(l[1]['F063'])) +'\n\n' + 'Is abortion justifiable?\n1 means never justifiable, 10 means always justifiable \nAverage score: ' + str(int(l[1]['F121'])) for l in wave_class.grouped_by_country.iterrows()]
    data = [ dict(
            type = 'choropleth', locationmode = 'country names',
            locations = locations1,
            #z = df['GDP (BILLIONS)'],
            z = locations2,
            text = texts,
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
                tickprefix = '',
                title = 'Secular values/social freedom'),
          ) ]

    layout = dict(
        title = 'Wave ' +  str(wave)  + ' ' +  time_period + ', Principal Component 1' ,
        geo = dict(
            showframe = True,
            showcoastlines = True,
            projection = dict(
                type = 'Mercator'
            )
        )
    )

    fig = dict( data=data, layout=layout )
    py.iplot( fig, validate=False, filename= 'Wave ' +  str(wave) )
