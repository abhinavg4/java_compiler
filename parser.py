import pydot
import node_file as nf
import lexRule

class ExpressionParser(object):
    tokens = lexRule.tokens

    def p_assignment_operator(self, p):
        '''assignment_operator : '='
                               | TIMES_ASSIGN
                               | DIVIDE_ASSIGN
                               | REMAINDER_ASSIGN
                               | PLUS_ASSIGN
                               | MINUS_ASSIGN
                               | LSHIFT_ASSIGN
                               | RSHIFT_ASSIGN
                               | RRSHIFT_ASSIGN
                               | AND_ASSIGN
                               | OR_ASSIGN
                               | XOR_ASSIGN'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_one_child(node_leaf,"assignment_operator")

