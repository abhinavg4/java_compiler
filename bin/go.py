#!/usr/bin/python
import sys
sys.path.insert(0, '/home/abhigarg/bitbucket/java_compiler/src/')
import lexRule
import parser
import ply.lex as lex
import ply.yacc as yacc
import node_file
import getopt
import pydot

def main(argv):
    to_parse = ''
    try:
        opts, args = getopt.getopt(argv,"d:s:e:f:hl:z:t:",["debug=","string=","expression=","file=","help","lexfile=","lexstring=","statement="])
    except getopt.GetoptError:
        print 'Usage : go.py [options][-d/-s/-e/-f/-h] [string]'
        sys.exit(2)
    parse = parser.Parser()
    for opt, arg in opts:
        if opt in ("-d", "--debug"):
            if arg == "1":
                node_file.debug = 1
        elif opt in ("-s", "--string"):
            node_file.graph = pydot.Dot(graph_type='digraph',ranksep=0.02,nodesep=0.02,size="8.5,11")
            parse.parse_string(arg)
            node_file.outputfile = "/home/abhigarg/bitbucket/java_compiler/string_tree.png"
            node_file.graph_plot()
            print("Output printed to file string_tree.png")
        elif opt in ("-e", "--expression"):
            node_file.graph = pydot.Dot(graph_type='digraph',ranksep=0.02,nodesep=0.02,size="8.5,11")
            parse.parse_expression(arg)
            node_file.outputfile = "/home/abhigarg/bitbucket/java_compiler/expression_tree.png"
            node_file.graph_plot()
            print("Output printed to file expression_tree.png")
        elif opt in ("-f", "--file"):
            node_file.graph = pydot.Dot(graph_type='digraph',ranksep=0.02,nodesep=0.02,size="8.5,11")
            parse.parse_file(file(arg))
            node_file.outputfile = "/home/abhigarg/bitbucket/java_compiler/file_tree.png"
            node_file.graph_plot()
            print("Output printed to file file_tree.png")
        elif opt in ("-l", "--lexfile"):
            parse.tokenize_file(file(arg))
        elif opt in ("-z", "--lexstring"):
            parse.tokenize_string(arg)
        elif opt in ("-t", "--statement"):
            node_file.graph = pydot.Dot(graph_type='digraph',ranksep=0.02,nodesep=0.02,size="8.5,11")
            parse.parse_statement(arg)
            node_file.outputfile = "/home/abhigarg/bitbucket/java_compiler/statement_tree.png"
            node_file.graph_plot()
            print("Output printed to file statement_tree.png")
        elif opt in ("-h", "--help"):
            _file = open("/home/abhigarg/bitbucket/java_compiler/README.txt")
            content = _file.read()
            print(content)
        else:
            print 'Usage : go.py [options][-d/-s/-e/-f/-h] [string]'
            sys.exit(2)
    if not opts:
        print 'Usage : go.py [options][-d/-s/-e/-f/-h] [string]'
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
