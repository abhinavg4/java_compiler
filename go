import lexRule
import parser
import ply.lex as lex
import ply.yacc as yacc
import node_file


parse = parser.Parser()
parse.parse_string('class Ideone { public static void main(){}}')
node_file.graph_plot()
