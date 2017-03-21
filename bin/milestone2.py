#!/usr/bin/python
import sys
sys.path.insert(0, './src/')
import lexRule
import parser
import ply.lex as lex
import ply.yacc as yacc
import node_file
import csv
import getopt
from PIL import Image

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"f:h",["file=","help"])
    except getopt.GetoptError:
        print 'Usage : ./bin/milestone2.py [options][-f/-h] [filename]'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-f", "--file"):
            parse = parser.Parser()
            tree = parse.parse_file(file(arg))
            parser.printing()
            print("\nAST in txt format:")
            print(tree)
            f = open('AST.txt', 'w')
            print >> f, tree
            f.close()
            print("\nSymbol Table:")
            print(parser.ST.SymbolTable)
            img = Image.open('AST.png')
            #img.show()
            print("\nSymbol Table Dump Written on ST.csv\nAST written in txt format on AST.txt\nAST dot output written on AST.png")
            with open('ST.csv', 'wb') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["function","variable","modifiers","type","dimension"])
                for a in parser.ST.SymbolTableFunction:
                     for b in parser.ST.SymbolTableFunction[a]['variables']:
                             writer.writerow([a , b, parser.ST.SymbolTableFunction[a]['variables'][b]['modifiers'],parser.ST.SymbolTableFunction[a]['variables'][b]['type'],parser.ST.SymbolTableFunction[a]['variables'][b]['dimension']])
        elif opt in ("-h", "--help"):
            _file = open("./README.txt")
            content = _file.read()
            print(content)
        else:
            print 'Usage : ./bin/milestone2.py [options][-f/-h/] [filename]'
            sys.exit(2)
    if not opts:
        print 'Usage : ./bin/milestone2.py [options][-f/-h] [filename]'
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
