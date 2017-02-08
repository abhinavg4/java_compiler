import ply.lex as lex
import ply.yacc as yacc

class Lexer(object):

    
    keywords = ('abstract','based','continue','for','new','switch','default','if','package','synchronized',
                'boolean','do','goto','private','this',
                'break','double','implements','protected','throw',
                'byte','else','import','public','throws',
                'case','enum','instanceof','return','transient',
                'catch','extends','int','short','try',
                'char','final','interface','static','void',
                'class','finally','long','strictfp','volatile',
                'float','native','super','while','default','assert','const',
                'enum','true','false','null','throws','true','void','volatile')
