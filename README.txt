\* Welcome! Following work is property of 
\* Abhinav Garg (14013) and Anuj Nagpal (14116).
\* You may use, distribute and modify this
\* code under the terms of the XYZ license,
\* which unfortunately won't be written for
\* another century :P

DESCRIPTION
    Milestone 1 - Java scanner and  parser written in python which outputs the syntax tree in a graphical form.
                  To draw the trees, we have used pydot package.
    Milestone 2 - Java Abstract Syntax Tree and Symbol Table Implementation. Tells some basic compilation errors also.

USAGE
    Milestone 1 : ./bin/go.py [options][-d/-s/-e/-f/-h/-l/-z/-t] [string]
    Milestone 2 : ./bin/milestone2.py

OPTIONS
[For ./bin/go.py]
    -d, --debug
        To print debugging statements while parsing. Set value 0 to disable and 1 to enable
    -e, --expression
        To parse the given input expression and generate syntax tree in file "expression_tree.png"
    -f, --file
        To parse the given input file and generate syntax tree in file "file_tree.png"
    -h, --help
        To display this readme file
    -l, --lexfile
        To generate all lex tokens for given input file
    -s, --string
        To parse the given input string and generate syntax tree in file "string_tree.png"
    -t, --statement
        To parse the given input statement and generate syntax tree in file "statement_tree.png"
    -z, --lexstring
        To generate all lex tokens for given input string

SAMPLE COMMAND
[For ./bin/go.py]
    ./bin/go.py -d 1 -f ./test/test.java
    
    This will generate syntax tree for the java code in test.java file in test directory and output the graph in "file_tree.png".
    -d 1 will print the debugging statements.

FILES
    Makefile - The usual makefile to clean all png files and display this readme on terminal
    /src - Contains all source files
    /bin - Binaries are built in this directory
    /tests - Contains testcases

REFERENCES
    https://github.com/musiKk/plyj
    https://github.com/antlr/antlr4
    http://cui.unige.ch/isi/bnf/JAVA/BNFidxkw.html
    https://docs.oracle.com/javase/specs/jls/se7/html/jls-3.html
