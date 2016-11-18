import plotly.plotly as py
import pandas as pd
from wave_6_dict import int_dic

def plotly_guy(country_averages,wave):
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
# df = load_wave('WV6.dat')
# df['COUNTRY'] = df.iloc[:,1].replace(d)
# df = df.convert_objects(convert_numeric=True)
# df_grouped = df.groupby('COUNTRY').mean().iloc[:,5]
    if wave == 'All':
        extra = '(1981-2014)'
    elif wave == 1:
        extra = '(1981-1984)'
    elif wave == 2:
        extra = '(1990-1994)'
    elif wave == 3:
        extra = '(1995-1998)'
    elif wave == 4:
        extra = '(1999-2004)'
    elif wave == 5:
        extra = '(2005-2009)'
    else:
        extra = '(2010-2014)'

    indexes = [32,
    56,
    124,
    208,
    250,
    276,
    352,
    372,
    380,
    392,
    484,
    528,
    578,
    710,
    724,
    752,
    826,
    840,
    909]
    indexes = ['Argentina',
    'Belgium',
    'Canada',
    'Denmark',
    'France',
    'Germany',
    'Iceland',
    'Ireland',
    'Italy',
    'Japan',
    'Mexico',
    'Netherlands',
    'Norway',
    'South Africa',
    'Spain',
    'Sweden',
    'Great Britain',
    'United States',
    'North Ireland']

    values = [-0.68392085996005725,
    -0.25153475312064738,
    -1.5428951227788785,
    4.6243551285409819,
    2.5600728856060369,
    1.0028611556246858,
    0.32051412969304005,
    -1.9756964211813473,
    0.11517378897616572,
    2.3312777045503985,
    -2.0512107147762966,
    1.8417593247050972,
    0.82508458689334585,
    -1.690275988166233,
    0.61877341152992837,
    3.2798758787184918,
    1.0679704529249463,
    -1.9529745026112391,
    -1.5237377879471015]
#499, 688
    #df_grouped = pd.Series(index = ['France', 'Denmark'], data = [4.624355, -2.051211])
    #py.sign_in('nordik91', 'zeqbxvvscf')
    py.sign_in('kruegg', 'zrm5q44z5e')
    # kurt user name kruegg
    # kurt password 12345678
    locations = pd.DataFrame(country_averages).reset_index()
    locations = locations.drop(locations[(locations.country == 499) | (locations.country == 688)].index, axis = 0)
    locations1 = locations.iloc[:,0].replace(int_dic)
    print locations1
    locations2 = locations.iloc[:,1]
    print locations2

    data = [ dict(
            type = 'choropleth', locationmode = 'country names',
            locations = locations1,
            #z = df['GDP (BILLIONS)'],
            z = locations2,
            text = locations1,
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
        title = 'First Principal Component: ' + 'Wave ' +  str(wave)  + ' ' +  extra,
        geo = dict(
            showframe = True,
            showcoastlines = True,
            projection = dict(
                type = 'Mercator'
            )
        )
    )

    fig = dict( data=data, layout=layout )
    py.iplot( fig, validate=False, filename= 'Wave' +  str(wave) )
