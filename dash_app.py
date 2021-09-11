# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objs as go

import pandas as pd
import numpy as np 
import networkx as nx
import datetime
from datetime import datetime as dt
import re

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Get and mung data 

# read in only columns that are needed
fields = [
    'entity_name','entity_region','entity_sector','entity_ticker',
    'event_group','event','doc_id','doc_title','doc_source','doc_type','entity_country',
    'entity_relevance','entity_sentiment','event_relevance','doc_sentiment',
    'event_sentiment','signal_id','signal_relevance','signal_sentiment',
    'crawled_at','harvested_at','published_at'
    ]

data_file = 'columbia_capstone_fall2020_esg.csv'

data = pd.read_csv(data_file, usecols=fields, nrows=10000)

# format date to utc
data['published_at'] = pd.to_datetime(data['published_at'], format='%Y-%m-%d').astype(str).str[:10]

# list prep for UI drop downs
def get_ordered_list(df, col):
    return sorted(list(set(list(df[col].astype(str)))))

entity_name_list = get_ordered_list(data, 'entity_name')
entity_sector_list = get_ordered_list(data, 'entity_sector')
event_list = get_ordered_list(data, 'event')
doc_title_list = get_ordered_list(data, 'doc_title')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.Br(),
    html.H1(children='Main Title', style={'text-align':'center'}),
    html.H3(children='Sub Title', style={'text-align':'center'}),
    html.Br(),

    html.Div(children='''
        Introduction and context goes here.
    '''),

    html.Br(),

    html.H6(children='Date Range Selector is Included Here'),
    html.P('I limited the date history to 1 year from the current date. The initial range of time is 30 days.'),

    html.Div(children=[
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=dt.today() - datetime.timedelta(730),
            max_date_allowed=dt.today(),
            initial_visible_month=dt.today(),
            end_date=dt.today(),
            start_date=dt.today() - datetime.timedelta(730),
        )
    ]),

    html.H6(children='UI Dropdowns are Included Here'),
    html.P('I put all of these in thier own Html DIV element to make moving them around easier.'),
    html.Br(),

    html.Div(children=[
        html.H5(children='Entity Name'),
        dcc.Dropdown(
            id='entity_name_dropdown',
            options=[{'label': i, 'value': i} for i in entity_name_list],
            value = [],
            multi = True,
            placeholder = 'Search for an Entity Name...'
            )
        ]),

    html.Div(children=[
        html.H5(children='Sector Name'),
        dcc.Dropdown(
            id='entity_sector_dropdown',
            options=[{'label': i, 'value': i} for i in entity_sector_list],
            value = entity_sector_list,
            multi = True,
            placeholder = 'Search for a Sector...'
            )
        ]),

    html.Div(children=[
        html.H5(children='Event Name'),
        dcc.Dropdown(
            id='event_dropdown',
            options=[{'label': i, 'value': i} for i in event_list],
            value = event_list,
            multi = True,
            placeholder = 'Search for an Event...'
            )
        ]),

    #html.Div(children=[
    #    html.H5(children='Document Title'),
    #    dcc.Dropdown(
    #        id='doc_title_dropdown',
    #        options=[{'label': i, 'value': i} for i in doc_title_list],
    #        value = doc_title_list,
    #        multi = True,
    #        placeholder = 'Search for a Document Title...'
    #        )
    #    ]),
        
        html.Div(id = 'network_graph')
])

@app.callback(
    dash.dependencies.Output('network_graph', 'children'),
    [
        dash.dependencies.Input('date-range', 'start_date'),
        dash.dependencies.Input('date-range', 'end_date'),
        dash.dependencies.Input('entity_name_dropdown', 'value'),
        dash.dependencies.Input('entity_sector_dropdown', 'value'),
        dash.dependencies.Input('event_dropdown', 'value'),
    ]
)
def return_network_graph(
    start_date, end_date, entity_name_dropdown, 
    entity_sector_dropdown, event_dropdown):

    s = dt.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
    e = dt.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')

    temp_data = data[
        (data['published_at'].astype(str) >= str(s)) &\
        (data['published_at'].astype(str) <= str(e)) &\
        (data['entity_name'].isin(entity_name_dropdown)) &\
        (data['entity_sector'].isin(entity_sector_dropdown)) &\
        (data['event'].isin(event_dropdown)) &\
        (data['doc_title'].isin(doc_title_list))]
    
    entity_name_nodes = list(temp_data.entity_name.unique())
    entity_sector_nodes = list(temp_data.entity_sector.unique())
    event_nodes = list(temp_data.event.unique())
    doc_title_nodes = list(temp_data.doc_title.unique())

    nodes_list = set(entity_name_nodes  + entity_sector_nodes + event_nodes + doc_title_nodes)

    G = nx.Graph()

    for i in nodes_list:
        G.add_node(i)

    for i,j in temp_data.iterrows():
        G.add_edges_from([(j["event"],j["doc_title"])]) #rls 1
        G.add_edges_from([(j["entity_name"],j["doc_title"])]) #rls 2
        G.add_edges_from([(j["entity_sector"],j["entity_name"])]) #rls 3

    pos = nx.spring_layout(G, k=0.5, iterations=50)

    for n, p in pos.items():
        G.nodes[n]['pos'] = p

    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='RdBu',
            reversescale=True,
            color=[],
            size=15,
            colorbar=dict(
                thickness=10,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=0)))

    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color']+=tuple([len(adjacencies[1])])
        #print(adjacencies[0])
        node_info = adjacencies[0] +' # of connections: '+str(len(adjacencies[1]))
        node_trace['text']+=tuple([node_info])

    fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='<br>ESG KG',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="No. of connections",
                        showarrow=False,
                        xref="paper", yref="paper") ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    return_div = html.Div([dcc.Graph(figure=fig)])

    return return_div


if __name__ == '__main__':
    app.run_server(debug=True)