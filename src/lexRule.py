# This contains lexing rules

#list of keywords
keywords = ('abstract','based','continue','for','new','switch','default','if','package','synchronized',
        'boolean','do','goto','private','this',
        'break','double','implements','protected','throw',
        'byte','else','import','public',
        'case','instanceof','return','transient',
        'catch','extends','int','short','try',
        'char','final','interface','static','void',
        'class','finally','long','strictfp','volatile',
        'float','native','super','while','assert','const',
        'enum','true','false','null','throws')

#list of tokens
tokens = [ 'NAME','NUM',
        'CHAR_LITERAL',
        'STRING_LITERAL',
        'LINE_COMMENT', 'BLOCK_COMMENT',
        'OR', 'AND',
        'EQ', 'NEQ', 'GTEQ', 'LTEQ' ,
        'LSHIFT','RSHIFT','RRSHIFT',
        'TIMES_ASSIGN','DIVIDE_ASSIGN', 'REMAINDER_ASSIGN',
        'PLUS_ASSIGN' , 'MINUS_ASSIGN' , 'LSHIFT_ASSIGN' , 'RSHIFT_ASSIGN' , 'RRSHIFT_ASSIGN',
        'AND_ASSIGN','OR_ASSIGN','XOR_ASSIGN',
        'PLUSPLUS','MINUSMINUS',
        'ELLIPSIS'
        ] + [w.upper() for w in keywords]

#list of literals
literals = '()+-*/=?:,.^|&~!=[]{};<>@%'

t_NUM = r'\.?[0-9][0-9eE_lLdDa-fA-F.xXpP]*'

t_CHAR_LITERAL = r'\'([^\\\n]|(\\.))*?\''
t_STRING_LITERAL = r'\"([^\\\n]|(\\.))*?\"'

t_ignore_LINE_COMMENT = '//.*'

def t_BLOCK_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

t_OR = r'\|\|'
t_AND = '&&'

t_EQ = '=='
t_NEQ = '!='
t_GTEQ = '>='
t_LTEQ = '<='

t_LSHIFT = '<<'
t_RSHIFT = '>>'
t_RRSHIFT = '>>>'

t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = '/='
t_REMAINDER_ASSIGN = '%='
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = '-='
t_LSHIFT_ASSIGN = '<<='
t_RSHIFT_ASSIGN = '>>='
t_RRSHIFT_ASSIGN = '>>>='
t_AND_ASSIGN = '&='
t_OR_ASSIGN = r'\|='
t_XOR_ASSIGN = '\^='

t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'\-\-'

t_ELLIPSIS = r'\.\.\.'

t_ignore = ' \t\f'

def t_NAME(t):
    '[A-Za-z_$][A-Za-z0-9_$]*'
    if t.value in keywords:
        t.type = t.value.upper()
    return t

    #This is for UNIX based languages
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

    #This is for windows based systems
def t_newline2(t):
    r'(\r\n)+'
    t.lexer.lineno += len(t.value) / 2

def t_error(t):
    print("Illegal character '{}' ({}) in line {}".format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
    t.lexer.skip(1)
