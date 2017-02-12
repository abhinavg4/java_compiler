import sys
sys.path.insert(0, '/home/abhigarg/bitbucket/java_compiler/src/')
import lexRule
import parser
import ply.lex as lex
import ply.yacc as yacc
import node_file
import getopt

def main(argv):
    whatm = ''
    srtingm=''
    try:
        opts, args = getopt.getopt(argv,"w:a:",["what=","string_parse="])
    except getopt.GetoptError:
        print 'go.py -w <what> -a <string>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-w", "--what"):
            whatm = arg
        elif opt in ("-a", "--string_parse"):
            stringm = arg
    if not whatm:
        print 'go.py -w <what> -a <string>'
        sys.exit(2)
    parse = parser.Parser()
    if whatm == "s":
        parse.parse_string(stringm)
    else:
        parse.parse_expression(stringm)
    node_file.graph_plot()

if __name__ == "__main__":
    main(sys.argv[1:])
