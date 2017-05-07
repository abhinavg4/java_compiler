#!/usr/bin/python
import sys
import os
sys.path.insert(0, './src/')
import lexRule
import parser
import ply.lex as lex
import ply.yacc as yacc
import node_file
import genAssembly as ga
import getopt
import pydot

def main(argv):
    to_parse = ''
    try:
        opts, args = getopt.getopt(argv,"o:f:h",["opt=","file=","help"])
    except getopt.GetoptError:
        print 'Usage : ./bin/final.py [options][-f/-h/-o] [string]'
        sys.exit(2)
    parse = parser.Parser()
    optjump = 0
    for opt, arg in opts:
        if opt in ("-o", "--opt"):
            if arg == "1":
                optjump = 1
        elif opt in ("-f", "--file"):
            tree = parse.parse_file(file(arg))
            t = parser.tac.code

            q = []
            if optjump == 1:
                for x in range(0,len(t)-1):
                    if t[x][0] == "goto" and t[x+1][3] == t[x][3]:
                        q.append(x)
                for qw in reversed(q):
                    del t[qw]
        
                parser.tac.code = t

            old_target = sys.stdout
            ga.generate()

            sys.stdout = open('output.s', 'w')
            ga.generate()

            sys.stdout = old_target


            print("Run ./a.out for execution")
            # os.system("nasm -f elf32 inout.s")
            # os.system("nasm -f elf32 fileio.s")
            os.system("nasm -f elf32 output.s")
            # os.system("nasm -f elf32 val1.s")
            # os.system("nasm -f elf32 next1.s")
            # os.system("nasm -f elf32 append2.s")
            os.system("gcc -m32 output.o ./bin/inout.o ./bin/fileio.o ./bin/val1.o ./bin/next1.o ./bin/append2.o")
            
        elif opt in ("-h", "--help"):
            _file = open("./README.txt")
            content = _file.read()
            print(content)
        else:
            print 'Usage : ./bin/final.py [options][-f/-h/-o] [string]'
            sys.exit(2)
    if not opts:
        print 'Usage : ./bin/final.py [options][-f/-h/-o] [string]'
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
