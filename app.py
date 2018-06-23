# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
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
for c in [1,2,3]:
    lt[c]=lt[c].str.strip().str.lower()
lt[5]=lt[5].str.strip().replace('(', '').replace(')', '')

lt[0]=pd.to_datetime(lt[0])
#lt=lt[(lt[0].dt.year==2018)&(lt[0] <pd.Timestamp.today()) ]





mapbox_access_token = 'pk.eyJ1IjoicmdpbmduYWdlbCIsImEiOiJjamc1OGN5dDMxNjgzMndwcWJkYzhwMjI4In0.18AdT2y0ZTzoq58R8ws62w'

cityLatLong = pd.read_csv('cityLatLong.csv', sep='\t', index_col=False )
cityLatLong['city'] = cityLatLong['city'].str.replace('(', '').replace(')', '')

data = Data([
    Scattermapbox(
        lat=cityLatLong['lat'],
        lon=cityLatLong['long'],
        mode='markers',
        marker=Marker(
            size=8,
            color = cityLatLong['color']
        ),
        hoverinfo='text',
        text=cityLatLong['city'].str.capitalize(),
    )
])
layout = Layout(
    autosize=False,
    hovermode='closest',
    width=830,
    height=935,
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

#def generateInitialMap():
    


def generateInitialTable():
    value_vs_rest=pd.DataFrame([lt.groupby(5)[4].sum()] ).T
    value_vs_rest.loc['K.Totaal'] = sum(value_vs_rest[4])
    valueWithLeerlingen = value_vs_rest[4]
    trace = go.Table(
    columnwidth = [20]+[8],
    header=dict(values=['Oplossing', "Leerlingen"],
                line = dict(color='#7D7F80'),
                fill = dict(color='#a1c3d1'),
                align = ['left', 'right']),
    cells=dict(values=[[x[2:] for x in value_vs_rest.index],
                       valueWithLeerlingen],
               line = dict(color='#7D7F80'),
               fill = dict(color='#EDFAFF'),
               align = ['left', 'right']))
    layout = dict(width=575, height=700)
    data = [trace]
    return dict(data=data, layout=layout)

def generateLineChart():
    trace1 = go.Scatter(
    x=[2015, 2016, 2017, 2018],
    y=[2, 124, 678, 1824],
    name = 'FTE',
    line = dict(
        color = ('rgb(211,211,211)'),
        width = 3
    ),
    showlegend=False
    )

    trace2 = go.Scatter(
    x=[2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
    y=[1824, 2909, 4053, 4909, 6086, 7378, 8838, 10537],
    line = dict(
        color = ('rgb(255,0,0)'),
        width = 3
    ),
    name="FTE"
    )

    layout = dict(title = 'Verwacht lerarentekort in FTE(voltijd werknemers)',
              xaxis = dict(title = 'Jaren'),
              yaxis = dict(title = 'FTE'),
              )

    data = [trace1, trace2]

    return dict(data=data, layout=layout)

def calculateMarkerColor(dataframe, cityName):
    colors = {
        'A.Klas naar huis sturen': 'rgb(215,48,39)',
        'B.Staking': 'rgb(244,109,67)',
        'C.Onbevoegde voor de klas': 'rgb(253,174,97)',
        'D.Klas verdelen':'rgb(254,224,139)',
        'E.Parttimer komt extra dag terug': 'rgb(217,239,139)',
        'F.Directie of IB-er etc...':'rgb(166,217,106)',
        'G.Ouder met lesbevoegdheid voor de klas':'rgb(102,189,99)',
        'H.Gepensioneerde voor de klas':'rgb(26,152,80)',
        'I.Invaller via detacheringsbureau':'rgb(18,106,56)',
        'J.Anders of combinatie':'rgb(220,220,220)' }

    lt_value=dataframe[dataframe[2].str.contains(cityName)]
    value_vs_rest=pd.DataFrame([lt_value.groupby(5)[4].sum()] ).T
    color='rgb(0,0,0)'
    if value_vs_rest.size:
        color = colors[value_vs_rest.idxmax()[4]]
    return color


def generateInitialBarChart():
    ams_vs_rest=pd.DataFrame([lt[5].value_counts()]).T
    ams_vs_rest.columns=['Nederland']
    ams_vs_rest.index.name='Oplossing'
    ams_vs_rest = ams_vs_rest.sort_index()
    trace1 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][0]) * 100), 2)],
    name=ams_vs_rest.index[0][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(215,48,39, 0.6)',
        line = dict(
            color = 'rgba(215,48,39, 1.0)',
            width = 3)
    )
    )

    trace2 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][1]) * 100), 2)],
    name=ams_vs_rest.index[1][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(244,109,67, 0.6)',
        line = dict(
            color = 'rgba(244,109,67, 1.0)',
            width = 3)
    )
    )

    trace3 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][2]) * 100), 2)],
    name=ams_vs_rest.index[2][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(253,174,97, 0.6)',
        line = dict(
            color = 'rgba(253,174,97, 1.0)',
            width = 3)
    )
    )

    trace4 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][3]) * 100), 2)],
    name=ams_vs_rest.index[3][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(254,224,139, 0.6)',
        line = dict(
            color = 'rgba(254,224,139, 1.0)',
            width = 3)
    )
    )

    trace5 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][4]) * 100), 2)],
    name=ams_vs_rest.index[4][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(217,239,139, 0.6)',
        line = dict(
            color = 'rgba(217,239,139, 1.0)',
            width = 3)
    )
    )

    trace6 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][5]) * 100), 2)],
    name=ams_vs_rest.index[5][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(166,217,106, 0.6)',
        line = dict(
            color = 'rgba(166,217,106, 1.0)',
            width = 3)
    )
    )

    trace7 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][6]) * 100), 2)],
    name=ams_vs_rest.index[6][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(102,189,99, 0.6)',
        line = dict(
            color = 'rgba(102,189,99, 1.0)',
            width = 3)
    )
    )

    trace8 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][7]) * 100), 2)],
    name=ams_vs_rest.index[7][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(26,152,80, 0.6)',
        line = dict(
            color = 'rgba(26,152,80, 1.0)',
            width = 3)
    )
    )

    trace9 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][8]) * 100), 2)],
    name=ams_vs_rest.index[8][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(18,106,56, 0.6)',
        line = dict(
            color = 'rgba(18,106,56, 1.0)',
            width = 3)
    )
    )

    trace10 = go.Bar(
    y=['Nederland'],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][9]) * 100), 2)],
    name=ams_vs_rest.index[9][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(220,220,220, 0.6)',
        line = dict(
            color = 'rgba(220,220,220, 1.0)',
            width = 3)
    )
    )

    data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10]
    layout = go.Layout(
        barmode='stack',
        legend=dict(
            traceorder='normal'
        ),
        title = 'Verdeling in procenten',
        xaxis=dict(
            ticksuffix="%"
        )
    )
    return go.Figure(data=data, layout=layout)

app.layout = html.Div([
    dcc.Markdown('''
# Lerarentekort primair onderwijs

In heel Nederland is er een tekort aan leraren voor het primair onderwijs. In 2018 gaat het volgens de Rijksoverheid om een **tekort** van **1824 full-time leraren** en directeuren. Dit tekort komt voornamelijk door de **hoge werkdruk** en het relatief **lage salaris**. Door de snelle bevolkingsgroei is het probleem in de steden in de Randstad het grootst. Zo heeft Amsterdam volgend schooljaar een verwacht docententekort van 1.6% (Rijksoverheid, 2018).

De kaart hieronder laat met behulp van kleur zien hoe groot het verwachtte lerarentekort per regio in 2020 is. 

![Image](https://www.rijksoverheid.nl/binaries/medium/content/gallery/rijksoverheid/content-afbeeldingen/onderwerpen/werken-in-het-onderwijs/vacaturedruk-po-kaart.png)

## Gevolgen lerarentekort in 2018

Het kan voorkomen dat een leraar door bijv. ziekte onverhoopt niet voor zijn klas kan staan. Door het lerarentekort is er in dit geval helaas vaak **geen vervangende docent beschikbaar**. Daarom moet er gekozen worden voor oplossingen zoals het naar huis sturen van de klas of het laten doceren door een onbevoegde. Om de gevolgen van het probleem in kaart te brengen zijn dit soort situaties in 2018 door scholen bijgehouden. 

Hieronder kan je deze **data interactief verkennen**. De gekleurde bolletjes op de kaart links staan voor de Nederlandse steden, **klik** op een bolletje om de statistieken van een stad te bekijken. De kleuren van de bolletjes komen overeen met de staaf grafiek rechts en laten zien wat de **meeste voorkomende oplossing** in die stad is. Je kan de maanden die je mee wilt nemen in de visualisatie aanpassen met de **slider** bovenaan.

Rechts bovenin zie je een tabel die de specifieke aantallen laat zien. Rechts onderin zie je een staaf grafiek die laat zien hoe de oplossingen in de stad en in de rest van Nederland verdeeld zijn. **Hover** met de muis over de staaf grafiek om de precieze procenten te zien. Door te slepen en klikken kan je de grafiek aanpassen.''', className='container',
    containerProps={'style': {'maxWidth': '650px'}}),
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
             figure = fig,
                 config={
        'displayModeBar': False
    }),
    html.Div([
        html.H2("Nederland", id='stad'),
        html.Button('Toon Nederland', id='my-button'),
        dcc.Graph(id='my-table',
            figure = generateInitialTable(),
                config={
        'displayModeBar': False
    }),
        dcc.Graph(id='my-bar-chart',
            figure = generateInitialBarChart(),
                config={
        'displayModeBar': False
    })
    ], style={'float': 'right'}),
    html.Div([
    html.H2("Toename tekort", style={'margin-top': '80px'}),
    dcc.Markdown('''Zoals duidelijk wordt uit bovenstaande interactieve visualisatie zijn er nu al veel negatieve gevolgen van het lerarentekort. Er wordt echter voorspelt dat als we de huidige koers blijven varen het **lerarentekort** en de bijbehorende **problemen** alleen maar **groter worden**.'''),
    dcc.Markdown('''**Hover** met de muis over onderstaande grafiek om de verwachtingen te zien.'''),
    dcc.Graph(id="line-chart",
            figure=generateLineChart(),
            config={
        'displayModeBar': False
    }),
    dcc.Markdown('''Het lerarentekort wordt voornamelijk veroorzaakt door te **weinig loon** en een **hoge werkdruk**. Goed onderwijs is een van de pijlers van de samenleving en daarom is een **betere CAO** voor docenten in het primair onderwijs hard nodig!'''),
    ], className='container', style={'maxWidth': '650px'}
    )
])

@app.callback(  
    Output(component_id='stad', component_property='children'),
    [Input(component_id='my-map', component_property='clickData'),
    Input(component_id='my-button', component_property='n_clicks')],
    [State('stad', 'children')])
def update_dingen(value, joe, stad):
    if stad == value['points'][0]['text']:
        title = "Nederland"
    else:
        title = value['points'][0]['text']
    return title



@app.callback(  
    Output(component_id='my-table', component_property='figure'),
    [Input(component_id='my-map', component_property='clickData'),
    Input(component_id='my-slider', component_property='value'),
    Input(component_id='my-button', component_property='n_clicks')],
    [State('stad', 'children')])
def update_output_div(input_value, slider, button, stad):
    timeFixed = lt[(lt[0]>=datetime.date(2018, slider[0] ,1)) & (lt[0]<datetime.date(2018 ,slider[1]+1 ,1))]
    if(input_value==None or stad==input_value['points'][0]['text']):
        lt_value=timeFixed
        cityName="Nederland"
    else:
        cityName = input_value['points'][0]['text'].lower()
        lt_value=timeFixed[timeFixed[2].str.contains(cityName)]

    value_vs_rest=pd.DataFrame([lt_value.groupby(5)[4].sum()] ).T
    value_vs_rest.loc['K.Totaal'] = sum(value_vs_rest[4])
    valueWithLeerlingen = value_vs_rest[4]
    trace = go.Table(
    columnwidth = [20]+[8],
    header=dict(values=['Oplossing', 'Leerlingen'],
                line = dict(color='#7D7F80'),
                fill = dict(color='#a1c3d1'),
                align = ['left', 'right']),
    cells=dict(values=[[x[2:] for x in value_vs_rest.index],
                       valueWithLeerlingen],
               line = dict(color='#7D7F80'),
               fill = dict(color='#EDFAFF'),
               height = 25,
               align = ['left', 'right']))
    layout = dict(width=575, height=700)
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
            size=8,
            color=[calculateMarkerColor(timeFilteredDF, x) for x in list(uniqueTimeFilteredDF['city'])]
        ),
        hoverinfo='text',
        text=uniqueTimeFilteredDF['city'].str.capitalize(),
    )
    ])
    layout = Layout(
        autosize=False,
        hovermode='closest',
        width=830,
        # title="Hover over stad om details te tonen",
        height=935,
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
    [Input(component_id='my-map', component_property='clickData'),
    Input(component_id='my-slider', component_property='value')])
def update_bar_chart(input_value, slider):
    timeFixed = lt[(lt[0]>=datetime.date(2018, slider[0] ,1)) & (lt[0]<datetime.date(2018 ,slider[1]+1 ,1))]
    cityName = input_value['points'][0]['text'].lower()
    lt_city=timeFixed[timeFixed[2].str.contains(cityName)]
    lt_not_city=timeFixed[~timeFixed[2].str.contains(cityName)]
    ams_vs_rest=pd.DataFrame([lt_not_city[5].value_counts(),lt_city[5].value_counts()] ).T
    ams_vs_rest.columns=['Nederland', cityName]
    ams_vs_rest.index.name='Oplossing'


    trace1 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][0]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][0]) * 100), 2)],
    name=ams_vs_rest.index[0][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(215,48,39, 0.6)',
        line = dict(
            color = 'rgba(215,48,39, 1.0)',
            width = 3)
    )
    )

    trace2 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][1]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][1]) * 100), 2)],
    name=ams_vs_rest.index[1][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(244,109,67, 0.6)',
        line = dict(
            color = 'rgba(244,109,67, 1.0)',
            width = 3)
    )
    )

    trace3 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][2]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][2]) * 100), 2)],
    name=ams_vs_rest.index[2][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(253,174,97, 0.6)',
        line = dict(
            color = 'rgba(253,174,97, 1.0)',
            width = 3)
    )
    )

    trace4 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][3]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][3]) * 100), 2)],
    name=ams_vs_rest.index[3][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(254,224,139, 0.6)',
        line = dict(
            color = 'rgba(254,224,139, 1.0)',
            width = 3)
    )
    )

    trace5 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][4]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][4]) * 100), 2)],
    name=ams_vs_rest.index[4][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(217,239,139, 0.6)',
        line = dict(
            color = 'rgba(217,239,139, 1.0)',
            width = 3)
    )
    )

    trace6 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][5]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][5]) * 100), 2)],
    name=ams_vs_rest.index[5][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(166,217,106, 0.6)',
        line = dict(
            color = 'rgba(166,217,106, 1.0)',
            width = 3)
    )
    )

    trace7 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][6]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][6]) * 100), 2)],
    name=ams_vs_rest.index[6][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(102,189,99, 0.6)',
        line = dict(
            color = 'rgba(102,189,99, 1.0)',
            width = 3)
    )
    )

    trace8 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][7]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][7]) * 100), 2)],
    name=ams_vs_rest.index[7][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(26,152,80, 0.6)',
        line = dict(
            color = 'rgba(26,152,80, 1.0)',
            width = 3)
    )
    )

    trace9 = go.Bar(
    y=['Nederland', cityName.title()],
    x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][8]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][8]) * 100), 2)],
    name=ams_vs_rest.index[8][2:],
    orientation = 'h',
    marker = dict(
        color = 'rgba(18,106,56, 0.6)',
        line = dict(
            color = 'rgba(18,106,56, 1.0)',
            width = 3)
    )
    )

    try:
        trace10 = go.Bar(
        y=['Nederland', cityName.title()],
        x=[round((((ams_vs_rest/ams_vs_rest.sum())["Nederland"][9]) * 100), 2), round((((ams_vs_rest/ams_vs_rest.sum())[cityName][9]) * 100), 2)],
        name=ams_vs_rest.index[9][2:],
        orientation = 'h',
        marker = dict(
            color = 'rgba(220,220,220, 0.6)',
            line = dict(
                color = 'rgba(220,220,220, 1.0)',
                width = 3)
        )
        )
        data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10]
    except:
        data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9]

    

    layout = go.Layout(
        barmode='stack',
        title = 'Verdeling oplossingen in procenten',
        legend=dict(
            traceorder='normal'
        ),
        xaxis=dict(
            ticksuffix="%"
        )
    )
    return go.Figure(data=data, layout=layout)



    

app.css.append_css({
    'external_url': 'https://codepen.io/rens/pen/dKRZOo.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)