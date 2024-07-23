import dash
from layout.main_layout import get_layout
from callbacks.mysql_callbacks import register_callbacks as register_mysql_callbacks
from callbacks.mongodb_callbacks import register_callbacks as register_mongo_callbacks
from callbacks.neo4j_callbacks import register_callbacks as register_neo4j_callbacks

app = dash.Dash(__name__, title='Research Nexus')

# Set layout
app.layout = get_layout()

# Register callbacks
register_mysql_callbacks(app)
register_mongo_callbacks(app)
register_neo4j_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=False, port=61443)
