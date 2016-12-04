# will clean and comment following presentation

import plotly.plotly as py
import pandas as pd
from country_dictionary import return_country_dictionary
from sklearn.preprocessing import StandardScaler
import numpy as np

def plot_all_graphs(waves,component_numbers = [1,2,3]):
    '''
    INPUT: LIST - each element of list is a wave object, one for each time period
           LIST - contains principal component numbers that should be graphed

    Creates Plotly choropleth maps for each time period and each principal component
    '''
    for wave in waves:
        for pc in component_numbers:
            plot_choropleth(wave,pc)



def plot_choropleth(wave,component_number):
    '''
    INPUT: WAVE object - Wave object created in 'analyze_surveys.py'
           INT - the principal component by which countries should be shaded

    Creates Plotly choropleth map, where each country is shaded by its value for the given principal component.
    '''

    py.sign_in('nordik91', 'zeqbxvvscf')
    wave_number = wave.wave_number

    # create label for graph based on time period
    if wave_number == 'All':
        time_period = '(1981-2014)'
    elif wave_number == 1:
        time_period = '(1981-1984)'
    elif wave_number == 2:
        time_period = '(1990-1994)'
    elif wave_number == 3:
        time_period = '(1995-1998)'
    elif wave_number == 4:
        time_period = '(1999-2004)'
    elif wave_number == 5:
        time_period = '(2005-2009)'
    else:
        time_period = '(2010-2014)'

    #Create index of countries to be shown on map
    locations_index = pd.Series(wave.grouped_by_country_pca.index)
    locations_string = locations_index.replace(return_country_dictionary())

    # Standardize component values
    scaler = StandardScaler()
    component_values = pd.Series(wave.grouped_by_country_pca.loc[:,component_number])
    component_values_scaled = scaler.fit_transform(component_values)
    component_values_scaled = np.round(component_values_scaled,2)

    # Determine three questions most correlated with principal component
    question1 = wave.correlation_dic_pca[component_number].index[0]
    question2 = wave.correlation_dic_pca[component_number].index[1]
    question3 = wave.correlation_dic_pca[component_number].index[2]


    # Text to be displayed when hovering over country: shows average survey responses to three questions most correlated with principal component
    hover_text =  ['\n' + str(locations_string.iloc[i]) +'\n\n'+ question1+': '  + str(int(country[1][question1])) +
    '\n' + question2 +  ': ' + str(int(country[1][question2])) + '\n' +  question3 +  ': '
    + str(int(country[1][question3])) for i,country in enumerate(wave.grouped_by_country_pca.loc[locations_index,:].iterrows())]


    # data for world map
    data = [ dict(
            type = 'choropleth', locationmode = 'country names',
            locations = locations_string,
            z = -1*component_values_scaled,
            text = hover_text,
            colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
                [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
            autocolorscale = True,
            reversescale = True,
            marker = dict(
                line = dict (
                    color = 'rgb(180,180,180)',
                    width = 0.5
                ) ),
            colorbar = dict(
                autotick = False,
                tickprefix = '',
                title = 'Principal Component Value '),
          ) ]

    layout = dict(
        title = 'Wave ' +  str(wave_number)  + ' ' +  time_period + ', Principal Component ' + str(component_number) ,
        geo = dict(
            showframe = True,
            showcoastlines = True,
            projection = dict(
                type = 'robinson'
            )
        )
    )

    fig = dict( data=data, layout=layout )
    py.iplot( fig, validate=False, filename= 'Wave ' +  str(wave_number) + '_PC' +  str(component_number) )
