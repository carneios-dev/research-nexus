from dash.dependencies import Input, Output
from dash import html
from dash.dash_table import DataTable
from wordcloud import WordCloud
import base64
from io import BytesIO
from utils.frontend.research_interests import random_color
from utils.backend.mongodb import mongo_get_faculty_keywords, mongo_get_publications

def register_callbacks(app):
    @app.callback(
        Output('wordcloud-div', 'children'),
        [Input('faculty-dropdown-2', 'value')]
    )
    def update_widget_three(selected_faculty_id):
        if selected_faculty_id is not None:
            keywords = mongo_get_faculty_keywords(selected_faculty_id)
            wordcloud = WordCloud(width=800, height=400, background_color='#001630', color_func=random_color).generate_from_frequencies(
                {kw['name']: kw['score'] for kw in keywords}
            )
            img = BytesIO()
            wordcloud.to_image().save(img, format='PNG')
            img.seek(0)
            encoded_image = base64.b64encode(img.getvalue()).decode()
            wordcloud_img = html.Img(src=f'data:image/png;base64,{encoded_image}', style={'height': '100%', 'width': '100%'})

            return wordcloud_img
        return None

    @app.callback(
        Output('publication-impact-table', 'children'),
        [Input('faculty-dropdown-3', 'value')]
    )
    def update_widget_four(selected_faculty_id):
        if selected_faculty_id is not None:
            if isinstance(selected_faculty_id, list):
                selected_faculty_id = selected_faculty_id[0]
            
            try:
                selected_faculty_id = int(selected_faculty_id)
            except ValueError:
                return html.Div('Invalid faculty ID selected.')
            
            publications = mongo_get_publications(selected_faculty_id)
            
            table = DataTable(
                columns=[
                    {"name": "Publication Title", "id": "title"},
                    {"name": "Citations", "id": "numCitations"}
                ],
                data=[{"title": pub['title'], "numCitations": pub['numCitations']} for pub in publications],
                sort_action="native",
                style_table={'height': '384px', 'overflowY': 'auto', 'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'whiteSpace': 'normal', 'border': '1px solid #FFA07A'},
                style_header={
                    'backgroundColor': '#001630',
                    'color': '#FFA07A',
                    'fontWeight': 'bold',
                    'font-family': 'Arial, sans-serif',
                    'border': '1px solid #FFA07A'
                },
                style_data={
                    'backgroundColor': '#002855',
                    'color': '#FFA07A',
                    'font-family': 'Arial, sans-serif',
                    'border': '1px solid #FFA07A'
                },
                # Like in `styles.css`, this is a hack to remove the `margin-left: -1px` style that Dash applies.
                css=[{'selector': '.dash-spreadsheet-container .dash-fixed-content', 'rule': 'margin-left: 0 !important;'}]
            )
            
            return html.Div(children=[table])
        return None
