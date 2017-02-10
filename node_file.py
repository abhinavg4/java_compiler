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

def node_six_child(a,b,c,d,e,f,value_g):
    node_g = pydot.Node(value_g)
    graph.add_node(node_g)
    graph.add_edge(pydot.Edge(node_g,a))
    graph.add_edge(pydot.Edge(node_g,b))
    graph.add_edge(pydot.Edge(node_g,c))
    graph.add_edge(pydot.Edge(node_g,d))
    graph.add_edge(pydot.Edge(node_g,e))
    graph.add_edge(pydot.Edge(node_g,f))
    return node_g

def node_seven_child(a,b,c,d,e,f,g,value_h):
    node_h = pydot.Node(value_h)
    graph.add_node(node_h)
    graph.add_edge(pydot.Edge(node_h,a))
    graph.add_edge(pydot.Edge(node_h,b))
    graph.add_edge(pydot.Edge(node_h,c))
    graph.add_edge(pydot.Edge(node_h,d))
    graph.add_edge(pydot.Edge(node_h,e))
    graph.add_edge(pydot.Edge(node_h,f))
    graph.add_edge(pydot.Edge(node_h,g))
    return node_h

def node_eight_child(a,b,c,d,e,f,g,h,value_i):
    node_i = pydot.Node(value_i)
    graph.add_node(node_i)
    graph.add_edge(pydot.Edge(node_i,a))
    graph.add_edge(pydot.Edge(node_i,b))
    graph.add_edge(pydot.Edge(node_i,c))
    graph.add_edge(pydot.Edge(node_i,d))
    graph.add_edge(pydot.Edge(node_i,e))
    graph.add_edge(pydot.Edge(node_i,f))
    graph.add_edge(pydot.Edge(node_i,g))
    graph.add_edge(pydot.Edge(node_i,h))
    return node_i

def graph_plot():
    graph.write_png('example2_graph.png')
