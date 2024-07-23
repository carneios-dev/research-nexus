import networkx as nx
import plotly.graph_objs as go

def create_collaboration_network(collab_network):
    if not collab_network:
        return go.Figure(
            data=[],
            layout=go.Layout(
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
        )

    G = nx.Graph()

    for record in collab_network:
        faculty = record["faculty"]
        coauthor = record["coauthor"]
        collaborations = record["collaborations"]
        
        G.add_node(faculty)
        G.add_node(coauthor)
        G.add_edge(faculty, coauthor, weight=collaborations)

    pos = nx.spring_layout(G)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#FF5F05'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_colors = []

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[node for node in G.nodes()],
        hoverinfo='text',
        textposition='top center',
        marker=dict(
            showscale=False,
            colorscale='YlGnBu',
            size=15,
            line_width=2,
            color='#FF5F05'
        ),
        textfont=dict(size=12, color='white')
    )

    for node, adjacencies in G.adjacency():
        node_colors.append(len(adjacencies))

    figure_layout = go.Layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(255,255,255,0)',
        paper_bgcolor='rgba(255,255,255,0)'
    )

    return go.Figure(data=[edge_trace, node_trace], layout=figure_layout)
