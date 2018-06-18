# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.plotly as py
from plotly.graph_objs import *
import pandas as pd
import plotly.figure_factory as ff
from geopy.geocoders import Nominatim
import datetime

lt=pd.read_csv('export.csv', sep=';', 
               error_bad_lines=False,header=None)
lt.head()
lt.fillna(0)
for c in [1,2,3,5]:
    lt[c]=lt[c].str.strip().str.lower()
lt[0]=pd.to_datetime(lt[0])
#lt=lt[(lt[0].dt.year==2018)&(lt[0] <pd.Timestamp.today()) ]





mapbox_access_token = 'pk.eyJ1IjoicmdpbmduYWdlbCIsImEiOiJjamc1OGN5dDMxNjgzMndwcWJkYzhwMjI4In0.18AdT2y0ZTzoq58R8ws62w'

cityLatLong = pd.read_csv('cityLatLong.csv', sep='\t')
print(cityLatLong)

data = Data([
    Scattermapbox(
        lat=cityLatLong['lat'],
        lon=cityLatLong['long'],
        mode='markers',
        marker=Marker(
            size=6
        ),
        text=cityLatLong['city'],
    )
])
layout = Layout(
    autosize=False,
    hovermode='closest',
    width=830,
    height=830,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=52.2,
            lon=5.4
        ),
        pitch=0,
        zoom=6
    ),
)

fig = dict(data=data, layout=layout)

app = dash.Dash()
server = app.server

def generateInitialTable():
    value_vs_rest=pd.DataFrame([lt.groupby(5)[4].sum()] ).T
    value_vs_rest.loc['totaal'] = sum(value_vs_rest[4])
    valueWithLeerlingen = value_vs_rest[4].apply(lambda x: str(x) + " leerlingen")
    trace = go.Table(
    header=dict(values=['Oplossing', "Nederland"],
                line = dict(color='#7D7F80'),
                fill = dict(color='#a1c3d1'),
                align = ['left'] * 5),
    cells=dict(values=[value_vs_rest.index,
                       valueWithLeerlingen],
               line = dict(color='#7D7F80'),
               fill = dict(color='#EDFAFF'),
               align = ['left'] * 5))
    layout = dict(width=700, height=500)
    data = [trace]
    return dict(data=data, layout=layout)

def generateLineChart():
    trace1 = go.Scatter(
    x=[2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
    y=[2, 124, 678, 1824, 2909, 4053, 4909, 6086, 7378, 8838, 10537],
    name = 'FTE',
    showlegend=True
    )

    data = [trace1]

    return dict(data=data)

def generateInitialBarChart():
    ams_vs_rest=pd.DataFrame([lt[5].value_counts()]).T
    ams_vs_rest.columns=['Nederland']
    ams_vs_rest.index.name='Oplossing'

    trace1 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][0]) * 100), 2)],
    name=ams_vs_rest.index[0],
    orientation = 'h',
    marker = dict(
        color = 'rgba(127,201,127, 0.6)',
        line = dict(
            color = 'rgba(127,201,127, 1.0)',
            width = 3)
    )
    )

    trace2 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][1]) * 100), 2)],
    name=ams_vs_rest.index[1],
    orientation = 'h',
    marker = dict(
        color = 'rgba(190,174,212, 0.6)',
        line = dict(
            color = 'rgba(190,174,212, 1.0)',
            width = 3)
    )
    )

    trace3 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][2]) * 100), 2)],
    name=ams_vs_rest.index[2],
    orientation = 'h',
    marker = dict(
        color = 'rgba(253,192,134, 0.6)',
        line = dict(
            color = 'rgba(253,192,134, 1.0)',
            width = 3)
    )
    )

    trace4 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][3]) * 100), 2)],
    name=ams_vs_rest.index[3],
    orientation = 'h',
    marker = dict(
        color = 'rgba(255,255,153, 0.6)',
        line = dict(
            color = 'rgba(255,255,153, 1.0)',
            width = 3)
    )
    )

    trace5 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][4]) * 100), 2)],
    name=ams_vs_rest.index[4],
    orientation = 'h',
    marker = dict(
        color = 'rgba(56,108,176, 0.6)',
        line = dict(
            color = 'rgba(56,108,176, 1.0)',
            width = 3)
    )
    )

    trace6 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][5]) * 100), 2)],
    name=ams_vs_rest.index[5],
    orientation = 'h',
    marker = dict(
        color = 'rgba(240,2,127, 0.6)',
        line = dict(
            color = 'rgba(240,2,127, 1.0)',
            width = 3)
    )
    )

    trace7 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][6]) * 100), 2)],
    name=ams_vs_rest.index[6],
    orientation = 'h',
    marker = dict(
        color = 'rgba(191,91,23, 0.6)',
        line = dict(
            color = 'rgba(191,91,23, 1.0)',
            width = 3)
    )
    )

    trace8 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][7]) * 100), 2)],
    name=ams_vs_rest.index[7],
    orientation = 'h',
    marker = dict(
        color = 'rgba(102,102,102, 0.6)',
        line = dict(
            color = 'rgba(102,102,102, 1.0)',
            width = 3)
    )
    )

    trace9 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][8]) * 100), 2)],
    name=ams_vs_rest.index[8],
    orientation = 'h',
    marker = dict(
        color = 'rgba(227,26,28, 0.6)',
        line = dict(
            color = 'rgba(227,26,28, 1.0)',
            width = 3)
    )
    )
    data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9]
    layout = go.Layout(
        barmode='stack',
        legend=dict(
            traceorder='reversed'
        ),
        xaxis=dict(
            ticksuffix="%"
        )
    )
    return go.Figure(data=data, layout=layout)

app.layout = html.Div([
    dcc.Markdown('''
# Primair Onderwijs in Nederland

Door heel Nederland is er is een groot tekort aan docenten in het Primair Onderwijs. In grote steden zoals Rotterdam, Amsterdam en Den Haag ligt het tekort op dit moment rond de 1.6% en dit aantal neemt snel toe. 

Hieronder zie je een kaart van Nederland die laat zien wat het verwachte leraren tekort in 2020 is.

![Image](https://www.rijksoverheid.nl/binaries/medium/content/gallery/rijksoverheid/content-afbeeldingen/onderwerpen/werken-in-het-onderwijs/vacaturedruk-po-kaart.png)
''', className='container',
    containerProps={'style': {'maxWidth': '650px'}}),
    html.H2('Statistieken 2018', className='container', style={'maxWidth': '650px', "textAlign": "center"}),
    dcc.RangeSlider(
        id="my-slider",
        className='container',
        min=1,
        max=6,
        step=None,
        value=[1, 6],
        marks={
            1: {'label':'januari', 'style': {'font-weight': 'bold'}},
            2: {'label':'februari', 'style': {'font-weight': 'bold'}},
            3: {'label':'maart', 'style': {'font-weight': 'bold'}},
            4: {'label':'april', 'style': {'font-weight': 'bold'}},
            5: {'label':'mei', 'style': {'font-weight': 'bold'}},
            6: {'label':'juni', 'style': {'font-weight': 'bold'}},
        }
    ),
    dcc.Graph(id='my-map',
             figure = fig),
    html.Div([
        dcc.Graph(id='my-table',
            figure = generateInitialTable()),
        dcc.Graph(id='my-bar-chart',
            figure = generateInitialBarChart())
    ], style={'float': 'right'}),
    html.H2('Toename tekort', className='container', style={'maxWidth': '650px', "textAlign": "center"}),
    dcc.Graph(id="line-chart",
            figure=generateLineChart())

])

@app.callback(  
    Output(component_id='my-table', component_property='figure'),
    [Input(component_id='my-map', component_property='hoverData'),
    Input(component_id='my-slider', component_property='value')])
def update_output_div(input_value, slider):
    timeFixed = lt[(lt[0]>=datetime.date(2018, slider[0] ,1)) & (lt[0]<datetime.date(2018 ,slider[1]+1 ,1))]
    if(input_value==None):
        lt_value=timeFixed
        cityName="Nederland"
    else:
        cityName = input_value['points'][0]['text']
        lt_value=timeFixed[timeFixed[2].str.contains(cityName)]

    value_vs_rest=pd.DataFrame([lt_value.groupby(5)[4].sum()] ).T
    value_vs_rest.loc['totaal'] = sum(value_vs_rest[4])
    valueWithLeerlingen = value_vs_rest[4].apply(lambda x: str(x) + " leerlingen")
    trace = go.Table(
    header=dict(values=['Oplossing', cityName.title()],
                line = dict(color='#7D7F80'),
                fill = dict(color='#a1c3d1'),
                align = ['left'] * 5),
    cells=dict(values=[value_vs_rest.index,
                       valueWithLeerlingen],
               line = dict(color='#7D7F80'),
               fill = dict(color='#EDFAFF'),
               align = ['left'] * 5))
    layout = dict(width=700, height=500)
    data = [trace]
    fig = dict(data=data, layout=layout)

    return fig

@app.callback(  
    Output(component_id='my-map', component_property='figure'),
    [Input(component_id='my-slider', component_property='value')]
)
def update_map(slider):
    timeFilteredDF = lt[(lt[0]>=datetime.date(2018, slider[0] ,1)) & (lt[0]<datetime.date(2018 ,slider[1]+1 ,1))]
    uniqueTimeFilteredDF = cityLatLong.loc[cityLatLong['city'].isin(timeFilteredDF[2].unique())]
    data = Data([
    Scattermapbox(
        lat=uniqueTimeFilteredDF['lat'],
        lon=uniqueTimeFilteredDF['long'],
        mode='markers',
        marker=Marker(
            size=6
        ),
        text=uniqueTimeFilteredDF['city'],
    )
    ])
    layout = Layout(
        autosize=False,
        hovermode='closest',
        width=830,
        height=830,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=52.2,
                lon=5.4
            ),
            pitch=0,
            zoom=6
        ),
    )
    return dict(data=data, layout=layout)


@app.callback(  
    Output(component_id='my-bar-chart', component_property='figure'),
    [Input(component_id='my-map', component_property='hoverData'),
    Input(component_id='my-slider', component_property='value')])
def update_bar_chart(input_value, slider):
    print("slider0", slider[0])
    print("slider1", slider[1])
    #print("joe", lt[(lt[0]>=datetime.date(2018, slider[0] ,1)) & (lt[0]<datetime.date(2018 ,slider[1]+1 ,1))])
    timeFixed = lt[(lt[0]>=datetime.date(2018, slider[0] ,1)) & (lt[0]<datetime.date(2018 ,slider[1]+1 ,1))]
    print(timeFixed)
    cityName = input_value['points'][0]['text']
    lt_city=timeFixed[timeFixed[2].str.contains(cityName)]
    lt_not_city=timeFixed[~timeFixed[2].str.contains(cityName)]
    ams_vs_rest=pd.DataFrame([lt_not_city[5].value_counts(),lt_city[5].value_counts()] ).T
    ams_vs_rest.columns=['Nederland', cityName]
    ams_vs_rest.index.name='Oplossing'
    #ams_vs_rest.sort_values(input_value, ascending=False)

    trace1 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][0]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][0]) * 100), 2)],
    name=ams_vs_rest.index[0],
    orientation = 'h',
    marker = dict(
        color = 'rgba(127,201,127, 0.6)',
        line = dict(
            color = 'rgba(127,201,127, 1.0)',
            width = 3)
    )
    )

    trace2 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][1]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][1]) * 100), 2)],
    name=ams_vs_rest.index[1],
    orientation = 'h',
    marker = dict(
        color = 'rgba(190,174,212, 0.6)',
        line = dict(
            color = 'rgba(190,174,212, 1.0)',
            width = 3)
    )
    )

    trace3 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][2]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][2]) * 100), 2)],
    name=ams_vs_rest.index[2],
    orientation = 'h',
    marker = dict(
        color = 'rgba(253,192,134, 0.6)',
        line = dict(
            color = 'rgba(253,192,134, 1.0)',
            width = 3)
    )
    )

    trace4 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][3]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][3]) * 100), 2)],
    name=ams_vs_rest.index[3],
    orientation = 'h',
    marker = dict(
        color = 'rgba(255,255,153, 0.6)',
        line = dict(
            color = 'rgba(255,255,153, 1.0)',
            width = 3)
    )
    )

    trace5 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][4]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][4]) * 100), 2)],
    name=ams_vs_rest.index[4],
    orientation = 'h',
    marker = dict(
        color = 'rgba(56,108,176, 0.6)',
        line = dict(
            color = 'rgba(56,108,176, 1.0)',
            width = 3)
    )
    )

    trace6 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][5]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][5]) * 100), 2)],
    name=ams_vs_rest.index[5],
    orientation = 'h',
    marker = dict(
        color = 'rgba(240,2,127, 0.6)',
        line = dict(
            color = 'rgba(240,2,127, 1.0)',
            width = 3)
    )
    )

    trace7 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][6]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][6]) * 100), 2)],
    name=ams_vs_rest.index[6],
    orientation = 'h',
    marker = dict(
        color = 'rgba(191,91,23, 0.6)',
        line = dict(
            color = 'rgba(191,91,23, 1.0)',
            width = 3)
    )
    )

    trace8 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][7]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][7]) * 100), 2)],
    name=ams_vs_rest.index[7],
    orientation = 'h',
    marker = dict(
        color = 'rgba(102,102,102, 0.6)',
        line = dict(
            color = 'rgba(102,102,102, 1.0)',
            width = 3)
    )
    )

    trace9 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][8]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][8]) * 100), 2)],
    name=ams_vs_rest.index[8],
    orientation = 'h',
    marker = dict(
        color = 'rgba(227,26,28, 0.6)',
        line = dict(
            color = 'rgba(227,26,28, 1.0)',
            width = 3)
    )
    )

    data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9]
    layout = go.Layout(
        barmode='stack',
        legend=dict(
            traceorder='reversed'
        ),
        xaxis=dict(
            ticksuffix="%"
        )
    )
    print(data)
    return go.Figure(data=data, layout=layout)



    

app.css.append_css({
    'external_url': 'https://codepen.io/rens/pen/dKRZOo.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)