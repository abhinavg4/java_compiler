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

def node_four_child(graph,a,b,c,d,value_e):
    node_e = pydot.Node(value_e)
    graph.add_node(node_e)
    graph.add_edge(pydot.Edge(node_e,a))
    graph.add_edge(pydot.Edge(node_e,b))
    graph.add_edge(pydot.Edge(node_e,c))
    graph.add_edge(pydot.Edge(node_e,d))

def node_five_child(graph,a,b,c,d,e,value_f):
    node_f = pydot.Node(value_f)
    graph.add_node(node_f)
    graph.add_edge(pydot.Edge(node_f,a))
    graph.add_edge(pydot.Edge(node_f,b))
    graph.add_edge(pydot.Edge(node_f,c))
    graph.add_edge(pydot.Edge(node_f,d))
    graph.add_edge(pydot.Edge(node_f,e))
