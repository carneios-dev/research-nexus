from dash.dependencies import Input, Output
from dash import html
import plotly.graph_objs as go
from utils.backend.mysql import get_faculty_pubs_cites, get_university_pubs_per_year

def register_callbacks(app):
    @app.callback(
        Output('faculty-pub-info', 'children'),
        [Input('faculty-dropdown', 'value')]
    )
    def update_widget_one(selected_faculty):
        if selected_faculty is not None:
            pubs_cites_info = get_faculty_pubs_cites(selected_faculty)
            return html.Div(children=[
                    html.P(f"Faculty Name: {selected_faculty}", className='widget-text'),
                    html.P(f"Publication Count: {pubs_cites_info[0]['publication_count']}", className='widget-text'),
                    html.P(f"Total Citations: {pubs_cites_info[0]['total_citations']}", className='widget-text')
                ])
        return None

    @app.callback(
        Output('university-info', 'figure'),
        [Input('university-dropdown', 'value')]
    )
    def update_widget_two(selected_university):
        if selected_university is not None:
            university_pubs_per_year = get_university_pubs_per_year(selected_university)
            years = [entry['year'] for entry in university_pubs_per_year]
            publication_counts = [entry['publication_count'] for entry in university_pubs_per_year]
            
            figure = {
                'data': [
                    go.Scatter(
                        x=years,
                        y=publication_counts,
                        mode='lines+markers',
                        name='Publications',
                        line=dict(color='#FFA07A', width=2),
                        marker=dict(color='#FFA07A', size=8)
                    )
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Year', 'color': '#FFA07A'},
                    yaxis={'title': 'Number of Publications', 'color': '#FFA07A'},
                    hovermode='closest',
                    plot_bgcolor='#001630',
                    paper_bgcolor='#001630',
                    font=dict(family='Arial, sans-serif', size=12, color='#FFA07A'),
                    title_font=dict(family='Arial, sans-serif', size=20, color='#FFA07A', weight='bold'),
                    margin=dict(l=40, r=40, t=64, b=40),
                )
            }
            return figure
        return {
            'data': [],
            'layout': go.Layout(
                xaxis={'title': 'Year', 'color': '#FFA07A'},
                yaxis={'title': 'Number of Publications', 'color': '#FFA07A'},
                hovermode='closest',
                plot_bgcolor='#001630',
                paper_bgcolor='#001630',
                font=dict(family='Arial, sans-serif', size=12, color='#FFA07A'),
                title_font=dict(family='Arial, sans-serif', size=20, color='#FFA07A', weight='bold'),
                margin=dict(l=40, r=40, t=64, b=40),
            )
        }
