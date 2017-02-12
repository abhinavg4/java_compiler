import pydot

global graph
graph = pydot.Dot(graph_type='digraph',ranksep=0.02,nodesep=0.02,size="8.5,11")

id = 0

def node(value_a):
    global id
    id += 1
    node_a = pydot.Node(id,label=value_a,shape="plaintext")
    print(id,value_a)
    graph.add_node(node_a)
    return id

def node_one_child(a,value_b):
    global id
    id += 1
    a = pydot.Node(a)
    print(a)
    node_b = pydot.Node(id,label=value_b,shape="plaintext")
    print(id,value_b)
    graph.add_node(node_b)
    graph.add_edge(pydot.Edge(node_b,a))
    return id


def node_two_child(a,b,value_c):
    global id
    id += 1
    a = pydot.Node(a)
    b = pydot.Node(b)
    print(a)
    print(b)
    node_c = pydot.Node(id,label=value_c,shape="plaintext")
    print(id,value_c)
    graph.add_node(node_c)
    graph.add_edge(pydot.Edge(node_c,a))
    graph.add_edge(pydot.Edge(node_c,b))
    return id

def node_three_child(a,b,c,value_d):
    global id
    id += 1
    a = pydot.Node(a)
    b = pydot.Node(b)
    c = pydot.Node(c)
    print(a)
    print(b)
    print(c)
    node_d = pydot.Node(id,label=value_d,shape="plaintext")
    print(id,value_d)
    graph.add_node(node_d)
    graph.add_edge(pydot.Edge(node_d,a))
    graph.add_edge(pydot.Edge(node_d,b))
    graph.add_edge(pydot.Edge(node_d,c))
    return id

def node_four_child(a,b,c,d,value_e):
    global id
    id += 1
    a = pydot.Node(a)
    b = pydot.Node(b)
    c = pydot.Node(c)
    d = pydot.Node(d)
    print(a)
    print(b)
    print(c)
    print(d)
    node_e = pydot.Node(id,label=value_e,shape="plaintext")
    print(id,value_e)
    graph.add_node(node_e)
    graph.add_edge(pydot.Edge(node_e,a))
    graph.add_edge(pydot.Edge(node_e,b))
    graph.add_edge(pydot.Edge(node_e,c))
    graph.add_edge(pydot.Edge(node_e,d))
    return id

def node_five_child(a,b,c,d,e,value_f):
    global id
    id += 1
    a = pydot.Node(a)
    b = pydot.Node(b)
    c = pydot.Node(c)
    d = pydot.Node(d)
    e = pydot.Node(e)
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    node_f = pydot.Node(id,label=value_f,shape="plaintext")
    print(id,value_f)
    graph.add_node(node_f)
    graph.add_edge(pydot.Edge(node_f,a))
    graph.add_edge(pydot.Edge(node_f,b))
    graph.add_edge(pydot.Edge(node_f,c))
    graph.add_edge(pydot.Edge(node_f,d))
    graph.add_edge(pydot.Edge(node_f,e))
    return id

def node_six_child(a,b,c,d,e,f,value_g):
    global id
    id += 1
    a = pydot.Node(a)
    b = pydot.Node(b)
    c = pydot.Node(c)
    d = pydot.Node(d)
    e = pydot.Node(e)
    f = pydot.Node(f)
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    print(f)
    node_g = pydot.Node(id,label=value_g,shape="plaintext")
    print(id,value_g)
    graph.add_node(node_g)
    graph.add_edge(pydot.Edge(node_g,a))
    graph.add_edge(pydot.Edge(node_g,b))
    graph.add_edge(pydot.Edge(node_g,c))
    graph.add_edge(pydot.Edge(node_g,d))
    graph.add_edge(pydot.Edge(node_g,e))
    graph.add_edge(pydot.Edge(node_g,f))
    return id

def node_seven_child(a,b,c,d,e,f,g,value_h):
    global id
    id += 1
    a = pydot.Node(a)
    b = pydot.Node(b)
    c = pydot.Node(c)
    d = pydot.Node(d)
    e = pydot.Node(e)
    f = pydot.Node(f)
    g = pydot.Node(g)
    node_h = pydot.Node(id,label=value_h,shape="plaintext")
    print(id,value_h)
    graph.add_node(node_h)
    graph.add_edge(pydot.Edge(node_h,a))
    graph.add_edge(pydot.Edge(node_h,b))
    graph.add_edge(pydot.Edge(node_h,c))
    graph.add_edge(pydot.Edge(node_h,d))
    graph.add_edge(pydot.Edge(node_h,e))
    graph.add_edge(pydot.Edge(node_h,f))
    graph.add_edge(pydot.Edge(node_h,g))
    return id

def node_eight_child(a,b,c,d,e,f,g,h,value_i):
    global id
    id += 1
    a = pydot.Node(a)
    b = pydot.Node(b)
    c = pydot.Node(c)
    d = pydot.Node(d)
    e = pydot.Node(e)
    f = pydot.Node(f)
    g = pydot.Node(g)
    h = pydot.Node(h)
    node_i = pydot.Node(id,label=value_i,shape="plaintext")
    print(id,value_i)
    graph.add_node(node_i)
    graph.add_edge(pydot.Edge(node_i,a))
    graph.add_edge(pydot.Edge(node_i,b))
    graph.add_edge(pydot.Edge(node_i,c))
    graph.add_edge(pydot.Edge(node_i,d))
    graph.add_edge(pydot.Edge(node_i,e))
    graph.add_edge(pydot.Edge(node_i,f))
    graph.add_edge(pydot.Edge(node_i,g))
    graph.add_edge(pydot.Edge(node_i,h))
    return id

def node_nine_child(a,b,c,d,e,f,g,h,i,value_j):
    global id
    id += 1
    a = pydot.Node(a)
    b = pydot.Node(b)
    c = pydot.Node(c)
    d = pydot.Node(d)
    e = pydot.Node(e)
    f = pydot.Node(f)
    g = pydot.Node(g)
    h = pydot.Node(h)
    i = pydot.Node(i)
    node_j = pydot.Node(id,label=value_j,shape="plaintext")
    print(id,value_j)
    graph.add_node(node_j)
    graph.add_edge(pydot.Edge(node_j,a))
    graph.add_edge(pydot.Edge(node_j,b))
    graph.add_edge(pydot.Edge(node_j,c))
    graph.add_edge(pydot.Edge(node_j,d))
    graph.add_edge(pydot.Edge(node_j,e))
    graph.add_edge(pydot.Edge(node_j,f))
    graph.add_edge(pydot.Edge(node_j,g))
    graph.add_edge(pydot.Edge(node_j,h))
    graph.add_edge(pydot.Edge(node_j,i))
    return id

def graph_plot():
    graph.write_png('example2_graph.png')
