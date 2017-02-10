import pydot

global graph
graph = pydot.Dot(graph_type='digraph')

def node(value_a):
    node_a = pydot.Node(value_a)
    graph.add_node(node_a)
    return node_a

def node_one_child(a,value_b):
    node_b = pydot.Node(value_b)
    graph.add_node(node_b)
    graph.add_edge(pydot.Edge(node_b,a))
    return node_b


def node_two_child(a,b,value_c):
    node_c = pydot.Node(value_c)
    graph.add_node(node_c)
    graph.add_edge(pydot.Edge(node_c,a))
    graph.add_edge(pydot.Edge(node_c,b))
    return node_c

def node_three_child(a,b,c,value_d):
    node_d = pydot.Node(value_d)
    graph.add_node(node_d)
    graph.add_edge(pydot.Edge(node_d,a))
    graph.add_edge(pydot.Edge(node_d,b))
    graph.add_edge(pydot.Edge(node_d,c))
    return node_d

def node_four_child(a,b,c,d,value_e):
    node_e = pydot.Node(value_e)
    graph.add_node(node_e)
    graph.add_edge(pydot.Edge(node_e,a))
    graph.add_edge(pydot.Edge(node_e,b))
    graph.add_edge(pydot.Edge(node_e,c))
    graph.add_edge(pydot.Edge(node_e,d))
    return node_e

def node_five_child(a,b,c,d,e,value_f):
    node_f = pydot.Node(value_f)
    graph.add_node(node_f)
    graph.add_edge(pydot.Edge(node_f,a))
    graph.add_edge(pydot.Edge(node_f,b))
    graph.add_edge(pydot.Edge(node_f,c))
    graph.add_edge(pydot.Edge(node_f,d))
    graph.add_edge(pydot.Edge(node_f,e))
    return node_f

def graph_plot():
    graph.write_png('example2_graph.png')
