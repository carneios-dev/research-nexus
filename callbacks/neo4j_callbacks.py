from dash.dependencies import Input, Output
from utils.frontend.collaboration_network import create_collaboration_network
from utils.backend.neo4j import neo4j_get_collaboration_network, neo4j_get_faculty_keyword_analysis
import plotly.graph_objs as go

def register_callbacks(app):
    @app.callback(
        Output('faculty-collab-network', 'figure'),
        [Input('faculty-dropdown-4', 'value')]
    )
    def update_collab_network(selected_faculty):
        if selected_faculty is not None:
            collab_network = neo4j_get_collaboration_network(selected_faculty)
            return create_collaboration_network(collab_network)
        return {
            "data": [],
            "layout": go.Layout(
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='rgba(255,255,255,0)',
                paper_bgcolor='rgba(255,255,255,0)',
                annotations=[{
                    'text': 'No collaborations found for the selected faculty member.',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 20, 'color': 'white'}
                }]
            )
        }

    @app.callback(
        Output('popular-keyword-analysis-graph', 'figure'),
        [Input('keywords-dropdown', 'value')]
    )
    def update_keyword_analysis(selected_keyword):
        if selected_keyword is not None:
            faculty_data = neo4j_get_faculty_keyword_analysis(selected_keyword)
            
            labels = [record['faculty_name'] for record in faculty_data]
            publication_counts = [record['publication_count'] for record in faculty_data]
            
            # Truncate labels if they are too long
            max_label_length = 12
            truncated_labels = [label if len(label) <= max_label_length else label[:max_label_length] + '...' for label in labels]
            
            figure = go.Figure(
                data=[go.Pie(
                    labels=truncated_labels, 
                    values=publication_counts, 
                    textinfo='label+percent',
                    insidetextfont=dict(size=12, color='black'),
                    outsidetextfont=dict(size=12, color='black'),
                    texttemplate='%{label}<br>%{percent}'
                )],
                layout=go.Layout(
                    showlegend=False,
                    margin=dict(b=20, l=5, r=5, t=40),
                    plot_bgcolor='rgba(255,255,255,0)',
                    paper_bgcolor='rgba(255,255,255,0)',
                )
            )
            
            return figure
        return {
            "data": [],
            "layout": go.Layout(
                showlegend=False,
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='rgba(255,255,255,0)',
                paper_bgcolor='rgba(255,255,255,0)',
                annotations=[{
                    'text': 'Please select a keyword to see the analysis.',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 20, 'color': 'white'}
                }]
            )
        }
