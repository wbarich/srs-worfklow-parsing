from graphviz import Digraph
from IPython.display import display

def render_graph(nodes):
    dot = Digraph(comment='Cafeteria Ordering System Process Flow')
    dot.attr(rankdir='LR')  # Set the direction from Left to Right

    # Add nodes and edges to the graph
    for node_pair in nodes:
        node_pair[0] = node_pair[0].replace(":", "_")
        node_pair[1] = node_pair[1].replace(":", "_")
        dot.node(node_pair[0], node_pair[0])
        dot.node(node_pair[1], node_pair[1])
        dot.edge(node_pair[0], node_pair[1])

    display(dot)
    
