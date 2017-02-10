import pydot
import node_file as nf
import lexRule

global tokens

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


    def p_expression(self, p):
        '''expression : assignment_expression'''
        p[0] = nf.node_one_child(p[1],"expression")

    def p_expression_not_name(self, p):
        '''expression_not_name : assignment_expression_not_name'''
        p[0] = nf.node_one_child(p[1],"expression_not_name")

    def p_assignment_expression(self, p):
        '''assignment_expression : assignment
                                 | conditional_expression'''
        p[0] = nf.node_one_child(p[1],"assignment_expression")

    def p_assignment_expression_not_name(self, p):
        '''assignment_expression_not_name : assignment
                                          | conditional_expression_not_name'''
        p[0] = nf.node_one_child(p[1],"assignment_expression_not_name")

    def p_assignment(self, p):
        '''assignment : postfix_expression assignment_operator assignment_expression'''
        p[0] = nf.node_three_child(p[1],p[2],p[3],"assignment")
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
        node_leaf = nf.node(p[1])
        p[0] = nf.node_one_child(node_leaf,"assignment_operator")


    def p_conditional_expression(self, p):
        '''conditional_expression : conditional_or_expression
                                  | conditional_or_expression '?' expression ':' conditional_expression'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1],"conditional_expression")
        else:
            node_leaf = nf.node(p[2])
            node_leaf1 = nf.node(p[4])
            p[0] = nf.node_five_child(p[1],p[2],p[3],p[4],p[5],"conditional_expression")

    def p_conditional_expression_not_name(self, p):
        '''conditional_expression_not_name : conditional_or_expression_not_name
                                           | conditional_or_expression_not_name '?' expression ':' conditional_expression
                                           | name '?' expression ':' conditional_expression'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1],"conditional_expression_not_name")
        else:
            node_leaf = nf.node(p[2])
            node_leaf1 = nf.node(p[4])
            p[0] = nf.node_five_child(p[1],p[2],p[3],p[4],p[5],"conditional_expression_not_name")

    def one_or_three(self, p, name_of_node):
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1],name_of_node)
        else:
            node_leaf = nf.node(p[2])
            p[0] = nf.node_three_child(p[1],node_leaf,p[3],name_of_node)
            #Ease: For ease of reading operator is between operants

    def p_conditional_or_expression(self, p):
        '''conditional_or_expression : conditional_and_expression
                                     | conditional_or_expression OR conditional_and_expression'''
        self.one_or_three(p, "conditional_or_expression")

    def p_conditional_or_expression_not_name(self, p):
        '''conditional_or_expression_not_name : conditional_and_expression_not_name
                                              | conditional_or_expression_not_name OR conditional_and_expression
                                              | name OR conditional_and_expression'''
        self.one_or_three(p, "conditional_or_expression_not_name")

    def p_conditional_and_expression(self, p):
        '''conditional_and_expression : inclusive_or_expression
                                      | conditional_and_expression AND inclusive_or_expression'''
        self.one_or_three(p, "conditional_and_expression")

    def p_conditional_and_expression_not_name(self, p):
        '''conditional_and_expression_not_name : inclusive_or_expression_not_name
                                               | conditional_and_expression_not_name AND inclusive_or_expression
                                               | name AND inclusive_or_expression'''
        self.one_or_three(p, "conditional_and_expression_not_name")

    def p_inclusive_or_expression(self, p):
        '''inclusive_or_expression : exclusive_or_expression
                                   | inclusive_or_expression '|' exclusive_or_expression'''
        self.one_or_three(p, "inclusive_or_expression")

    def p_inclusive_or_expression_not_name(self, p):
        '''inclusive_or_expression_not_name : exclusive_or_expression_not_name
                                            | inclusive_or_expression_not_name '|' exclusive_or_expression
                                            | name '|' exclusive_or_expression'''
        self.one_or_three(p, "inclusive_or_expression_not_name")

    def p_exclusive_or_expression(self, p):
        '''exclusive_or_expression : and_expression
                                   | exclusive_or_expression '^' and_expression'''
        self.one_or_three(p, "exclusive_or_expression")

    def p_exclusive_or_expression_not_name(self, p):
        '''exclusive_or_expression_not_name : and_expression_not_name
                                            | exclusive_or_expression_not_name '^' and_expression
                                            | name '^' and_expression'''
        self.one_or_three(p, "exclusive_or_expression_not_name")

    def p_and_expression(self, p):
        '''and_expression : equality_expression
                          | and_expression '&' equality_expression'''
        self.one_or_three(p, "and_expression")

    def p_and_expression_not_name(self, p):
        '''and_expression_not_name : equality_expression_not_name
                                   | and_expression_not_name '&' equality_expression
                                   | name '&' equality_expression'''
        self.one_or_three(p, "and_expression_not_name")

    def p_equality_expression(self, p):
        '''equality_expression : instanceof_expression
                               | equality_expression EQ instanceof_expression
                               | equality_expression NEQ instanceof_expression'''
        self.one_or_three(p, "equality_expression")

    def p_equality_expression_not_name(self, p):
        '''equality_expression_not_name : instanceof_expression_not_name
                                        | equality_expression_not_name EQ instanceof_expression
                                        | name EQ instanceof_expression
                                        | equality_expression_not_name NEQ instanceof_expression
                                        | name NEQ instanceof_expression'''
        self.one_or_three(p, "equality_expression_not_name")

    def p_instanceof_expression(self, p):
        '''instanceof_expression : relational_expression
                                 | instanceof_expression INSTANCEOF reference_type'''
        self.one_or_three(p, "instanceof_expression")

    def p_instanceof_expression_not_name(self, p):
        '''instanceof_expression_not_name : relational_expression_not_name
                                          | name INSTANCEOF reference_type
                                          | instanceof_expression_not_name INSTANCEOF reference_type'''
        self.one_or_three(p, "instanceof_expression_not_name")

    def p_relational_expression(self, p):
        '''relational_expression : shift_expression
                                 | relational_expression '>' shift_expression
                                 | relational_expression '<' shift_expression
                                 | relational_expression GTEQ shift_expression
                                 | relational_expression LTEQ shift_expression'''
        self.one_or_three(p, "relational_expression")

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
        self.one_or_three(p, "relational_expression_not_name")

    def p_shift_expression(self, p):
        '''shift_expression : additive_expression
                            | shift_expression LSHIFT additive_expression
                            | shift_expression RSHIFT additive_expression
                            | shift_expression RRSHIFT additive_expression'''
        self.one_or_three(p, "shift_expression")

    def p_shift_expression_not_name(self, p):
        '''shift_expression_not_name : additive_expression_not_name
                                     | shift_expression_not_name LSHIFT additive_expression
                                     | name LSHIFT additive_expression
                                     | shift_expression_not_name RSHIFT additive_expression
                                     | name RSHIFT additive_expression
                                     | shift_expression_not_name RRSHIFT additive_expression
                                     | name RRSHIFT additive_expression'''
        self.one_or_three(p, "shift_expression_not_name")

    def p_additive_expression(self, p):
        '''additive_expression : multiplicative_expression
                               | additive_expression '+' multiplicative_expression
                               | additive_expression '-' multiplicative_expression'''
        self.one_or_three(p, "additive_expression")

    def p_additive_expression_not_name(self, p):
        '''additive_expression_not_name : multiplicative_expression_not_name
                                        | additive_expression_not_name '+' multiplicative_expression
                                        | name '+' multiplicative_expression
                                        | additive_expression_not_name '-' multiplicative_expression
                                        | name '-' multiplicative_expression'''
        self.one_or_three(p, "additive_expression_not_name")

    def p_multiplicative_expression(self, p):
        '''multiplicative_expression : unary_expression
                                     | multiplicative_expression '*' unary_expression
                                     | multiplicative_expression '/' unary_expression
                                     | multiplicative_expression '%' unary_expression'''
        self.one_or_three(p, "multiplicative_expression")

    def p_multiplicative_expression_not_name(self, p):
        '''multiplicative_expression_not_name : unary_expression_not_name
                                              | multiplicative_expression_not_name '*' unary_expression
                                              | name '*' unary_expression
                                              | multiplicative_expression_not_name '/' unary_expression
                                              | name '/' unary_expression
                                              | multiplicative_expression_not_name '%' unary_expression
                                              | name '%' unary_expression'''
        self.one_or_three(p, "multiplicative_expression_not_name")

    def front_unary(self, p,node_name):
        node_leaf = nf.node(p[1])
        nf.node_two_child(leaf_node,p[2],node_name)


    def back_unary(self, p,node_name):
        node_leaf = nf.node(p[2])
        nf.node_two_child(p[1],leaf_node,node_name)

    def p_unary_expression(self, p):
        '''unary_expression : pre_increment_expression
                            | pre_decrement_expression
                            | '+' unary_expression
                            | '-' unary_expression
                            | unary_expression_not_plus_minus'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1],"unary_expression")
        else:
            p[0] = front_unary(p, "unary_expression")

    def p_unary_expression_not_name(self, p):
        '''unary_expression_not_name : pre_increment_expression
                                     | pre_decrement_expression
                                     | '+' unary_expression
                                     | '-' unary_expression
                                     | unary_expression_not_plus_minus_not_name'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1],"unary_expression_not_expression")
        else:
            p[0] = front_unary(p, "unary_expression_not_name")

    def p_pre_increment_expression(self, p):
        '''pre_increment_expression : PLUSPLUS unary_expression'''
        node_leaf = nf.node(p[1])
        nf.node_two_child(node_leaf,p[2])

    def p_pre_decrement_expression(self, p):
        '''pre_decrement_expression : MINUSMINUS unary_expression'''
        node_leaf = nf.node(p[1])
        nf.node_two_child(node_leaf,p[2])

    def p_unary_expression_not_plus_minus(self, p):
        '''unary_expression_not_plus_minus : postfix_expression
                                           | '~' unary_expression
                                           | '!' unary_expression
                                           | cast_expression'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1],"unary_expression_not_plus_minus")
        else:
            p[0] = front_unary(p, "unary_expression_not_plus_minus")


    def p_unary_expression_not_plus_minus_not_name(self, p):
        '''unary_expression_not_plus_minus_not_name : postfix_expression_not_name
                                                    | '~' unary_expression
                                                    | '!' unary_expression
                                                    | cast_expression'''
        if len(p) == 2:
            p[0] = nf.node_one_child(p[1],"unary_expression_not_plus_minus_not_name")
        else:
            p[0] = front_unary(p, "unary_expression_not_plus_minus_not_name")

    def p_postfix_expression(self, p):
        '''postfix_expression : primary
                              | name
                              | post_increment_expression
                              | post_decrement_expression'''
        p[0] = nf.node_one_child(p[1],"postfix_expression")

    def p_postfix_expression_not_name(self, p):
        '''postfix_expression_not_name : primary
                                       | post_increment_expression
                                       | post_decrement_expression'''
        p[0] = nf.node_one_child(p[1],"postfix_expression_not_name")

    def p_post_increment_expression(self, p):
        '''post_increment_expression : postfix_expression PLUSPLUS'''
        p[0] = back_unary(p, "post_increment_expression")

    def p_post_decrement_expression(self, p):
        '''post_decrement_expression : postfix_expression MINUSMINUS'''
        p[0] = back_unary(p, "post_decrement_expression")

    def p_primary(self, p):
        '''primary : primary_no_new_array
                   | array_creation_with_array_initializer
                   | array_creation_without_array_initializer'''
        p[0] = nf.node_one_child(p[1],"primary")

    def p_primary_no_new_array(self, p):
        '''primary_no_new_array : literal
                                | THIS
                                | class_instance_creation_expression
                                | field_access
                                | method_invocation
                                | array_access'''
        if p[1] == "THIS":
            node_leaf = nf.node(p[1])
            p[0] = node_one_child(node_leaf,"primary_no_new_array")
        else:
            p[0] = node_one_child(p[1],"primary_no_new_array")

    def p_primary_no_new_array2(self, p):
        '''primary_no_new_array : '(' name ')'
                                | '(' expression_not_name ')' '''
        node_leaf = nf.node(p[1])
        node_leaf1 = nf.node(p[3])
        p[0] = node_three_child(node_leaf,p[2],node_leaf1)

    def p_primary_no_new_array3(self, p):
        '''primary_no_new_array : name '.' THIS
                                | name '.' SUPER'''
        node_leaf = nf.node(p[2])
        node_leaf1 = nf.node(p[3])
        p[0] = nf.node_three_child(p[1],node_leaf,node_leaf1)

    def p_primary_no_new_array4(self, p):
        '''primary_no_new_array : name '.' CLASS
                                | name dims '.' CLASS
                                | primitive_type dims '.' CLASS
                                | primitive_type '.' CLASS'''
        if len(p) == 4:
            p[0] = p[1]
        else:
            p[0] = p[1]

    def p_dims_opt(self, p):
        '''dims_opt : dims'''
        p[0] = p[1]

    def p_dims_opt2(self, p):
        '''dims_opt : empty'''
        p[0] = 0

    def p_dims(self, p):
        '''dims : dims_loop'''
        p[0] = p[1]

    def p_dims_loop(self, p):
        '''dims_loop : one_dim_loop
                     | dims_loop one_dim_loop'''
        if len(p) == 2:
            p[0] = 1
        else:
            p[0] = 1 + p[1]

    def p_one_dim_loop(self, p):
        '''one_dim_loop : '[' ']' '''
        # ignore

    def p_cast_expression(self, p):
        '''cast_expression : '(' primitive_type dims_opt ')' unary_expression'''
        p[0] = p[1]#Cast(Type(p[2], dimensions=p[3]), p[5])

    def p_cast_expression2(self, p):
        '''cast_expression : '(' name type_arguments dims_opt ')' unary_expression_not_plus_minus'''
        p[0] = p[1]#Cast(Type(p[2], type_arguments=p[3], dimensions=p[4]), p[6])

    def p_cast_expression3(self, p):
        '''cast_expression : '(' name type_arguments '.' class_or_interface_type dims_opt ')' unary_expression_not_plus_minus'''
        p[0] = p[1]
        #p[5].dimensions = p[6]
        #p[5].enclosed_in = Type(p[2], type_arguments=p[3])
        #p[0] = Cast(p[5], p[8])

    def p_cast_expression4(self, p):
        '''cast_expression : '(' name ')' unary_expression_not_plus_minus'''
        # technically it's not necessarily a type but could be a type parameter
        p[0] = p[1]#Cast(Type(p[2]), p[4])

    def p_cast_expression5(self, p):
        '''cast_expression : '(' name dims ')' unary_expression_not_plus_minus'''
        # technically it's not necessarily a type but could be a type parameter
        p[0] = p[1]#Cast(Type(p[2], dimensions=p[3]), p[5])

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
        p[0] = nf.node_one_child(p[1], "modifiers_opt")

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
                    | STRICTFP
                    | annotation'''
        if p[1] != "public" | "protected" | "private" | "static" | "abstract" | "final" | "native" | "synchronized" | "transient" | "volatile" | "strictfp":
            p[0] = nf.node_one_child(p[1], "modifier")
        else:
            node_leaf = nf.node(p[1])
            p[0] = nf.node_one_child(node_leaf, "modifier")

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
            p[0] = nf.node_three_child(p[1],p[2],p[3],"class_or_interface")

    def p_generic_type(self, p):
        '''generic_type : class_or_interface type_arguments'''
        p[0] = nf.node_two_child(p[1],p[2],"generic_type")

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
        p[0] = nf.node_three_child(p[1], node_leaf, p[3], "array_type")

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
        if p[1] == 'extends':
            node_leaf = nf.node(p[1])
            p[0] = nf.node_two_child(node_leaf, p[2], "wildcard_bounds")
        else:
            node_leaf = nf.node(p[1])
            p[0] = nf.node_two_child(node_leaf, p[2], "wildcard_bounds")

    def p_wildcard1(self, p):
        '''wildcard1 : '?' '>'
                     | '?' wildcard_bounds1'''
        if p[2] == '>':
            node_leaf = nf.node(p[1])
            node_leaf1 = nf.node(p[2])
            p[0] = nf.node_two_child(node_leaf, node_leaf1, "wildcard1")
        else:
            node_leaf = nf.node(p[1])
            p[0] = nf.node_two_child(node_leaf, p[2], "wildcard1")

    def p_wildcard_bounds1(self, p):
        '''wildcard_bounds1 : EXTENDS reference_type1
                            | SUPER reference_type1'''
        if p[1] == 'extends':
            node_leaf = nf.node(p[1])
            p[0] = nf.node_two_child(node_leaf, p[2], "wildcard_bounds1")
        else:
            node_leaf = nf.node(p[1])
            p[0] = nf.node_two_child(node_leaf, p[2], "wildcard_bounds1")

    def p_wildcard2(self, p):
        '''wildcard2 : '?' RSHIFT
                     | '?' wildcard_bounds2'''
        if p[2] == '>>':
            node_leaf = nf.node(p[1])
            node_leaf1 = nf.node(p[2])
            p[0] = nf.node_two_child(node_leaf, node_leaf1, "wildcard2")
        else:
            node_leaf = nf.node(p[1])
            p[0] = nf.node_two_child(node_leaf, p[2], "wildcard2")

    def p_wildcard_bounds2(self, p):
        '''wildcard_bounds2 : EXTENDS reference_type2
                            | SUPER reference_type2'''
        if p[1] == 'extends':
            node_leaf = nf.node(p[1])
            p[0] = nf.node_two_child(node_leaf, p[2], "wildcard_bounds2")
        else:
            node_leaf = nf.node(p[1])
            p[0] = nf.node_two_child(node_leaf, p[2], "wildcard_bounds2")

    def p_wildcard3(self, p):
        '''wildcard3 : '?' RRSHIFT
                     | '?' wildcard_bounds3'''
        if p[2] == '>>>':
            node_leaf = nf.node(p[1])
            node_leaf1 = nf.node(p[2])
            p[0] = nf.node_two_child(node_leaf, node_leaf2, "wildcard3")
        else:
            node_leaf = nf.node(p[1])
            p[0] = nf.node_two_child(node_leaf, p[2], "wildcard3")

    def p_wildcard_bounds3(self, p):
        '''wildcard_bounds3 : EXTENDS reference_type3
                            | SUPER reference_type3'''
        if p[1] == 'extends':
            node_leaf = nf.node(p[1])
            p[0] = nf.node_two_child(node_leaf, p[2], "wildcard_bounds3")
        else:
            node_leaf = nf.node(p[1])
            p[0] = nf.node_two_child(node_leaf, p[2], "wildcard_bounds3")

    def p_type_parameter_header(self, p):
        '''type_parameter_header : NAME'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_one_child(node_leaf, "type_parameter_header")

    def p_type_parameters(self, p):
        '''type_parameters : '<' type_parameter_list1'''
        node_leaf = nf.node(p[1])
        p[0] = nf.node_two_child(node_leaf, p[1], "type_parameters")

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
