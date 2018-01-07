#!/usr/bin/python
import sys
sys.path.insert(0, './src/')
import lexRule
import parser
import ply.lex as lex
import ply.yacc as yacc
import node_file
import genAssembly as ga
parse = parser.Parser()
tree = parse.parse_file(file('./test/ackermann.java'))
t = parser.tac.code
ga.generate()

import getopt
import pydot

def main(argv):
    to_parse = ''
    try:
        opts, args = getopt.getopt(argv,"d:s:e:f:hl:z:t:",["debug=","string=","expression=","file=","help","lexfile=","lexstring=","statement="])
    except getopt.GetoptError:
        print 'Usage : ./bin/go.py [options][-d/-s/-e/-f/-h/-l/-z/-t] [string]'
        sys.exit(2)
    parse = parser.Parser()
    for opt, arg in opts:
        if opt in ("-d", "--debug"):
            if arg == "1":
                node_file.debug = 1
        elif opt in ("-s", "--string"):
            node_file.graph = pydot.Dot(graph_type='digraph',ranksep=0.02,nodesep=0.02,size="8.5,11")
            parse.parse_string(arg)
            node_file.outputfile = "./string_tree.png"
            node_file.graph_plot()
            print("Output printed to file string_tree.png")
        elif opt in ("-e", "--expression"):
            node_file.graph = pydot.Dot(graph_type='digraph',ranksep=0.02,nodesep=0.02,size="8.5,11")
            parse.parse_expression(arg)
            node_file.outputfile = "./expression_tree.png"
            node_file.graph_plot()
            print("Output printed to file expression_tree.png")
        elif opt in ("-f", "--file"):
            node_file.graph = pydot.Dot(graph_type='digraph',ranksep=0.02,nodesep=0.02,size="8.5,11")
            parse.parse_file(file(arg))
            node_file.outputfile = "./file_tree.png"
            node_file.graph_plot()
            print("Output printed to file file_tree.png")
        elif opt in ("-l", "--lexfile"):
            parse.tokenize_file(file(arg))
        elif opt in ("-z", "--lexstring"):
            parse.tokenize_string(arg)
        elif opt in ("-t", "--statement"):
            node_file.graph = pydot.Dot(graph_type='digraph',ranksep=0.02,nodesep=0.02,size="8.5,11")
            parse.parse_statement(arg)
            node_file.outputfile = "./statement_tree.png"
            node_file.graph_plot()
            print("Output printed to file statement_tree.png")
        elif opt in ("-h", "--help"):
            _file = open("./README.txt")
            content = _file.read()
            print(content)
        else:
            print 'Usage : ./bin/go.py [options][-d/-s/-e/-f/-h/-l/-z/-t] [string]'
            sys.exit(2)
    if not opts:
        print 'Usage : ./bin/go.py [options][-d/-s/-e/-f/-h/-l/-z/-t] [string]'
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
