#!/usr/bin/python
import sys
sys.path.insert(0, './src/')
import lexRule
import parser
import ply.lex as lex
import ply.yacc as yacc
import node_file
import csv
from PIL import Image

parse = parser.Parser()
tree = parse.parse_file(file('./test/test1.java'))
parser.printing()
print("\nAST in txt format:")
print(tree)
print("\nSymbol Table:")
print(parser.ST.SymbolTable)
img = Image.open('AST.png')
img.show()
print("\nSymbol Table Dump Written on ST.csv")
with open('ST.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["function","variable","modifiers","type","dimension"])
    for a in parser.ST.SymbolTableFunction:
         for b in parser.ST.SymbolTableFunction[a]['variables']:
                 writer.writerow([a , b, parser.ST.SymbolTableFunction[a]['variables'][b]['modifiers'],parser.ST.SymbolTableFunction[a]['variables'][b]['type'],parser.ST.SymbolTableFunction[a]['variables'][b]['dimension']])
