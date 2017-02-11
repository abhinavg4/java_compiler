import lexRule
import parser
import ply.lex as lex
import ply.yacc as yacc
import node_file


parse = parser.Parser()

parse.parse_string('class foo{int a;}')
node_file.graph_plot()
