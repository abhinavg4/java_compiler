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
tree = parse.parse_file(file('./test/linked_list_search.java'))
t = parser.tac.code

q = []
optjump = 1
if optjump == 1:
    for x in range(0,len(t)-1):
        if t[x][0] == "goto" and t[x+1][3] == t[x][3]:
            q.append(x)
    for qw in reversed(q):
        del t[qw]

    parser.tac.code = t

#for i in t:
#   print i

old_target = sys.stdout
ga.generate()

sys.stdout = open('output.s', 'w')
ga.generate()

sys.stdout.close()

os.system("nasm -f elf32 inout.s")
os.system("nasm -f elf32 fileio.s")
os.system("nasm -f elf32 output.s")
os.system("nasm -f elf32 val1.s")
os.system("nasm -f elf32 next1.s")
os.system("nasm -f elf32 append2.s")
os.system("gcc -m32 output.o inout.o fileio.o val1.o next1.o append2.o")
os.system("./a.out")
