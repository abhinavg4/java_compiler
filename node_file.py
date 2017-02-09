import pydot

def node_one_child(graph,a,value_b):
    node_b = pydot.Node(value_b)
    graph.add_node(node_b)
    graph.add_edge(pydot.Edge(node_b,a))


def node_two_child(graph,a,b,value_c):
    node_c = pydot.Node(value_c)
    graph.add_node(node_c)
    graph.add_edge(pydot.Edge(node_c,a))
    graph.add_edge(pydot.Edge(node_c,b))

def node_three_child(graph,a,b,c,value_d):
    node_d = pydot.Node(value_d)
    graph.add_node(node_d)
    graph.add_edge(pydot.Edge(node_d,a))
    graph.add_edge(pydot.Edge(node_d,b))
    graph.add_edge(pydot.Edge(node_d,c))
