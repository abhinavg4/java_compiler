#!/usr/bin/python
import sys
sys.path.insert(0, './src/')
import lexRule
import parser
import ply.lex as lex
import ply.yacc as yacc
import node_file
parse = parser.Parser()
tree = parse.parse_file(file('./test/test1.java'))
parser.printing()
print("AST printed on AST.png")
from PIL import Image
img = Image.open('AST.png')
img.show()
