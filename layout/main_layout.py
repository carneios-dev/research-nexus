from dash import html
from dash import dcc
from utils.backend.mysql import get_faculty, get_universities
from utils.backend.mongodb import mongo_get_faculty
from utils.backend.neo4j import neo4j_get_faculty, neo4j_get_popular_keywords

mongo_faculty_options = mongo_get_faculty()

def get_layout():
    return html.Div(children=[
        html.H1(children='Research Nexus', style={'margin-left': '20px'}),
        html.Div(children=[
            html.Div(children=[
                dcc.Dropdown(
                    id='faculty-dropdown',
                    options=[{'label': faculty['faculty_name'], 'value': faculty['faculty_name']} for faculty in get_faculty()],
                    placeholder='Select a faculty member',
                    style={'color': '#333'}
                ),
                html.H3('Faculty Publication Information', className='card-title'),
                dcc.Loading(
                    id="loading-faculty-pub-info",
                    type="default",
                    className='loading-parent',
                    children=html.Div(id='faculty-pub-info')
                )
            ], id='widget-1', className='widget'),
            html.Div(children=[
                dcc.Dropdown(
                    id='university-dropdown',
                    options=[{'label': university['university_name'], 'value': university['university_name']} for university in get_universities()],
                    placeholder='Select a university',
                    style={'color': '#333'}
                ),
                html.H3('Publications Per Year', className='card-title'),
                dcc.Loading(
                    id="loading-university-info",
                    type="default",
                    className='loading-parent',
                    children=dcc.Graph(id='university-info', style={'margin-top': '20px'})
                )
            ], id='widget-2', className='widget'),
            html.Div(children=[
                dcc.Dropdown(
                    id='faculty-dropdown-2',
                    options=mongo_faculty_options,
                    placeholder='Select a faculty member',
                    style={'color': '#333'}
                ),
                html.H3('Faculty Research Interests', className='card-title'),
                dcc.Loading(
                    id="loading-wordcloud-div",
                    type="default",
                    className='loading-parent',
                    children=html.Div(id='wordcloud-div')
                )
            ], id='widget-3', className='widget'),
            html.Div(children=[
                dcc.Dropdown(
                    id='faculty-dropdown-3',
                    options=mongo_faculty_options,
                    placeholder='Select a faculty member',
                    style={'color': '#333'}
                ),
                html.H3('Publication Impact Analysis', className='card-title'),
                dcc.Loading(
                    id="loading-publication-impact-table",
                    type="default",
                    className='loading-parent',
                    children=html.Div(id='publication-impact-table')
                )
            ], id='widget-4', className='widget'),
            html.Div(children=[
                dcc.Dropdown(
                    id='faculty-dropdown-4',
                    options=neo4j_get_faculty(),
                    placeholder='Select a faculty member',
                    style={'color': '#333'}
                ),
                html.H3('Faculty Collaboration Network', className='card-title'),
                dcc.Loading(
                    id="loading-collab-network",
                    type="default",
                    className='loading-parent',
                    children=dcc.Graph(id='faculty-collab-network')
                )
            ], id='widget-5', className='widget'),
            html.Div(children=[
                dcc.Dropdown(
                    id='keywords-dropdown',
                    options=neo4j_get_popular_keywords(),
                    placeholder='Select a popular keyword',
                    style={'color': '#333'}
                ),
                html.H3('Top Researchers in Key Areas', className='card-title'),
                dcc.Loading(
                    id="loading-popular-keyword-analysis",
                    type="default",
                    className='loading-parent',
                    children=dcc.Graph(id='popular-keyword-analysis-graph')
                )
            ], id='widget-6', className='widget')
        ], id='main')
    ], style={'display': 'flex', 'flexDirection': 'column', 'minHeight': '100vh'})
