import sys
import os
sys.path.insert(0, './src/')
import lexRule
import parser
import ply.lex as lex
import ply.yacc as yacc
import node_file
import genAssembly as ga
parse = parser.Parser()
tree = parse.parse_file(file('./test/test1.java'))
t = parser.tac.code

#for i in t:
#    print i

#old_target = sys.stdout
#ga.generate()

sys.stdout = open('output.s', 'w')
ga.generate()

sys.stdout.close()

os.system("nasm -f elf32 printInt1.s")
os.system("nasm -f elf32 output.s")
os.system("gcc -m32 output.o printInt1.o")
os.system("./a.out")
