import pydot
import node_file as nf
import lexRule
import ply.lex as lex
import ply.yacc as yacc

global tokens

class ExpressionParser(object):

    def p_expression(self, p):
        '''expression : assignment_expression'''
        p[0] = p[1]

    def p_expression_not_name(self, p):
        '''expression_not_name : assignment_expression_not_name'''
        p[0] = p[1]

    def p_assignment_expression(self, p):
        '''assignment_expression : assignment
                                 | conditional_expression'''
        p[0] = p[1]

    def p_assignment_expression_not_name(self, p):
        '''assignment_expression_not_name : assignment
                                          | conditional_expression_not_name'''
        p[0] = p[1]

    def p_assignment(self, p):
        '''assignment : postfix_expression assignment_operator assignment_expression'''
        p[0] = Assignment(p[2],p[1],p[3])
        #Ease: for ease of readiblity we can even do it p[1] p[2] p[3]

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
        p[0] = p[1]

    def p_conditional_expression(self, p):
        '''conditional_expression : conditional_or_expression
                                  | conditional_or_expression '?' expression ':' conditional_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Conditional(p[1],p[3],p[5])

    def p_conditional_expression_not_name(self, p):
        '''conditional_expression_not_name : conditional_or_expression_not_name
                                           | conditional_or_expression_not_name '?' expression ':' conditional_expression
                                           | name '?' expression ':' conditional_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Conditional(p[1],p[3],p[5])

    def one_or_three(self, p, name_of_node):
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = name_of_node(p[2],p[1],p[3])
            #Ease: For ease of reading operator is between operants

    def p_conditional_or_expression(self, p):
        '''conditional_or_expression : conditional_and_expression
                                     | conditional_or_expression OR conditional_and_expression'''
        self.one_or_three(p, ConditionalOr )

    def p_conditional_or_expression_not_name(self, p):
        '''conditional_or_expression_not_name : conditional_and_expression_not_name
                                              | conditional_or_expression_not_name OR conditional_and_expression
                                              | name OR conditional_and_expression'''
        self.one_or_three(p, ConditionalOr )

    def p_conditional_and_expression(self, p):
        '''conditional_and_expression : inclusive_or_expression
                                      | conditional_and_expression AND inclusive_or_expression'''
        self.one_or_three(p, ConditionalAnd )

    def p_conditional_and_expression_not_name(self, p):
        '''conditional_and_expression_not_name : inclusive_or_expression_not_name
                                               | conditional_and_expression_not_name AND inclusive_or_expression
                                               | name AND inclusive_or_expression'''
        self.one_or_three(p, ConditionalAnd)

    def p_inclusive_or_expression(self, p):
        '''inclusive_or_expression : exclusive_or_expression
                                   | inclusive_or_expression '|' exclusive_or_expression'''
        self.one_or_three(p, Or )

    def p_inclusive_or_expression_not_name(self, p):
        '''inclusive_or_expression_not_name : exclusive_or_expression_not_name
                                            | inclusive_or_expression_not_name '|' exclusive_or_expression
                                            | name '|' exclusive_or_expression'''
        self.one_or_three(p, Or )

    def p_exclusive_or_expression(self, p):
        '''exclusive_or_expression : and_expression
                                   | exclusive_or_expression '^' and_expression'''
        self.one_or_three(p, Xor )

    def p_exclusive_or_expression_not_name(self, p):
        '''exclusive_or_expression_not_name : and_expression_not_name
                                            | exclusive_or_expression_not_name '^' and_expression
                                            | name '^' and_expression'''
        self.one_or_three(p, Xor )

    def p_and_expression(self, p):
        '''and_expression : equality_expression
                          | and_expression '&' equality_expression'''
        self.one_or_three(p, And)

    def p_and_expression_not_name(self, p):
        '''and_expression_not_name : equality_expression_not_name
                                   | and_expression_not_name '&' equality_expression
                                   | name '&' equality_expression'''
        self.one_or_three(p, And)

    def p_equality_expression(self, p):
        '''equality_expression : instanceof_expression
                               | equality_expression EQ instanceof_expression
                               | equality_expression NEQ instanceof_expression'''
        self.one_or_three(p, EqualNotEqual )

    def p_equality_expression_not_name(self, p):
        '''equality_expression_not_name : instanceof_expression_not_name
                                        | equality_expression_not_name EQ instanceof_expression
                                        | name EQ instanceof_expression
                                        | equality_expression_not_name NEQ instanceof_expression
                                        | name NEQ instanceof_expression'''
        self.one_or_three(p, EqualNotEqual )

    def p_instanceof_expression(self, p):
        '''instanceof_expression : relational_expression
                                 | instanceof_expression INSTANCEOF reference_type'''
        self.one_or_three(p, InstanceOfExp )

    def p_instanceof_expression_not_name(self, p):
        '''instanceof_expression_not_name : relational_expression_not_name
                                          | name INSTANCEOF reference_type
                                          | instanceof_expression_not_name INSTANCEOF reference_type'''
        self.one_or_three(p, InstanceOfExp )

    def p_relational_expression(self, p):
        '''relational_expression : shift_expression
                                 | relational_expression '>' shift_expression
                                 | relational_expression '<' shift_expression
                                 | relational_expression GTEQ shift_expression
                                 | relational_expression LTEQ shift_expression'''
        self.one_or_three(p, RelationalExp )

    def p_relational_expression_not_name(self, p):
        '''relational_expression_not_name : shift_expression_not_name
                                          | shift_expression_not_name '<' shift_expression
                                          | name '<' shift_expression
                                          | shift_expression_not_name '>' shift_expression
                                          | name '>' shift_expression
                                          | shift_expression_not_name GTEQ shift_expression
                                          | name GTEQ shift_expression
                                          | shift_expression_not_name LTEQ shift_expression
                                          | name LTEQ shift_expression'''
        self.one_or_three(p, RelationalExp )

    def p_shift_expression(self, p):
        '''shift_expression : additive_expression
                            | shift_expression LSHIFT additive_expression
                            | shift_expression RSHIFT additive_expression
                            | shift_expression RRSHIFT additive_expression'''
        self.one_or_three(p, ShiftExp )

    def p_shift_expression_not_name(self, p):
        '''shift_expression_not_name : additive_expression_not_name
                                     | shift_expression_not_name LSHIFT additive_expression
                                     | name LSHIFT additive_expression
                                     | shift_expression_not_name RSHIFT additive_expression
                                     | name RSHIFT additive_expression
                                     | shift_expression_not_name RRSHIFT additive_expression
                                     | name RRSHIFT additive_expression'''
        self.one_or_three(p, ShiftExp )

    def p_additive_expression(self, p):
        '''additive_expression : multiplicative_expression
                               | additive_expression '+' multiplicative_expression
                               | additive_expression '-' multiplicative_expression'''
        self.one_or_three(p, AddSub )

    def p_additive_expression_not_name(self, p):
        '''additive_expression_not_name : multiplicative_expression_not_name
                                        | additive_expression_not_name '+' multiplicative_expression
                                        | name '+' multiplicative_expression
                                        | additive_expression_not_name '-' multiplicative_expression
                                        | name '-' multiplicative_expression'''
        self.one_or_three(p, AddSub )

    def p_multiplicative_expression(self, p):
        '''multiplicative_expression : unary_expression
                                     | multiplicative_expression '*' unary_expression
                                     | multiplicative_expression '/' unary_expression
                                     | multiplicative_expression '%' unary_expression'''
        self.one_or_three(p, MulDivMod )

    def p_multiplicative_expression_not_name(self, p):
        '''multiplicative_expression_not_name : unary_expression_not_name
                                              | multiplicative_expression_not_name '*' unary_expression
                                              | name '*' unary_expression
                                              | multiplicative_expression_not_name '/' unary_expression
                                              | name '/' unary_expression
                                              | multiplicative_expression_not_name '%' unary_expression
                                              | name '%' unary_expression'''
        self.one_or_three(p, MulDivMod )

    def p_unary_expression(self, p):
        '''unary_expression : pre_increment_expression
                            | pre_decrement_expression
                            | '+' unary_expression
                            | '-' unary_expression
                            | unary_expression_not_plus_minus'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Unary(p[1],p[2])

    def p_unary_expression_not_name(self, p):
        '''unary_expression_not_name : pre_increment_expression
                                     | pre_decrement_expression
                                     | '+' unary_expression
                                     | '-' unary_expression
                                     | unary_expression_not_plus_minus_not_name'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Unary( p[1],p[2] )

    def p_pre_increment_expression(self, p):
        '''pre_increment_expression : PLUSPLUS unary_expression'''
        p[0] = Unary('++x',p[2])

    def p_pre_decrement_expression(self, p):
        '''pre_decrement_expression : MINUSMINUS unary_expression'''
        p[0] = Unary('--x',p[2])

    def p_unary_expression_not_plus_minus(self, p):
        '''unary_expression_not_plus_minus : postfix_expression
                                           | '~' unary_expression
                                           | '!' unary_expression
                                           | cast_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Unary(p[1],p[2])

    def p_unary_expression_not_plus_minus_not_name(self, p):
        '''unary_expression_not_plus_minus_not_name : postfix_expression_not_name
                                                    | '~' unary_expression
                                                    | '!' unary_expression
                                                    | cast_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Unary(p[1],p[2])

    def p_postfix_expression(self, p):
        '''postfix_expression : primary
                              | name
                              | post_increment_expression
                              | post_decrement_expression'''
        p[0] = p[1]

    def p_postfix_expression_not_name(self, p):
        '''postfix_expression_not_name : primary
                                       | post_increment_expression
                                       | post_decrement_expression'''
        p[0] = p[1]

    def p_post_increment_expression(self, p):
        '''post_increment_expression : postfix_expression PLUSPLUS'''
        p[0] = Unary('x++', p[1])

    def p_post_decrement_expression(self, p):
        '''post_decrement_expression : postfix_expression MINUSMINUS'''
        p[0] = Unary('x--',p[1])

    def p_primary(self, p):
        '''primary : primary_no_new_array
                   | array_creation_with_array_initializer
                   | array_creation_without_array_initializer'''
        p[0] = p[1]

    def p_primary_no_new_array(self, p):
        '''primary_no_new_array : literal
                                | THIS
                                | class_instance_creation_expression
                                | field_access
                                | method_invocation
                                | array_access'''
        p[0] = p[1]

    def p_primary_no_new_array2(self, p):
        '''primary_no_new_array : '(' name ')'
                                | '(' expression_not_name ')' '''
        p[0] = p[2]

    def p_primary_no_new_array3(self, p):
        '''primary_no_new_array : name '.' THIS
                                | name '.' SUPER'''
        p[1].value = p[1].value + '.' + p[2]
        p[0] = p[1]

    def p_primary_no_new_array4(self, p):
        '''primary_no_new_array : name '.' CLASS
                                | name dims '.' CLASS
                                | primitive_type dims '.' CLASS
                                | primitive_type '.' CLASS'''
        if len(p) == 4:
            node_leaf = nf.node(p[2])
            node_leaf1 = nf.node(p[3])
            p[0] = nf.node_three_child(p[1],node_leaf,node_leaf1,"primary_no_new_array")
        else:
            node_leaf = nf.node(p[3])
            node_leaf1 = nf.node(p[4])
            p[0] = nf.node_four_child(p[1],p[2],node_leaf,node_leaf1, "primary_no_new_array")

    def p_dims_opt(self, p):
        '''dims_opt : dims'''
        p[0] = nf.node_one_child(p[1],"dims_opt")

    def p_dims_opt2(self, p):
        '''dims_opt : empty'''
        node_leaf = nf.node("empty")
        p[0] = nf.node_one_child(node_leaf, "dims_opt")

    def p_dims(self, p):
        '''dims : dims_loop'''
        p[0] = nf.node_one_child(p[1],"dims")

    def p_dims_loop(self, p):
        '''dims_loop : one_dim_loop
                     | dims_loop one_dim_loop'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "dims_loop")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "dims_loop")

    def p_one_dim_loop(self, p):
        '''one_dim_loop : '[' ']' '''
        node_leaf = nf.node("[")
        node_leaf1 = nf.node("]")
        p[0] = nf.node_two_child(node_leaf,node_leaf1,"one_dim_loop")
        # ignore

    def p_cast_expression(self, p):
        '''cast_expression : '(' primitive_type dims_opt ')' unary_expression'''
        node_leaf = nf.node("(")
        node_leaf1 = nf.node(")")
        p[0] = nf.node_five_child(node_leaf,p[2],p[3],node_leaf1,p[5],"cast_expression")

    def p_cast_expression2(self, p):
        '''cast_expression : '(' name type_arguments dims_opt ')' unary_expression_not_plus_minus'''
        node_leaf = nf.node("(")
        node_leaf1 = nf.node(")")
        p[0] = nf.node_six_child(node_leaf,p[2],p[3],p[4],node_leaf1,p[6],"cast_expression")

    def p_cast_expression3(self, p):
        '''cast_expression : '(' name type_arguments '.' class_or_interface_type dims_opt ')' unary_expression_not_plus_minus'''
        node_leaf = nf.node("(")
        node_leaf1 = nf.node(".")
        node_leaf2 = nf.node(")")
        p[0] = nf.node_eight_child(node_leaf,p[2],p[3],node_leaf1,p[5],p[6],node_leaf2,p[8],"cast_expression")

    def p_cast_expression4(self, p):
        '''cast_expression : '(' name ')' unary_expression_not_plus_minus'''
        node_leaf = nf.node("(")
        node_leaf1 = nf.node(")")
        p[0] = nf.node_four_child(node_leaf,p[2],node_leaf1,p[4],"cast_expression")

    def p_cast_expression5(self, p):
        '''cast_expression : '(' name dims ')' unary_expression_not_plus_minus'''
        node_leaf = nf.node("(")
        node_leaf1 = nf.node(")")
        p[0] = nf.node_five_child(node_leaf,p[2],p[3],node_leaf1,p[5],"cast_expression")

class StatementParser(object):

    def p_block(self, p):
        '''block : '{' block_statements_opt '}' '''
        node_leaf = nf.node("{")
        node_leaf1 = nf.node("}")
        p[0] = nf.node_three_child(node_leaf,p[2],node_leaf1,"block")

    def p_block_statements_opt(self, p):
        '''block_statements_opt : block_statements'''
        p[0] = nf.node_one_child(p[1],"block_statements_opt")

    def p_block_statements_opt2(self, p):
        '''block_statements_opt : empty'''
        node_leaf = nf.node("empty")
        p[0] = nf.node_one_child(node_leaf,"block_statements_opt")

    def p_block_statements(self, p):
        '''block_statements : block_statement
                            | block_statements block_statement'''
        if len(p) == 2:
            p[0]=nf.node_one_child(p[1],"block_statements")
        else:
            p[0] = nf.node_two_child(p[1],p[2],"block_statements")

    def p_block_statement(self, p):
        '''block_statement : local_variable_declaration_statement
                           | statement
                           | class_declaration
                           | interface_declaration
                           | annotation_type_declaration
                           | enum_declaration'''
        p[0] = nf.node_one_child(p[1],"block_statement")

    def p_local_variable_declaration_statement(self, p):
        '''local_variable_declaration_statement : local_variable_declaration ';' '''
        node_leaf = nf.node(";")
        p[0] = nf.node_two_child(p[1],node_leaf,"local_variable_declaration_statement")

    def p_local_variable_declaration(self, p):
        '''local_variable_declaration : type variable_declarators'''
        p[0] = nf.node_two_child(p[1],p[2],"local_variable_declaration")

    def p_local_variable_declaration2(self, p):
        '''local_variable_declaration : modifiers type variable_declarators'''
        p[0] = nf.node_three_child(p[1],p[2],p[3],"local_variable_declaration")

    def p_variable_declarators(self, p):
        '''variable_declarators : variable_declarator
                                | variable_declarators ',' variable_declarator'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1],"variable_declarators")
        else:
            node_leaf = nf.node(",")
            p[0] = nf.node_three_child(p[1],node_leaf,p[3],"variable_declarators")

    def p_variable_declarator(self, p):
        '''variable_declarator : variable_declarator_id
                               | variable_declarator_id '=' variable_initializer'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1],"variable_declarator")
        else:
            node_leaf = nf.node("=")
            p[0] = nf.node_three_child(p[1],node_leaf,p[3],"variable_declarator")

    def p_variable_declarator_id(self, p):
        '''variable_declarator_id : NAME dims_opt'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf,p[2],"variable_declarator_id")

    def p_variable_initializer(self, p):
        '''variable_initializer : expression
                                | array_initializer'''
        p[0] = nf.node_one_child(p[1],"variable_initializer")

    def p_statement(self, p):
        '''statement : statement_without_trailing_substatement
                     | labeled_statement
                     | if_then_statement
                     | if_then_else_statement
                     | while_statement
                     | for_statement
                     | enhanced_for_statement'''
        p[0] = nf.node_one_child(p[1],"statement")

    def p_statement_without_trailing_substatement(self, p):
        '''statement_without_trailing_substatement : block
                                                   | expression_statement
                                                   | assert_statement
                                                   | empty_statement
                                                   | switch_statement
                                                   | do_statement
                                                   | break_statement
                                                   | continue_statement
                                                   | return_statement
                                                   | synchronized_statement
                                                   | throw_statement
                                                   | try_statement
                                                   | try_statement_with_resources'''
        p[0] = nf.node_one_child(p[1],"statement_without_trailing_substatement")

    def p_expression_statement(self, p):
        '''expression_statement : statement_expression ';'
                                | explicit_constructor_invocation'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1],"expression_statement")
        else:
            node_leaf = nf.node(";")
            p[0] = nf.node_two_child(p[1],node_leaf,"expression_statement")

    def p_statement_expression(self, p):
        '''statement_expression : assignment
                                | pre_increment_expression
                                | pre_decrement_expression
                                | post_increment_expression
                                | post_decrement_expression
                                | method_invocation
                                | class_instance_creation_expression'''
        p[0] = nf.node_one_child(p[1],"statement_expression")

    def p_comma_opt(self, p):
        '''comma_opt : ','
                     | empty'''
        if p[1] == ',':
            node_leaf = nf.node(",")
            p[0] = nf.node_one_child(node_leaf,"variable_declarators")
        else:
            node_leaf = nf.node("empty")
            p[0] = nf.node_one_child(node_leaf,"variable_declarators")

    def p_array_initializer(self, p):
        '''array_initializer : '{' comma_opt '}' '''
        node_leaf = nf.node("{")
        node_leaf1 = nf.node("}")
        p[0] = nf.node_three_child(node_leaf,p[2],node_leaf1,"array_initializer")

    def p_array_initializer2(self, p):
        '''array_initializer : '{' variable_initializers '}'
                             | '{' variable_initializers ',' '}' '''
        if len(p) == 3:
            node_leaf = nf.node("{")
            node_leaf1 = nf.node("}")
            p[0] = nf.node_three_child(node_leaf,p[2],node_leaf1,"array_initializer")
        else:
            node_leaf = nf.node("{")
            node_leaf1 = nf.node("}")
            node_leaf2 = nf.node(",")
            p[0] = nf.node_four_child(node_leaf,p[2],node_leaf2,node_leaf1,"array_initializer")

    def p_variable_initializers(self, p):
        '''variable_initializers : variable_initializer
                                 | variable_initializers ',' variable_initializer'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1],"variable_initializers")
        else:
            node_leaf = nf.node(",")
            p[0] = nf.node_three_child(p[1],node_leaf,p[2],"variable_initializers")

    def p_method_invocation(self, p):
        '''method_invocation : NAME '(' argument_list_opt ')' '''
        node_leaf1 = nf.node("(")
        node_leaf2 = nf.node(")")
        node_leaf = nf.node(p[1])
        p[0] = nf.node_four_child(node_leaf,node_leaf1,p[3],node_leaf2,"method_invocation")

    def p_method_invocation2(self, p):
        '''method_invocation : name '.' type_arguments NAME '(' argument_list_opt ')'
                             | primary '.' type_arguments NAME '(' argument_list_opt ')'
                             | SUPER '.' type_arguments NAME '(' argument_list_opt ')' '''
        node_leaf = nf.node(".")
        node_leaf1 = nf.node(p[4])
        node_leaf2 = nf.node("(")
        node_leaf3 = nf.node(")")
        if p[1] == "super":
            node_leaf4 = nf.node(p[1])
            p[0] = nf.node_seven_child(node_leaf4,node_leaf,p[3],node_leaf1,node_leaf2,p[6],node_leaf3,"method_invocation")
        else:
            p[0] = nf.node_seven_child(p[1],node_leaf,p[3],node_leaf1,node_leaf2,p[6],node_leaf3,"method_invocation")

    def p_method_invocation3(self, p):
        '''method_invocation : name '.' NAME '(' argument_list_opt ')'
                             | primary '.' NAME '(' argument_list_opt ')'
                             | SUPER '.' NAME '(' argument_list_opt ')' '''
        node_leaf = nf.node(".")
        node_leaf1 = nf.node(p[3])
        node_leaf2 = nf.node("(")
        node_leaf3 = nf.node(")")
        if p[1] == "super":
            node_leaf4 = nf.node(p[1])
            p[0] = nf.node_six_child(node_leaf4,node_leaf,node_leaf1,node_leaf2,p[5],node_leaf3,"method_invocation")
        else:
            p[0] = nf.node_six_child(p[1],node_leaf,node_leaf1,node_leaf2,p[5],node_leaf3,"method_invocation")

    def p_labeled_statement(self, p):
        '''labeled_statement : label ':' statement'''
        node_leaf = nf.node(":")
        p[0] = nf.node_three_child(p[1],node_leaf,p[3],"labeled_statement")

    def p_labeled_statement_no_short_if(self, p):
        '''labeled_statement_no_short_if : label ':' statement_no_short_if'''
        node_leaf = nf.node(":")
        p[0] = nf.node_three_child(p[1],node_leaf,p[3],"labeled_statement_no_short_if")

    def p_label(self, p):
        '''label : NAME'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_one_child(node_leaf,"label")

    def p_if_then_statement(self, p):
        '''if_then_statement : IF '(' expression ')' statement'''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node("(")
        node_leaf2 = nf.node(")")
        p[0] = nf.node_five_child(node_leaf,node_leaf1,p[3],node_leaf2,p[5],"if_then_statement")

    def p_if_then_else_statement(self, p):
        '''if_then_else_statement : IF '(' expression ')' statement_no_short_if ELSE statement'''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node("(")
        node_leaf2 = nf.node(")")
        node_leaf3 = nf.node(p[6])
        p[0] = nf.node_seven_child(node_leaf,node_leaf1,p[3],node_leaf2,p[5],node_leaf3,p[7],"if_then_else_statement")

    def p_if_then_else_statement_no_short_if(self, p):
        '''if_then_else_statement_no_short_if : IF '(' expression ')' statement_no_short_if ELSE statement_no_short_if'''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node("(")
        node_leaf2 = nf.node(")")
        node_leaf3 = nf.node(p[6])
        p[0] = nf.node_seven_child(node_leaf,node_leaf1,p[3],node_leaf2,p[5],node_leaf3,p[7],"if_then_else_statement_no_short_if")

    def p_while_statement(self, p):
        '''while_statement : WHILE '(' expression ')' statement'''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node("(")
        node_leaf2 = nf.node(")")
        p[0] = nf.node_five_child(node_leaf,node_leaf1,p[3],node_leaf2,p[5],"while_statement")

    def p_while_statement_no_short_if(self, p):
        '''while_statement_no_short_if : WHILE '(' expression ')' statement_no_short_if'''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node("(")
        node_leaf2 = nf.node(")")
        p[0] = nf.node_five_child(node_leaf,node_leaf1,p[3],node_leaf2,p[5],"while_statement_no_short_if")

    def p_for_statement(self, p):
        '''for_statement : FOR '(' for_init_opt ';' expression_opt ';' for_update_opt ')' statement'''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node("(")
        node_leaf2 = nf.node(";")
        node_leaf3 = nf.node(";")
        node_leaf4 = nf.node(")")
        p[0] = nf.node_nine_child(node_leaf,node_leaf1,p[3],node_leaf2,p[5],node_leaf3,p[7],node_leaf4,p[9],"for_statement")

    def p_for_statement_no_short_if(self, p):
        '''for_statement_no_short_if : FOR '(' for_init_opt ';' expression_opt ';' for_update_opt ')' statement_no_short_if'''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node("(")
        node_leaf2 = nf.node(";")
        node_leaf3 = nf.node(";")
        node_leaf4 = nf.node(")")
        p[0] = nf.node_nine_child(node_leaf,node_leaf1,p[3],node_leaf2,p[5],node_leaf3,p[7],node_leaf4,p[9],"for_statement_no_short_if")

    def p_for_init_opt(self, p):
        '''for_init_opt : for_init
                        | empty'''
        if not p[1]:
            node_leaf = nf.node("empty")
            p[0] = nf.node_one_child(node_leaf,"for_init_opt")
        else:
            p[0] = nf.node_one_child(p[1],"for_init_opt")

    def p_for_init(self, p):
        '''for_init : statement_expression_list
                    | local_variable_declaration'''
        p[0] = nf.node_one_child(p[1],"for_init")

    def p_statement_expression_list(self, p):
        '''statement_expression_list : statement_expression
                                     | statement_expression_list ',' statement_expression'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1],"statement_expression_list")
        else:
            node_leaf = nf.node(",")
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "statement_expression_list")

    def p_expression_opt(self, p):
        '''expression_opt : expression
                          | empty'''
        if not p[1]:
            node_leaf = nf.node("empty")
            p[0] = nf.node_one_child(node_leaf,"expression_opt")
        else:
            p[0] = nf.node_one_child(p[1],"expression_opt")

    def p_for_update_opt(self, p):
        '''for_update_opt : for_update
                          | empty'''
        if not p[1]:
            node_leaf = nf.node("empty")
            p[0] = nf.node_one_child(node_leaf,"for_update_opt")
        else:
            p[0] = nf.node_one_child(p[1],"for_update_opt")

    def p_for_update(self, p):
        '''for_update : statement_expression_list'''
        p[0] = nf.node_one_child(p[1], "for_update")

    def p_enhanced_for_statement(self, p):
        '''enhanced_for_statement : enhanced_for_statement_header statement'''
        p[0] = nf.node_two_child(p[1], p[2], "enhanced_for_statement")

    def p_enhanced_for_statement_no_short_if(self, p):
        '''enhanced_for_statement_no_short_if : enhanced_for_statement_header statement_no_short_if'''
        p[0] = nf.node_two_child(p[1], p[2], "enhanced_for_statement_no_short_if")

    def p_enhanced_for_statement_header(self, p):
        '''enhanced_for_statement_header : enhanced_for_statement_header_init ':' expression ')' '''
        node_leaf = nf. node(":")
        node_leaf1 = nf.node(")")
        p[0] = nf.node_four_child(p[1], node_leaf, p[3], node_leaf1, "enhanced_for_statement_header")

    def p_enhanced_for_statement_header_init(self, p):
        '''enhanced_for_statement_header_init : FOR '(' type NAME dims_opt'''
        node_leaf = nf.node("(")
        node_leaf1 = nf.node(p[1])
        node_leaf2 = nf.node(p[4])
        p[0] = nf.node_five_child(node_leaf1, node_leaf, p[3], node_leaf2, p[5], "enhanced_for_statement_header_init")

    def p_enhanced_for_statement_header_init2(self, p):
        '''enhanced_for_statement_header_init : FOR '(' modifiers type NAME dims_opt'''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node("(")
        node_leaf2 = nf.node(p[5])
        p[0] = nf.node_six_child(node_leaf, node_leaf1, p[3], p[4], node_leaf2, p[6], "enhanced_for_statement_header_init")

    def p_statement_no_short_if(self, p):
        '''statement_no_short_if : statement_without_trailing_substatement
                                 | labeled_statement_no_short_if
                                 | if_then_else_statement_no_short_if
                                 | while_statement_no_short_if
                                 | for_statement_no_short_if
                                 | enhanced_for_statement_no_short_if'''
        p[0] = nf.node_one_child(p[1],"statement_no_short_if")

    def p_assert_statement(self, p):
        '''assert_statement : ASSERT expression ';'
                            | ASSERT expression ':' expression ';' '''
        if len(p) == 4:
            node_leaf = nf.node(p[1])
            node_leaf1 = nf.node(p[3])
            p[0] = nf.node_three_child(node_leaf, p[2], node_leaf1, "assert_statement")
        else:
            node_leaf = nf.node(p[1])
            node_leaf1 = nf.node(p[3])
            node_leaf2 = nf.node(p[5])
            p[0] = nf.node_five_child(node_leaf, p[2], node_leaf1, p[4], node_leaf2, "assert_statement")

    def p_empty_statement(self, p):
        '''empty_statement : ';' '''
        node_leaf = nf.node(";")
        p[0] = nf.node_one_child(node_leaf,"empty_statement")

    def p_switch_statement(self, p):
        '''switch_statement : SWITCH '(' expression ')' switch_block'''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[2])
        node_leaf2 = nf.node(p[4])
        p[0] = nf.node_five_child(node_leaf, node_leaf1, p[3], node_leaf2, p[5], "switch_statement")

    def p_switch_block(self, p):
        '''switch_block : '{' '}' '''
        node_leaf = nf.node("{")
        node_leaf1 = nf.node("}")
        p[0] = nf.node_two_child(node_leaf, node_leaf1, "switch_block")

    def p_switch_block2(self, p):
        '''switch_block : '{' switch_block_statements '}' '''
        node_leaf = nf.node("{")
        node_leaf1 = nf.node("}")
        p[0] = nf.node_three_child(node_leaf, p[2], node_leaf1, "switch_block")

    def p_switch_block3(self, p):
        '''switch_block : '{' switch_labels '}' '''
        node_leaf = nf.node("{")
        node_leaf1 = nf.node("}")
        p[0] = nf.node_three_child(node_leaf, p[2], node_leaf1, "switch_block")

    def p_switch_block4(self, p):
        '''switch_block : '{' switch_block_statements switch_labels '}' '''
        node_leaf = nf.node("{")
        node_leaf1 = nf.node("}")
        p[0] = nf.node_four_child(node_leaf, p[2], p[3], node_leaf1, "switch_block")

    def p_switch_block_statements(self, p):
        '''switch_block_statements : switch_block_statement
                                   | switch_block_statements switch_block_statement'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "switch_block_statements")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "switch_block_statements")

    def p_switch_block_statement(self, p):
        '''switch_block_statement : switch_labels block_statements'''
        p[0] = nf.node_two_child(p[1], p[2], "switch_block_statement")

    def p_switch_labels(self, p):
        '''switch_labels : switch_label
                         | switch_labels switch_label'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "switch_labels")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "switch_labels")

    def p_switch_label(self, p):
        '''switch_label : CASE constant_expression ':'
                        | DEFAULT ':' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(":")
        if len(p) == 3:
            p[0] = nf.node_two_child(node_leaf, node_leaf1, "switch_label")
        else:
            p[0] = nf.node_three_child(node_leaf, p[2], node_leaf1, "switch_label")

    def p_constant_expression(self, p):
        '''constant_expression : expression'''
        p[0] = nf.node_one_child(p[1], "constant_expression")

    def p_do_statement(self, p):
        '''do_statement : DO statement WHILE '(' expression ')' ';' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[3])
        node_leaf2 = nf.node("(")
        node_leaf3 = nf.node(")")
        node_leaf4 = nf.node(";")
        p[0] = nf.node_seven_child(node_leaf, p[2], node_leaf1, node_leaf2, p[5], node_leaf3, node_leaf4, "do_statement")

    def p_break_statement(self, p):
        '''break_statement : BREAK ';'
                           | BREAK NAME ';' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(";")
        if len(p) == 3:
            p[0] = nf.node_two_child(node_leaf, node_leaf1, "break_statement")
        else:
            node_leaf2 = nf.node(p[2])
            p[0] = nf.node_three_child(node_leaf, node_leaf2, node_leaf1, "break_statement")

    def p_continue_statement(self, p):
        '''continue_statement : CONTINUE ';'
                              | CONTINUE NAME ';' '''
        node_leaf = nf.node(p[1])
        node_leaf1 =nf.node(";")
        if len(p) == 3:
            p[0] = nf.node_two_child(node_leaf, node_leaf1, "continue_statement")
        else:
            node_leaf2 = nf.node(p[2])
            p[0] = nf.node_three_child(node_leaf, node_leaf2, node_leaf1, "continue_statement")

    def p_return_statement(self, p):
        '''return_statement : RETURN expression_opt ';' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[3])
        p[0] = nf.node_three_child(node_leaf, p[2], node_leaf1, "return_statement")

    def p_synchronized_statement(self, p):
        '''synchronized_statement : SYNCHRONIZED '(' expression ')' block'''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node("(")
        node_leaf2 = nf.node(")")
        p[0] = nf.node_five_child(node_leaf, node_leaf1, p[3], node_leaf2, p[5], "synchronized_statement")

    def p_throw_statement(self, p):
        '''throw_statement : THROW expression ';' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(";")
        p[0] = nf.node_three_child(node_leaf, p[2], node_leaf1, "throw_statement")

    def p_try_statement(self, p):
        '''try_statement : TRY try_block catches
                         | TRY try_block catches_opt finally'''
        node_leaf = nf.node(p[1])
        if len(p) == 4:
            p[0] = nf.node_three_child(node_leaf, p[2], p[3], "try_statement")
        else:
            p[0] = nf.node_four_child(node_leaf, p[2], p[3], p[4], "try_statement")

    def p_try_block(self, p):
        '''try_block : block'''
        p[0] = nf.node_one_child(p[1], "try_block")

    def p_catches(self, p):
        '''catches : catch_clause
                   | catches catch_clause'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "catches")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "catches")

    def p_catches_opt(self, p):
        '''catches_opt : catches'''
        p[0] = nf.node_one_child(p[1], "catches_opt")

    def p_catches_opt2(self, p):
        '''catches_opt : empty'''
        node_leaf = nf.node("empty")
        p[0] = nf.node_one_child(node_leaf,"catches_opt")

    def p_catch_clause(self, p):
        '''catch_clause : CATCH '(' catch_formal_parameter ')' block'''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node("(")
        node_leaf2 = nf.node(")")
        p[0] = nf.node_five_child(node_leaf, node_leaf1, p[3], node_leaf2, p[5], "catch_clause")

    def p_catch_formal_parameter(self, p):
        '''catch_formal_parameter : modifiers_opt catch_type variable_declarator_id'''
        p[0] = nf.node_three_child(p[1], p[2], p[3], "catch_formal_parameter")

    def p_catch_type(self, p):
        '''catch_type : union_type'''
        p[0] = nf.node_one_child(p[1], "catch_type")

    def p_union_type(self, p):
        '''union_type : type
                      | union_type '|' type'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "union_type")
        else:
            node_leaf = nf.node("|")
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "union_type")

    def p_try_statement_with_resources(self, p):
        '''try_statement_with_resources : TRY resource_specification try_block catches_opt
                                        | TRY resource_specification try_block catches_opt finally'''
        node_leaf = nf.node(p[1])
        if len(p) == 5:
            p[0] = nf.node_four_child(node_leaf, p[2], p[3], p[4], "try_statement_with_resources")
        else:
            p[0] = nf.node_five_child(node_leaf, p[2], p[3], p[4], p[5], "try_statement_with_resources")

    def p_resource_specification(self, p):
        '''resource_specification : '(' resources semi_opt ')' '''
        node_leaf = nf.node("(")
        node_leaf1 = nf.node(")")
        p[0] = nf.node_three_child(node_leaf, p[2], node_leaf1, "resource_specification")

    def p_semi_opt(self, p):
        '''semi_opt : ';'
                    | empty'''
        if p[1] == ";":
            node_leaf = nf.node(";")
            p[0] = nf.node_one_child(node_leaf, "semi_opt")
        else:
            node_leaf = nf.node("empty")
            p[0] = nf.node_one_child(node_leaf, "semi_opt")
        # ignore

    def p_resources(self, p):
        '''resources : resource
                     | resources trailing_semicolon resource'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "resources")
        else:
            p[0] = nf.node_three_child(p[1], p[2], p[3], "resources")

    def p_trailing_semicolon(self, p):
        '''trailing_semicolon : ';' '''
        node_leaf = nf.node(";")
        p[0] = nf.node_one_child(node_leaf, "trailing_semicolon")
        # ignore

    def p_resource(self, p):
        '''resource : type variable_declarator_id '=' variable_initializer'''
        node_leaf = nf.node("=")
        p[0] = nf.node_four_child(p[1], p[2], node_leaf, p[4], "resource")

    def p_resource2(self, p):
        '''resource : modifiers type variable_declarator_id '=' variable_initializer'''
        node_leaf = nf.node("=")
        p[0] = nf.node_five_child(p[1], p[2], p[3], node_leaf, p[5], "resource")

    def p_finally(self, p):
        '''finally : FINALLY block'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[2], "finally")

    def p_explicit_constructor_invocation(self, p):
        '''explicit_constructor_invocation : THIS '(' argument_list_opt ')' ';'
                                           | SUPER '(' argument_list_opt ')' ';' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node("(")
        node_leaf2 = nf.node(")")
        node_leaf3 = nf.node(";")
        p[0] = nf.node_five_child(node_leaf, node_leaf1, p[3], node_leaf2, node_leaf3, "explicit_constructor_invocation")

    def p_explicit_constructor_invocation2(self, p):
        '''explicit_constructor_invocation : type_arguments SUPER '(' argument_list_opt ')' ';'
                                           | type_arguments THIS '(' argument_list_opt ')' ';' '''
        node_leaf = nf.node(p[2])
        node_leaf1 = nf.node("(")
        node_leaf2 = nf.node(")")
        node_leaf3 = nf.node(";")
        p[0] = nf.node_six_child(p[1], node_leaf, node_leaf1, p[4], node_leaf2, node_leaf3, "explicit_constructor_invocation")

    def p_explicit_constructor_invocation3(self, p):
        '''explicit_constructor_invocation : primary '.' SUPER '(' argument_list_opt ')' ';'
                                           | name '.' SUPER '(' argument_list_opt ')' ';'
                                           | primary '.' THIS '(' argument_list_opt ')' ';'
                                           | name '.' THIS '(' argument_list_opt ')' ';' '''
        node_leaf = nf.node(".")
        node_leaf1 = nf.node(p[3])
        node_leaf2 = nf.node("(")
        node_leaf3 = nf.node(")")
        node_leaf4 = nf.node(";")
        p[0] = nf.node_seven_child(p[1], node_leaf, node_leaf1, node_leaf2, p[5], node_leaf3, node_leaf4, "explicit_constructor_invocation")

    def p_explicit_constructor_invocation4(self, p):
        '''explicit_constructor_invocation : primary '.' type_arguments SUPER '(' argument_list_opt ')' ';'
                                           | name '.' type_arguments SUPER '(' argument_list_opt ')' ';'
                                           | primary '.' type_arguments THIS '(' argument_list_opt ')' ';'
                                           | name '.' type_arguments THIS '(' argument_list_opt ')' ';' '''
        node_leaf = nf.node(".")
        node_leaf1 = nf.node(p[4])
        node_leaf2 = nf.node("(")
        node_leaf3 = nf.node(")")
        node_leaf4 = nf.node(";")
        p[0] = nf.node_eight_child(p[1], node_leaf, p[3], node_leaf1, node_leaf2, p[6], node_leaf3, node_leaf4, "explicit_constructor_invocation")

    def p_class_instance_creation_expression(self, p):
        '''class_instance_creation_expression : NEW type_arguments class_type '(' argument_list_opt ')' class_body_opt'''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node("(")
        node_leaf2 = nf.node(")")
        p[0] = nf.node_seven_child(node_leaf, p[2], p[3], node_leaf1, p[5], node_leaf2, p[7], "class_instance_creation_expression")

    def p_class_instance_creation_expression2(self, p):
        '''class_instance_creation_expression : NEW class_type '(' argument_list_opt ')' class_body_opt'''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node("(")
        node_leaf2 = nf.node(")")
        p[0] = nf.node_six_child(node_leaf, p[2], node_leaf1, p[4], node_leaf2, p[6], "class_instance_creation_expression")

    def p_class_instance_creation_expression3(self, p):
        '''class_instance_creation_expression : primary '.' NEW type_arguments class_type '(' argument_list_opt ')' class_body_opt'''
        node_leaf = nf.node(".")
        node_leaf1 = nf.node(p[3])
        node_leaf2 = nf.node(p[6])
        node_leaf3 = nf.node(p[8])
        p[0] = nf.node_nine_child(p[1], node_leaf, node_leaf1, p[4], p[5], node_leaf2, p[7], node_leaf3, p[9], "class_instance_creation_expression")

    def p_class_instance_creation_expression4(self, p):
        '''class_instance_creation_expression : primary '.' NEW class_type '(' argument_list_opt ')' class_body_opt'''
        node_leaf = nf.node(".")
        node_leaf1 = nf.node(p[3])
        node_leaf2 = nf.node(p[5])
        node_leaf3 = nf.node(p[7])
        p[0] = nf.node_eight_child(p[1], node_leaf, node_leaf1, p[4], node_leaf2, p[6], node_leaf3, p[8], "class_instance_creation_expression")

    def p_class_instance_creation_expression5(self, p):
        '''class_instance_creation_expression : class_instance_creation_expression_name NEW class_type '(' argument_list_opt ')' class_body_opt'''
        node_leaf = nf.node(p[2])
        node_leaf1 = nf.node(p[4])
        node_leaf2 = nf.node(p[6])
        p[0] = nf.node_seven_child(p[1], node_leaf, p[3], node_leaf1, p[5], node_leaf2, p[7], "class_instance_creation_expression")

    def p_class_instance_creation_expression6(self, p):
        '''class_instance_creation_expression : class_instance_creation_expression_name NEW type_arguments class_type '(' argument_list_opt ')' class_body_opt'''
        node_leaf = nf.node(p[2])
        node_leaf1 = nf.node(p[5])
        node_leaf2 = nf.node(p[7])
        p[0] = nf.node_eight_child(p[1], node_leaf, p[3], p[4], node_leaf1, p[6], node_leaf2, p[8], "class_instance_creation_expression")

    def p_class_instance_creation_expression_name(self, p):
        '''class_instance_creation_expression_name : name '.' '''
        node_leaf = nf.node(".")
        p[0] = nf.node_two_child(p[1], node_leaf, "class_instance_creation_expression_name")

    def p_class_body_opt(self, p):
        '''class_body_opt : class_body
                          | empty'''
        if not p[1]:
            node_leaf = nf.node("empty")
            p[0] = nf.node_one_child(node_leaf,"class_body_opt")
        else:
            p[0] = nf.node_one_child(p[1],"class_body_opt")

    def p_field_access(self, p):
        '''field_access : primary '.' NAME
                        | SUPER '.' NAME'''
        node_leaf = nf.node(".")
        node_leaf1 = nf.node(p[3])
        if p[1] == "super":
            node_leaf2 = nf.node(p[1])
            p[0] = nf.node_three_child(node_leaf2, node_leaf, node_leaf1, "field_access")
        else:
            p[0] = nf.node_three_child(p[1], node_leaf, node_leaf1, "field_access")

    def p_array_access(self, p):
        '''array_access : name '[' expression ']'
                        | primary_no_new_array '[' expression ']'
                        | array_creation_with_array_initializer '[' expression ']' '''
        node_leaf = nf.node("[")
        node_leaf1 = nf.node("]")
        p[0] = nf.node_four_child(p[1], node_leaf, p[3], node_leaf1, "array_access")

    def p_array_creation_with_array_initializer(self, p):
        '''array_creation_with_array_initializer : NEW primitive_type dim_with_or_without_exprs array_initializer
                                                 | NEW class_or_interface_type dim_with_or_without_exprs array_initializer'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_four_child(node_leaf, p[2], p[3], p[4], "array_creation_with_array_initializer")

    def p_dim_with_or_without_exprs(self, p):
        '''dim_with_or_without_exprs : dim_with_or_without_expr
                                     | dim_with_or_without_exprs dim_with_or_without_expr'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "dim_with_or_without_exprs")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "dim_with_or_without_exprs")

    def p_dim_with_or_without_expr(self, p):
        '''dim_with_or_without_expr : '[' expression ']'
                                    | '[' ']' '''
        if len(p) == 3:
            node_leaf = nf.node("[")
            node_leaf1 = nf.node("]")
            p[0] = nf.node_two_child(node_leaf, node_leaf1, "dim_with_or_without_expr")
        else:
            node_leaf = nf.node("[")
            node_leaf1 = nf.node("]")
            p[0] = nf.node_three_child(node_leaf, p[2], node_leaf1, "dim_with_or_without_expr")

    def p_array_creation_without_array_initializer(self, p):
        '''array_creation_without_array_initializer : NEW primitive_type dim_with_or_without_exprs
                                                    | NEW class_or_interface_type dim_with_or_without_exprs'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_three_child(node_leaf, p[2], p[3], "array_creation_without_array_initializer")

class NameParser(object):

    def p_name(self, p):
        '''name : simple_name
                | qualified_name'''
        p[0] = nf.node_one_child(p[1],"name")

    def p_simple_name(self, p):
        '''simple_name : NAME'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_one_child(node_leaf,"simple-name")

    def p_qualified_name(self, p):
        '''qualified_name : name '.' simple_name'''
        node_leaf = nf.node(p[2])
        p[0] = nf.node_three_child(p[1], node_leaf, p[3],"qualified_name")

class LiteralParser(object):

    def p_literal(self, p):
        '''literal : NUM
                   | CHAR_LITERAL
                   | STRING_LITERAL
                   | TRUE
                   | FALSE
                   | NULL'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_one_child(node_leaf,"literal")

class TypeParser(object):

    def p_modifiers_opt(self, p):
        '''modifiers_opt : modifiers'''
        p[0] = nf.node_one_child(p[1], "modifiers_opt")

    def p_modifiers_opt2(self, p):
        '''modifiers_opt : empty'''
        node_leaf = nf.node("empty")
        p[0] = nf.node_one_child(node_leaf, "modifiers_opt")

    def p_modifiers(self, p):
        '''modifiers : modifier
                     | modifiers modifier'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1],"modifiers")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "modifiers")

    def p_modifier(self, p):
        '''modifier : PUBLIC
                    | PROTECTED
                    | PRIVATE
                    | STATIC
                    | ABSTRACT
                    | FINAL
                    | NATIVE
                    | SYNCHRONIZED
                    | TRANSIENT
                    | VOLATILE
                    | STRICTFP'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_one_child(node_leaf, "modifier")

    def p_modifier2(self, p):
        '''modifier : annotation'''
        p[0] = nf.node_one_child(p[1], "modifier")

    def p_type(self, p):
        '''type : primitive_type
                | reference_type'''
        p[0] = nf.node_one_child(p[1], "type")

    def p_primitive_type(self, p):
        '''primitive_type : BOOLEAN
                          | VOID
                          | BYTE
                          | SHORT
                          | INT
                          | LONG
                          | CHAR
                          | FLOAT
                          | DOUBLE'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_one_child(node_leaf, "primitive_type")

    def p_reference_type(self, p):
        '''reference_type : class_or_interface_type
                          | array_type'''
        p[0] = nf.node_one_child(p[1], "reference_type")

    def p_class_or_interface_type(self, p):
        '''class_or_interface_type : class_or_interface
                                   | generic_type'''
        p[0] = nf.node_one_child(p[1], "class_or_interface_type")

    def p_class_type(self, p):
        '''class_type : class_or_interface_type'''
        p[0] = nf.node_one_child(p[1], "class_type")

    def p_class_or_interface(self, p):
        '''class_or_interface : name
                              | generic_type '.' name'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "class_or_interface")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "class_or_interface")

    def p_generic_type(self, p):
        '''generic_type : class_or_interface type_arguments'''
        p[0] = nf.node_two_child(p[1], p[2], "generic_type")

    def p_generic_type2(self, p):
        '''generic_type : class_or_interface '<' '>' '''
        node_leaf = nf.node(p[2])
        node_leaf1 = nf.node(p[3])
        p[0] = nf.node_three_child(p[1], node_leaf, node_leaf1, "generic_type")

#    def p_array_type(self, p):
#        '''array_type : primitive_type dims
#                      | name dims
#                      | array_type_with_type_arguments_name dims
#                      | generic_type dims'''
#        p[0] = p[1] + '[' + p[2] + ']'
#
#    def p_array_type_with_type_arguments_name(self, p):
#        '''array_type_with_type_arguments_name : generic_type '.' name'''
#        p[0] = p[1] + '.' + p[3]

    def p_array_type(self, p):
        '''array_type : primitive_type dims
                      | name dims'''
        p[0] = nf.node_two_child(p[1], p[2], "array_type")

    def p_array_type2(self, p):
        '''array_type : generic_type dims'''
        p[0] = nf.node_two_child(p[1], p[2], "array_type")

    def p_array_type3(self, p):
        '''array_type : generic_type '.' name dims'''
        node_leaf = nf.node(p[2])
        p[0] = nf.node_four_child(p[1], node_leaf, p[3], p[4], "array_type")

    def p_type_arguments(self, p):
        '''type_arguments : '<' type_argument_list1'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[2], "type_arguments")

    def p_type_argument_list1(self, p):
        '''type_argument_list1 : type_argument1
                               | type_argument_list ',' type_argument1'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "type_argument_list1")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "type_argument_list1")

    def p_type_argument_list(self, p):
        '''type_argument_list : type_argument
                              | type_argument_list ',' type_argument'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "type_argument_list")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "type_argument_list")

    def p_type_argument(self, p):
        '''type_argument : reference_type
                         | wildcard'''
        p[0] = nf.node_one_child(p[1], "type_argument")

    def p_type_argument1(self, p):
        '''type_argument1 : reference_type1
                          | wildcard1'''
        p[0] = nf.node_one_child(p[1], "type_argument1")

    def p_reference_type1(self, p):
        '''reference_type1 : reference_type '>'
                           | class_or_interface '<' type_argument_list2'''
        if len(p) == 3:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_two_child(p[1], node_leaf, "reference_type1")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "reference_type1")

    def p_type_argument_list2(self, p):
        '''type_argument_list2 : type_argument2
                               | type_argument_list ',' type_argument2'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "type_argument_list2")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "type_argument_list2")

    def p_type_argument2(self, p):
        '''type_argument2 : reference_type2
                          | wildcard2'''
        p[0] = nf.node_one_child(p[1], "type_argument2")

    def p_reference_type2(self, p):
        '''reference_type2 : reference_type RSHIFT
                           | class_or_interface '<' type_argument_list3'''
        if len(p) == 3:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_two_child(p[1], node_leaf, "reference_type2")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "reference_type2")

    def p_type_argument_list3(self, p):
        '''type_argument_list3 : type_argument3
                               | type_argument_list ',' type_argument3'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "type_argument_list3")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "type_argument_list3")

    def p_type_argument3(self, p):
        '''type_argument3 : reference_type3
                          | wildcard3'''
        p[0] = nf.node_one_child(p[1], "type_argument3")

    def p_reference_type3(self, p):
        '''reference_type3 : reference_type RRSHIFT'''
        node_leaf = nf.node(p[2])
        p[0] = nf.node_two_child(p[1], node_leaf, "reference_type3")

    def p_wildcard(self, p):
        '''wildcard : '?'
                    | '?' wildcard_bounds'''
        if len(p) == 2:
            node_leaf = nf.node(p[1])
            p[0] = nf.node_one_child(node_leaf, "wildcard")
        else:
            node_leaf = nf.node(p[1])
            p[0] = nf.node_two_child(node_leaf, p[2], "wildcard")

    def p_wildcard_bounds(self, p):
        '''wildcard_bounds : EXTENDS reference_type
                           | SUPER reference_type'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[2], "wildcard_bounds")

    def p_wildcard1(self, p):
        '''wildcard1 : '?' '>'
                     | '?' wildcard_bounds1'''
        if p[2] == ">":
            node_leaf = nf.node(p[1])
            node_leaf1 = nf.node(p[2])
            p[0] = nf.node_two_child(node_leaf, node_leaf1, "wildcard1")
        else:
            node_leaf = nf.node(p[1])
            p[0] = nf.node_two_child(node_leaf, p[2], "wildcard1")

    def p_wildcard_bounds1(self, p):
        '''wildcard_bounds1 : EXTENDS reference_type1
                            | SUPER reference_type1'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[2], "wildcard_bounds1")

    def p_wildcard2(self, p):
        '''wildcard2 : '?' RSHIFT
                     | '?' wildcard_bounds2'''
        if p[2] == ">>":
            node_leaf = nf.node(p[1])
            node_leaf1 = nf.node(p[2])
            p[0] = nf.node_two_child(node_leaf, node_leaf1, "wildcard2")
        else:
            node_leaf = nf.node(p[1])
            p[0] = nf.node_two_child(node_leaf, p[2], "wildcard2")

    def p_wildcard_bounds2(self, p):
        '''wildcard_bounds2 : EXTENDS reference_type2
                            | SUPER reference_type2'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[2], "wildcard_bounds2")

    def p_wildcard3(self, p):
        '''wildcard3 : '?' RRSHIFT
                     | '?' wildcard_bounds3'''
        if p[2] == ">>>":
            node_leaf = nf.node(p[1])
            node_leaf1 = nf.node(p[2])
            p[0] = nf.node_two_child(node_leaf, node_leaf2, "wildcard3")
        else:
            node_leaf = nf.node(p[1])
            p[0] = nf.node_two_child(node_leaf, p[2], "wildcard3")

    def p_wildcard_bounds3(self, p):
        '''wildcard_bounds3 : EXTENDS reference_type3
                            | SUPER reference_type3'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[2], "wildcard_bounds3")

    def p_type_parameter_header(self, p):
        '''type_parameter_header : NAME'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_one_child(node_leaf, "type_parameter_header")

    def p_type_parameters(self, p):
        '''type_parameters : '<' type_parameter_list1'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[2], "type_parameters")

    def p_type_parameter_list(self, p):
        '''type_parameter_list : type_parameter
                               | type_parameter_list ',' type_parameter'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "type_parameter_list")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "type_parameter_list")

    def p_type_parameter(self, p):
        '''type_parameter : type_parameter_header
                          | type_parameter_header EXTENDS reference_type
                          | type_parameter_header EXTENDS reference_type additional_bound_list'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "type_parameter")
        elif len(p) == 4:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "type_parameter")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_four_child(p[1], node_leaf, p[3], p[4], "type_parameter")

    def p_additional_bound_list(self, p):
        '''additional_bound_list : additional_bound
                                 | additional_bound_list additional_bound'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "additional_bound_list")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "additional_bound_list")

    def p_additional_bound(self, p):
        '''additional_bound : '&' reference_type'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[2], "additional_bound")

    def p_type_parameter_list1(self, p):
        '''type_parameter_list1 : type_parameter1
                                | type_parameter_list ',' type_parameter1'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "type_parameter_list1")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "type_parameter_list1")

    def p_type_parameter1(self, p):
        '''type_parameter1 : type_parameter_header '>'
                           | type_parameter_header EXTENDS reference_type1
                           | type_parameter_header EXTENDS reference_type additional_bound_list1'''
        if len(p) == 3:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_two_child(p[1], node_leaf, "type_parameter1")
        elif len(p) == 4:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "type_parameter1")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_four_child(p[1], node_leaf, p[3], p[4], "type_parameter1")

    def p_additional_bound_list1(self, p):
        '''additional_bound_list1 : additional_bound1
                                  | additional_bound_list additional_bound1'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "additional_bound_list1")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "additional_bound_list1")

    def p_additional_bound1(self, p):
        '''additional_bound1 : '&' reference_type1'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[2], "additional_bound1")

class ClassParser(object):

    def p_type_declaration(self, p):
        '''type_declaration : class_declaration
                            | interface_declaration
                            | enum_declaration
                            | annotation_type_declaration'''
        p[0] = nf.node_one_child(p[1], "type_declaration")

    def p_type_declaration2(self, p):
        '''type_declaration : ';' '''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_one_child(node_leaf, "type_declaration")

    def p_class_declaration(self, p):
        '''class_declaration : class_header class_body'''
        p[0] = nf.node_two_child(p[1], p[2], "class_declaration")

    def p_class_header(self, p):
        '''class_header : class_header_name class_header_extends_opt class_header_implements_opt'''
        p[0] = nf.node_three_child(p[1], p[2], p[3], "class_header")

    def p_class_header_name(self, p):
        '''class_header_name : class_header_name1 type_parameters
                             | class_header_name1'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "class_header_name")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "class_header_name")

    def p_class_header_name1(self, p):
        '''class_header_name1 : modifiers_opt CLASS NAME'''
        node_leaf = nf.node(p[2])
        node_leaf1 = nf.node(p[3])
        p[0] = nf.node_three_child(p[1], node_leaf, node_leaf1, "class_header_name1")

    def p_class_header_extends_opt(self, p):
        '''class_header_extends_opt : class_header_extends
                                    | empty'''
        if not p[1]:
            node_leaf = nf.node("empty")
            p[0] = nf.node_one_child(node_leaf, "class_header_extends_opt")
        else:
            p[0] = nf.node_one_child(p[1], "class_header_extends_opt")

    def p_class_header_extends(self, p):
        '''class_header_extends : EXTENDS class_type'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[1], "class_header_extends")

    def p_class_header_implements_opt(self, p):
        '''class_header_implements_opt : class_header_implements
                                       | empty'''
        if not p[1]:
            node_leaf = nf.node("empty")
            p[0] = nf.node_one_child(node_leaf, "class_header_implements_opt")
        else:
            p[0] = nf.node_one_child(p[1], "class_header_implements_opt")

    def p_class_header_implements(self, p):
        '''class_header_implements : IMPLEMENTS interface_type_list'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[2], "class_header_implements")

    def p_interface_type_list(self, p):
        '''interface_type_list : interface_type
                               | interface_type_list ',' interface_type'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "interface_type_list")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "interface_type_list")

    def p_interface_type(self, p):
        '''interface_type : class_or_interface_type'''
        p[0] = nf.node_one_child(p[1], "interface_type")

    def p_class_body(self, p):
        '''class_body : '{' class_body_declarations_opt '}' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[3])
        p[0] = nf.node_three_child(node_leaf, p[2], node_leaf1, "class_body")

    def p_class_body_declarations_opt(self, p):
        '''class_body_declarations_opt : class_body_declarations'''
        p[0] = nf.node_one_child(p[1], "class_body_declarations_opt")

    def p_class_body_declarations_opt2(self, p):
        '''class_body_declarations_opt : empty'''
        node_leaf = nf.node("empty")
        p[0] = nf.node_one_child(node_leaf, "class_body_declarations_opt")

    def p_class_body_declarations(self, p):
        '''class_body_declarations : class_body_declaration
                                   | class_body_declarations class_body_declaration'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "class_body_declarations")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "class_body_declarations")

    def p_class_body_declaration(self, p):
        '''class_body_declaration : class_member_declaration
                                  | static_initializer
                                  | constructor_declaration'''
        p[0] = nf.node_one_child(p[1], "class_body_declaration")

    def p_class_body_declaration2(self, p):
        '''class_body_declaration : block'''
        p[0] = nf.node_one_child(p[1], "class_body_declaration")

    def p_class_member_declaration(self, p):
        '''class_member_declaration : field_declaration
                                    | class_declaration
                                    | method_declaration
                                    | interface_declaration
                                    | enum_declaration
                                    | annotation_type_declaration'''
        p[0] = nf.node_one_child(p[1], "class_member_declaration")

    def p_class_member_declaration2(self, p):
        '''class_member_declaration : ';' '''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_one_child(node_leaf, "class_member_declaration")


    def p_field_declaration(self, p):
        '''field_declaration : modifiers_opt type variable_declarators ';' '''
        node_leaf = nf.node(p[4])
        p[0] = nf.node_four_child(p[1], p[2], p[3], node_leaf, "field_declaration")

    def p_static_initializer(self, p):
        '''static_initializer : STATIC block'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[2], "static_initializer")

    def p_constructor_declaration(self, p):
        '''constructor_declaration : constructor_header method_body'''
        p[0] = nf.node_two_child(p[1], p[2], "constructor_declaration")

    def p_constructor_header(self, p):
        '''constructor_header : constructor_header_name formal_parameter_list_opt ')' method_header_throws_clause_opt'''
        node_leaf = nf.node(p[3])
        p[0] = nf.node_four_child(p[1], p[2], node_leaf, p[4], "constructor_header")

    def p_constructor_header_name(self, p):
        '''constructor_header_name : modifiers_opt type_parameters NAME '('
                                   | modifiers_opt NAME '(' '''
        if len(p) == 4:
            node_leaf = nf.node(p[2])
            node_leaf1 = nf.node(p[3])
            p[0] = nf.node_three_child(p[1], node_leaf, node_leaf1, "constructor_header_name")
        else:
            node_leaf = nf.node(p[3])
            node_leaf1 = nf.node(p[4])
            p[0] = nf.node_four_child(p[1], p[2], node_leaf, node_leaf1, "constructor_header_name")

    def p_formal_parameter_list_opt(self, p):
        '''formal_parameter_list_opt : formal_parameter_list'''
        p[0] = nf.node_one_child(p[1], "formal_parameter_list_opt")

    def p_formal_parameter_list_opt2(self, p):
        '''formal_parameter_list_opt : empty'''
        node_leaf = nf.node("empty")
        p[0] = nf.node_one_child(node_leaf,"formal_parameter_list_opt")

    def p_formal_parameter_list(self, p):
        '''formal_parameter_list : formal_parameter
                                 | formal_parameter_list ',' formal_parameter'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "formal_parameter_list")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "formal_parameter_list")

    def p_formal_parameter(self, p):
        '''formal_parameter : modifiers_opt type variable_declarator_id
                            | modifiers_opt type ELLIPSIS variable_declarator_id'''
        if len(p) == 4:
            p[0] = nf.node_three_child(p[1], p[2], p[3], "formal_parameter")
        else:
            node_leaf = nf.node(p[3])
            p[0] = nf.node_four_child(p[1], p[2], node_leaf, p[4], "formal_parameter")

    def p_method_header_throws_clause_opt(self, p):
        '''method_header_throws_clause_opt : method_header_throws_clause
                                           | empty'''
        if not p[1]:
            node_leaf = nf.node("empty")
            p[0] = nf.node_one_child(node_leaf,"method_header_throws_clause_opt")
        else:
            p[0] = nf.node_one_child(p[1], "method_header_throws_clause_opt")

    def p_method_header_throws_clause(self, p):
        '''method_header_throws_clause : THROWS class_type_list'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[2], "method_header_throws_clause")

    def p_class_type_list(self, p):
        '''class_type_list : class_type_elt
                           | class_type_list ',' class_type_elt'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "class_type_list")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "class_type_list")

    def p_class_type_elt(self, p):
        '''class_type_elt : class_type'''
        p[0] = nf.node_one_child(p[1], "class_type_elt")

    def p_method_body(self, p):
        '''method_body : '{' block_statements_opt '}' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[3])
        p[0] = nf.node_three_child(node_leaf, p[2], node_leaf1, "method_body")

    def p_method_declaration(self, p):
        '''method_declaration : abstract_method_declaration
                              | method_header method_body'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "method_declaration")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "method_declaration")

    def p_abstract_method_declaration(self, p):
        '''abstract_method_declaration : method_header ';' '''
        node_leaf = nf.node(p[2])
        p[0] = nf.node_two_child(p[1], node_leaf, "abstract_method_declaration")

    def p_method_header(self, p):
        '''method_header : method_header_name formal_parameter_list_opt ')' method_header_extended_dims method_header_throws_clause_opt'''
        node_leaf = nf.node(p[3])
        p[0] = nf.node_five_child(p[1], p[2], node_leaf, p[4], p[5], "method_header")

    def p_method_header_name(self, p):
        '''method_header_name : modifiers_opt type_parameters type NAME '('
                              | modifiers_opt type NAME '(' '''
        if len(p) == 6:
            node_leaf = nf.node(p[4])
            node_leaf1 = nf.node(p[5])
            p[0] = nf.node_five_child(p[1], p[2], p[3], node_leaf, node_leaf1, "method_header_name")
        else:
            node_leaf = nf.node(p[3])
            node_leaf1 = nf.node(p[4])
            p[0] = nf.node_four_child(p[1], p[2], node_leaf, node_leaf1, "method_header_name")

    def p_method_header_extended_dims(self, p):
        '''method_header_extended_dims : dims_opt'''
        p[0] = nf.node_one_child(p[1], "method_header_extended_dims")

    def p_interface_declaration(self, p):
        '''interface_declaration : interface_header interface_body'''
        p[0] = nf.node_two_child(p[1], p[2], "interface_declaration")

    def p_interface_header(self, p):
        '''interface_header : interface_header_name interface_header_extends_opt'''
        p[0] = nf.node_two_child(p[1], p[2], "interface_header")

    def p_interface_header_name(self, p):
        '''interface_header_name : interface_header_name1 type_parameters
                                 | interface_header_name1'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "interface_header_name")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "interface_header_name")

    def p_interface_header_name1(self, p):
        '''interface_header_name1 : modifiers_opt INTERFACE NAME'''
        node_leaf = nf.node(p[2])
        node_leaf1 = nf.node(p[3])
        p[0] = nf.node_three_child(p[1], node_leaf, node_leaf1, "interface_header_name1")

    def p_interface_header_extends_opt(self, p):
        '''interface_header_extends_opt : interface_header_extends'''
        p[0] = nf.node_one_child(p[1], "interface_header_extends_opt")

    def p_interface_header_extends_opt2(self, p):
        '''interface_header_extends_opt : empty'''
        node_leaf = nf.node("empty")
        p[0] = nf.node_one_child(node_leaf, "interface_header_extends_opt")

    def p_interface_header_extends(self, p):
        '''interface_header_extends : EXTENDS interface_type_list'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[2], "interface_header_extends")

    def p_interface_body(self, p):
        '''interface_body : '{' interface_member_declarations_opt '}' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[3])
        p[0] = nf.node_three_child(node_leaf, p[2], node_leaf1, "interface_body")

    def p_interface_member_declarations_opt(self, p):
        '''interface_member_declarations_opt : interface_member_declarations'''
        p[0] = nf.node_one_child(p[1], "interface_member_declarations_opt")

    def p_interface_member_declarations_opt2(self, p):
        '''interface_member_declarations_opt : empty'''
        node_leaf = nf.node("empty")
        p[0] = nf.node_one_child(node_leaf, "interface_member_declarations_opt")

    def p_interface_member_declarations(self, p):
        '''interface_member_declarations : interface_member_declaration
                                         | interface_member_declarations interface_member_declaration'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "interface_member_declarations")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "interface_member_declarations")

    def p_interface_member_declaration(self, p):
        '''interface_member_declaration : constant_declaration
                                        | abstract_method_declaration
                                        | class_declaration
                                        | interface_declaration
                                        | enum_declaration
                                        | annotation_type_declaration'''
        p[0] = nf.node_one_child(p[1], "interface_member_declaration")

    def p_interface_member_declaration2(self, p):
        '''interface_member_declaration : ';' '''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_one_child(node_leaf, "interface_member_declaration")

    def p_constant_declaration(self, p):
        '''constant_declaration : field_declaration'''
        p[0] = nf.node_one_child(p[1], "constant_declaration")

    def p_enum_declaration(self, p):
        '''enum_declaration : enum_header enum_body'''
        p[0] = nf.node_two_child(p[1], p[2], "enum_declaration")

    def p_enum_header(self, p):
        '''enum_header : enum_header_name class_header_implements_opt'''
        p[0] = nf.node_two_child(p[1], p[2], "enum_header")

    def p_enum_header_name(self, p):
        '''enum_header_name : modifiers_opt ENUM NAME
                            | modifiers_opt ENUM NAME type_parameters'''
        if len(p) == 4:
            node_leaf = nf.node(p[2])
            node_leaf1 = nf.node(p[3])
            p[0] = nf.node_three_child(p[1], node_leaf, node_leaf1, "enum_header_name")
        else:
            node_leaf = nf.node(p[2])
            node_leaf = nf.node(p[3])
            p[0] = nf.node_four_child(p[1], node_leaf, node_leaf1, p[4], "enum_header_name")

    def p_enum_body(self, p):
        '''enum_body : '{' enum_body_declarations_opt '}' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[3])
        p[0] = nf.node_three_child(node_leaf, p[2], node_leaf1, "enum_body")

    def p_enum_body2(self, p):
        '''enum_body : '{' ',' enum_body_declarations_opt '}' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[2])
        node_leaf2 = nf.node(p[4])
        p[0] = nf.node_four_child(node_leaf, node_leaf1, p[3], node_leaf2, "enum_body")

    def p_enum_body3(self, p):
        '''enum_body : '{' enum_constants ',' enum_body_declarations_opt '}' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[3])
        node_leaf2 = nf.node(p[5])
        p[0] = nf.node_five_child(node_leaf, p[2], node_leaf1, p[4], node_leaf2, "enum_body")

    def p_enum_body4(self, p):
        '''enum_body : '{' enum_constants enum_body_declarations_opt '}' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[4])
        p[0] = nf.node_four_child(node_leaf, p[2], p[3], node_leaf1, "enum_body")

    def p_enum_constants(self, p):
        '''enum_constants : enum_constant
                          | enum_constants ',' enum_constant'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "enum_constants")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "enum_constants")

    def p_enum_constant(self, p):
        '''enum_constant : enum_constant_header class_body
                         | enum_constant_header'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "enum_constant")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "enum_constant")

    def p_enum_constant_header(self, p):
        '''enum_constant_header : enum_constant_header_name arguments_opt'''
        p[0] = nf.node_two_child(p[1], p[2], "enum_constant_header")

    def p_enum_constant_header_name(self, p):
        '''enum_constant_header_name : modifiers_opt NAME'''
        node_leaf = nf.node(p[2])
        p[0] = nf.node_two_child(p[1], node_leaf, "enum_constant_header_name")

    def p_arguments_opt(self, p):
        '''arguments_opt : arguments'''
        p[0] = nf.node_one_child(p[1], "arguments_opt")

    def p_arguments_opt2(self, p):
        '''arguments_opt : empty'''
        node_leaf = nf.node("empty")
        p[0] = nf.node_one_child(node_leaf, "arguments_opt")

    def p_arguments(self, p):
        '''arguments : '(' argument_list_opt ')' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[3])
        p[0] = nf.node(node_leaf, p[2], node_leaf1, "arguments")

    def p_argument_list_opt(self, p):
        '''argument_list_opt : argument_list'''
        p[0] = nf.node_one_child(p[1], "argument_list_opt")

    def p_argument_list_opt2(self, p):
        '''argument_list_opt : empty'''
        node_leaf = nf.node("empty")
        p[0] = nf.node_one_child(node_leaf, "argument_list_opt")

    def p_argument_list(self, p):
        '''argument_list : expression
                         | argument_list ',' expression'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "argument_list")
        else:
            node_leaf = nf.node(p[2])
            p[0] =  nf.node_three_child(p[1], node_leaf, p[3], "argument_list")

    def p_enum_body_declarations_opt(self, p):
        '''enum_body_declarations_opt : enum_declarations'''
        p[0] = nf.node_one_child(p[1], "enum_body_declarations_opt")

    def p_enum_body_declarations_opt2(self, p):
        '''enum_body_declarations_opt : empty'''
        node_leaf = nf.node("empty")
        p[0] = nf.node_one_child(node_leaf, "enum_body_declarations_opt")

    def p_enum_body_declarations(self, p):
        '''enum_declarations : ';' class_body_declarations_opt'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[2], "enum_declarations")

    def p_annotation_type_declaration(self, p):
        '''annotation_type_declaration : annotation_type_declaration_header annotation_type_body'''
        p[0] = nf.node_two_child(p[1], p[2], "annotation_type_declaration")

    def p_annotation_type_declaration_header(self, p):
        '''annotation_type_declaration_header : annotation_type_declaration_header_name class_header_extends_opt class_header_implements_opt'''
        p[0] = nf.node_three_child(p[1], p[2], p[3], "annotation_type_declaration_header")

    def p_annotation_type_declaration_header_name(self, p):
        '''annotation_type_declaration_header_name : modifiers '@' INTERFACE NAME'''
        node_leaf = nf.node(p[2])
        node_leaf1 = nf.node(p[3])
        node_leaf2 = nf.node(p[4])
        p[0] = nf.node_four_child(p[1], node_leaf, node_leaf1, node_leaf2, "annotation_type_declaration_header_name")

    def p_annotation_type_declaration_header_name2(self, p):
        '''annotation_type_declaration_header_name : modifiers '@' INTERFACE NAME type_parameters'''
        node_leaf = nf.node(p[2])
        node_leaf1 = nf.node(p[3])
        node_leaf2 = nf.node(p[4])
        p[0] = nf.node_five_child(p[1], node_leaf, node_leaf1, node_leaf2, p[5], "annotation_type_declaration_header_name")

    def p_annotation_type_declaration_header_name3(self, p):
        '''annotation_type_declaration_header_name : '@' INTERFACE NAME type_parameters'''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[2])
        node_leaf2 = nf.node(p[3])
        p[0] = nf.node_four_child(node_leaf, node_leaf1, node_leaf2, p[4], "annotation_type_declaration_header_name")

    def p_annotation_type_declaration_header_name4(self, p):
        '''annotation_type_declaration_header_name : '@' INTERFACE NAME'''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[2])
        node_leaf2 = nf.node(p[3])
        p[0] = nf.node_three_child(node_leaf, node_leaf1, node_leaf2, "annotation_type_declaration_header_name")


    def p_annotation_type_body(self, p):
        '''annotation_type_body : '{' annotation_type_member_declarations_opt '}' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[3])
        p[0] = nf.node_three_child(node_leaf, p[2], node_leaf1, "annotation_type_body")

    def p_annotation_type_member_declarations_opt(self, p):
        '''annotation_type_member_declarations_opt : annotation_type_member_declarations'''
        p[0] = nf.node_one_child(p[1], "annotation_type_member_declarations_opt")

    def p_annotation_type_member_declarations_opt2(self, p):
        '''annotation_type_member_declarations_opt : empty'''
        node_leaf = nf.node("empty")
        p[0] = nf.node_one_child(node_leaf, "annotation_type_member_declarations_opt")

    def p_annotation_type_member_declarations(self, p):
        '''annotation_type_member_declarations : annotation_type_member_declaration
                                               | annotation_type_member_declarations annotation_type_member_declaration'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "annotation_type_member_declarations")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "annotation_type_member_declarations")

    def p_annotation_type_member_declaration(self, p):
        '''annotation_type_member_declaration : annotation_method_header ';'
                                              | constant_declaration
                                              | constructor_declaration
                                              | type_declaration'''
        if len(p) == 3:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_two_child(p[1], node_leaf, "annotation_type_member_declaration")
        else:
            p[0] = nf.node_one_child(p[1], "annotation_type_member_declaration")

    def p_annotation_method_header(self, p):
        '''annotation_method_header : annotation_method_header_name formal_parameter_list_opt ')' method_header_extended_dims annotation_method_header_default_value_opt'''
        node_leaf = nf.node(p[3])
        p[0] = nf.node_five_child(p[1], p[2], node_leaf, p[4], p[5], "annotation_method_header")

    def p_annotation_method_header_name(self, p):
        '''annotation_method_header_name : modifiers_opt type_parameters type NAME '('
                                         | modifiers_opt type NAME '(' '''
        if len(p) == 6:
            node_leaf = nf.node(p[4])
            node_leaf1 = nf.node(p[5])
            p[0] = nf.node_four_child(p[1], p[2], p[3], node_leaf, node_leaf1, "annotation_method_header_name")
        else:
            node_leaf = nf.node(p[3])
            node_leaf1 = nf.node(p[4])
            p[0] = nf.node_four_child(p[1], p[2], node_leaf, node_leaf1, "annotation_method_header_name")

    def p_annotation_method_header_default_value_opt(self, p):
        '''annotation_method_header_default_value_opt : default_value
                                                      | empty'''
        if not p[1]:
            node_leaf = nf.node("empty")
            p[0] = nf.node_one_child(node_leaf, "annotation_method_header_default_value_opt")
        else:
            p[0] = nf.node_one_child(p[1], "annotation_method_header_default_value_opt")

    def p_default_value(self, p):
        '''default_value : DEFAULT member_value'''
        node_leaf =nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[2], "default_value")

    def p_member_value(self, p):
        '''member_value : conditional_expression_not_name
                        | name
                        | annotation
                        | member_value_array_initializer'''
        p[0] = nf.node_one_child(p[1], "member_value")

    def p_member_value_array_initializer(self, p):
        '''member_value_array_initializer : '{' member_values ',' '}'
                                          | '{' member_values '}' '''
        if len(p) == 5:
            node_leaf = nf.node(p[1])
            node_leaf1 = nf.node(p[3])
            node_leaf2 = nf.node(p[4])
            p[0] = nf.node_four_child(node_leaf, p[2], node_leaf1, node_leaf2, "member_value_array_initializer")
        else:
            node_leaf = nf.node(p[1])
            node_leaf1 = nf.node(p[3])
            p[0] = nf.node_three_child(node_leaf, p[2], node_leaf1, "member_value_array_initializer")

    def p_member_value_array_initializer2(self, p):
        '''member_value_array_initializer : '{' ',' '}'
                                          | '{' '}' '''
        # ignore
        if len(p) == 4:
            node_leaf = nf.node(p[1])
            node_leaf1 = nf.node(p[2])
            node_leaf2 = nf.node(p[3])
            p[0] = nf.node_three_child(node_leaf, node_leaf1, node_leaf2, "member_value_array_initializer")
        else:
            node_leaf = nf.node(p[1])
            node_leaf1 = nf.node(p[2])
            p[0] = nf.node_two_child(node_leaf, node_leaf1, "member_value_array_initializer")

    def p_member_values(self, p):
        '''member_values : member_value
                         | member_values ',' member_value'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "member_values")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "member_values")

    def p_annotation(self, p):
        '''annotation : normal_annotation
                      | marker_annotation
                      | single_member_annotation'''
        p[0] = nf.node_one_child(p[1], "annotation")

    def p_normal_annotation(self, p):
        '''normal_annotation : annotation_name '(' member_value_pairs_opt ')' '''
        node_leaf = nf.node(p[2])
        node_leaf1 = nf.node(p[4])
        p[0] = nf.node_four_child(p[1], node_leaf, p[3], node_leaf1, "normal_annotation")

    def p_annotation_name(self, p):
        '''annotation_name : '@' name'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[2], "annotation_name")

    def p_member_value_pairs_opt(self, p):
        '''member_value_pairs_opt : member_value_pairs'''
        p[0] = nf.node_one_child(p[1], "member_value_pairs_opt")

    def p_member_value_pairs_opt2(self, p):
        '''member_value_pairs_opt : empty'''
        node_leaf = nf.node("empty")
        p[0] = nf.node_one_child(node_leaf, "member_value_pairs_opt")

    def p_member_value_pairs(self, p):
        '''member_value_pairs : member_value_pair
                              | member_value_pairs ',' member_value_pair'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "member_value_pairs")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "member_value_pairs")

    def p_member_value_pair(self, p):
        '''member_value_pair : simple_name '=' member_value'''
        node_leaf = nf.node(p[2])
        p[0] = nf.node_three_child(p[1], node_leaf, p[3], "member_value_pair")

    def p_marker_annotation(self, p):
        '''marker_annotation : annotation_name'''
        p[0] = nf.node_one_child(p[1], "marker_annotation")

    def p_single_member_annotation(self, p):
        '''single_member_annotation : annotation_name '(' single_member_annotation_member_value ')' '''
        node_leaf = nf.node(p[2])
        node_leaf1 = nf.node(p[4])
        p[0] = nf.node_four_child(p[1], node_leaf, p[3], node_leaf1, "single_member_annotation")

    def p_single_member_annotation_member_value(self, p):
        '''single_member_annotation_member_value : member_value'''
        p[0] = nf.node_one_child(p[1], "single_member_annotation_member_value")

class CompilationUnitParser(object):

    def p_compilation_unit(self, p):
        '''compilation_unit : package_declaration'''
        p[0] = nf.node_one_child(p[1], "compilation_unit")

    def p_compilation_unit2(self, p):
        '''compilation_unit : package_declaration import_declarations'''
        p[0] = nf.node_two_child(p[1], p[2], "compilation_unit")

    def p_compilation_unit3(self, p):
        '''compilation_unit : package_declaration import_declarations type_declarations'''
        p[0] = nf.node_three_child(p[1], p[2], p[3], "compilation_unit")

    def p_compilation_unit4(self, p):
        '''compilation_unit : package_declaration type_declarations'''
        p[0] = nf.node_two_child(p[1], p[2], "compilation_unit")

    def p_compilation_unit5(self, p):
        '''compilation_unit : import_declarations'''
        p[0] = nf.node_one_child(p[1], "compilation_unit")

    def p_compilation_unit6(self, p):
        '''compilation_unit : type_declarations'''
        p[0] = nf.node_one_child(p[1], "compilation_unit")

    def p_compilation_unit7(self, p):
        '''compilation_unit : import_declarations type_declarations'''
        p[0] = nf.node_two_child(p[1], p[2], "compilation_unit")

    def p_compilation_unit8(self, p):
        '''compilation_unit : empty'''
        node_leaf = nf.node("empty")
        p[0] = nf.node_one_child(node_leaf, "compilation_unit")

    def p_package_declaration(self, p):
        '''package_declaration : package_declaration_name ';' '''
        node_leaf = nf.node(p[2])
        p[0] = nf.node_two_child(p[1], node_leaf, "package_declaration")

    def p_package_declaration_name(self, p):
        '''package_declaration_name : modifiers PACKAGE name
                                    | PACKAGE name'''
        if len(p) == 3:
            node_leaf = nf.node(p[1])
            p[0] = nf.node_two_child(node_leaf, p[2], "package_declaration_name")
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1], node_leaf, p[3], "package_declaration_name")

    def p_import_declarations(self, p):
        '''import_declarations : import_declaration
                               | import_declarations import_declaration'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "import_declarations")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "import_declarations")

    def p_import_declaration(self, p):
        '''import_declaration : single_type_import_declaration
                              | type_import_on_demand_declaration
                              | single_static_import_declaration
                              | static_import_on_demand_declaration'''
        p[0] = nf.node_one_child(p[1], "import_declaration")

    def p_single_type_import_declaration(self, p):
        '''single_type_import_declaration : IMPORT name ';' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[3])
        p[0] = nf.node_three_child(node_leaf, p[2], node_leaf1, "single_type_import_declaration")

    def p_type_import_on_demand_declaration(self, p):
        '''type_import_on_demand_declaration : IMPORT name '.' '*' ';' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[3])
        node_leaf2 = nf.node(p[4])
        node_leaf3 = nf.node(p[5])
        p[0] = nf.node_five_child(node_leaf, p[2], node_leaf1, node_leaf2, node_leaf3, "type_import_on_demand_declaration")

    def p_single_static_import_declaration(self, p):
        '''single_static_import_declaration : IMPORT STATIC name ';' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[2])
        node_leaf2 = nf.node(p[4])
        p[0] = nf.node_four_child(node_leaf, node_leaf1, p[3], node_leaf2, "single_static_import_declaration")

    def p_static_import_on_demand_declaration(self, p):
        '''static_import_on_demand_declaration : IMPORT STATIC name '.' '*' ';' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[2])
        node_leaf2 = nf.node(p[4])
        node_leaf3 = nf.node(p[5])
        node_leaf4 = nf.node(p[6])
        p[0] = nf.node_six_child(node_leaf, node_leaf1, p[3], node_leaf2, node_leaf3, node_leaf4, "static_import_on_demand_declaration")

    def p_type_declarations(self, p):
        '''type_declarations : type_declaration
                             | type_declarations type_declaration'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1], "type_declarations")
        else:
            p[0] = nf.node_two_child(p[1], p[2], "type_declarations")

class MyParser(ExpressionParser, NameParser, LiteralParser, TypeParser, ClassParser, StatementParser, CompilationUnitParser):

    tokens = lexRule.tokens

    def p_start_compilation_unit(self, p):
        '''start : PLUSPLUS compilation_unit'''
        p[0] = nf.node_one_child(p[2],"start")

    def p_start_expression(self, p):
        '''start : MINUSMINUS expression'''
        p[0] = nf.node_one_child(p[2],"start")


    def p_start_statement(self, p):
        '''start : '*' block_statement'''
        p[0] = nf.node_one_child(p[2],"start")


    def p_error(self, p):
        print('error: {}'.format(p))

    def p_empty(self, p):
        '''empty :'''

class Parser(object):

    def __init__(self):
        self.lexer = lex.lex(module=lexRule)
        self.parser = yacc.yacc(module=MyParser(), start='start')

    def tokenize_string(self, code):
        self.lexer.input(code)
        for token in self.lexer:
            print(token)

    def tokenize_file(self, _file):
        if type(_file) == str:
            _file = open(_file)
        content = ''
        for line in _file:
            content += line
        return self.tokenize_string(content)

    def parse_expression(self, code, debug=0, lineno=1):
        return self.parse_string(code, debug, lineno, prefix='--')

    def parse_statement(self, code, debug=0, lineno=1):
        return self.parse_string(code, debug, lineno, prefix='* ')

    def parse_string(self, code, debug=0, lineno=1, prefix='++'):
        self.lexer.lineno = lineno
        return self.parser.parse(prefix + code, lexer=self.lexer, debug=debug)

    def parse_file(self, _file, debug=0):
        if type(_file) == str:
            _file = open(_file)
        content = _file.read()
        return self.parse_string(content, debug=debug)
