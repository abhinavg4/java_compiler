# Base node
import pdb
import pydot
import sys
import SymbolTable
global graph
global outputfile
from tac import *

global tac
tac = TAC()

idg = 0
graph = pydot.Dot(graph_type='digraph',ranksep=0.02,nodesep=0.02,size="8.5,11")

class SourceElement(object):
    '''
    A SourceElement is the base class for all elements that occur in a Java
    file parsed by plyj.
    '''

    def __init__(self):
        super(SourceElement, self).__init__()
        self._fields = []
        global idg
        idg+=1
        self.id = idg

    def __repr__(self):
        equals = ("{0}={1!r}".format(k, getattr(self, k))
                  for k in self._fields)
        args = ", ".join(equals)
        args = args + ", "+str(self.id)
        return "{0}({1})".format(self.__class__.__name__, args)

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self == other

    def accept(self, visitor):
        """
        default implementation that visit the subnodes in the order
        they are stored in self_field
        """
        class_name = self.__class__.__name__
        visit = getattr(visitor, 'visit_' + class_name)
        if visit(self):
            for f in self._fields:
                field = getattr(self, f)
                if field:
                    if isinstance(field, list):
                        for elem in field:
                            if isinstance(elem, SourceElement):
                                elem.accept(visitor)
                    elif isinstance(field, SourceElement):
                        field.accept(visitor)
        getattr(visitor, 'leave_' + class_name)(self)

class node:
    def __init__(self,*args):
        global graph
        global idg
        node_a = pydot.Node(args[1],label=args[0])
        graph.add_node(node_a)
        for x in args[2:]:
            y = [1,2]
            z = "Abhinav and Anuj were here!!"
            if x:
                if type(x) == type(y):
                    for k in x:
                        if type(k) == type(z):
                            idg+=1;
                            node_b = pydot.Node(idg,label=k)
                            graph.add_node(node_b)
                            graph.add_edge(pydot.Edge(node_a,node_b))
                        else:
                            graph.add_edge(pydot.Edge(node_a,pydot.Node(k.id)))
                elif type(x) == type(z):
                    idg+=1;
                    node_b = pydot.Node(idg,label=x)
                    graph.add_node(node_b)
                    graph.add_edge(pydot.Edge(node_a,node_b))
                else:
                    graph.add_edge(pydot.Edge(node_a,pydot.Node(x.id)))
def printing():
    global graph
    graph.write_png('./AST.png')

class CompilationUnit(SourceElement):

    def __init__(self, package_declaration=None, import_declarations=None,
                 type_declarations=None):
        super(CompilationUnit, self).__init__()
        node("CompilationUnit",self.id,package_declaration, import_declarations, type_declarations)
        self._fields = [
            'package_declaration', 'import_declarations', 'type_declarations','type']
        if import_declarations is None:
            import_declarations = []
        if type_declarations is None:
            type_declarations = []
        self.package_declaration = package_declaration
        self.import_declarations = import_declarations
        self.type_declarations = type_declarations
        self.type = 'void'

class PackageDeclaration(SourceElement):

    def __init__(self, name, modifiers=None):
        super(PackageDeclaration, self).__init__()
        node("PackageDeclaration",self.id, name,modifiers)
        self._fields = ['name', 'modifiers', 'type']
        if modifiers is None:
            modifiers = []
        self.name = name
        self.modifiers = modifiers
        self.type = 'void'

class ImportDeclaration(SourceElement):

    def __init__(self, name, static=False, on_demand=False):
        super(ImportDeclaration, self).__init__()
        node("ImportDeclaration",self.id, name)
        self._fields = ['name', 'static', 'on_demand', 'type']
        self.name = name
        self.static = static
        self.on_demand = on_demand
        self.type = 'void'

class ClassDeclaration(SourceElement):

    def __init__(self, name, body, modifiers=None, type_parameters=None,
                 extends=None, implements=None):
        super(ClassDeclaration, self).__init__()
        node("ClassDeclaration",self.id, name,body, modifiers, type_parameters,extends, implements)
        self._fields = ['name', 'body', 'modifiers',
                        'type_parameters', 'extends', 'implements', 'type']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if implements is None:
            implements = []
        self.name = name
        self.body = body
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extends = extends
        self.implements = implements
        self.type = 'void'

class ClassInitializer(SourceElement):

    def __init__(self, block, static=False):
        super(ClassInitializer, self).__init__()
        node("ClassInitializer",self.id, block)
        self._fields = ['block', 'static', 'type']
        self.block = block
        self.static = static
        self.type = 'void'

class ConstructorDeclaration(SourceElement):

    def __init__(self, name, block, modifiers=None, type_parameters=None,
                 parameters=None, throws=None):
        super(ConstructorDeclaration, self).__init__()
        node("ConstructorDeclaration",self.id, name,block, modifiers, type_parameters,parameters, throws)
        self._fields = ['name', 'block', 'modifiers',
                        'type_parameters', 'parameters', 'throws', 'type']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if parameters is None:
            parameters = []
        self.name = name
        self.block = block
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.parameters = parameters
        self.throws = throws
        self.type = 'void'

class EmptyDeclaration(SourceElement):
    pass

class FieldDeclaration(SourceElement):

    def __init__(self, type, variable_declarators, modifiers=None):
        super(FieldDeclaration, self).__init__()
        node("FieldDeclaration",self.id, type, variable_declarators, modifiers)
        self._fields = ['type', 'variable_declarators', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.type = type
        self.variable_declarators = variable_declarators
        self.modifiers = modifiers
        global ST
        for x in self.variable_declarators:
            if x.initializer and self.type != x.initializer.type:
                sys.exit("Variable "+x.variable.name+" not initialized properly")
            if self.type.__class__ is str:
                ST.Add('variables',x.variable.name,x.variable.dimensions,self.type,self.modifiers)
            else:
                #to handle type casting
                ST.Add('variables',x.variable.name,x.variable.dimensions,self.type.name.value,self.modifiers)

            #code to give symbol table the exact dimensions of an array
            if x.initializer and x.initializer.__class__ == ArrayCreation:
                dimensions = []
                width = 1
                for individual_dimension in x.initializer.dimensions:
                    dimensions = dimensions + [individual_dimension.place]
                    width *= int(individual_dimension.place)
                ST.SymbolTable[ST.scope]['variables'][x.variable.name]['dimension'] = dimensions
                ST.SymbolTableFunction[ST.func]['variables'][x.variable.name+'_'+str(ST.scope)]['dimension'] = dimensions
                ST.offset = ST.offset + 4*(width-1)
                ST.SymbolTableFunction[ST.func]['variables'][x.variable.name+'_'+str(ST.scope)]['offset'] = ST.offset
                scope_var = ST.scope
                tac.emit(x.variable.name+'_'+str(scope_var),width,'','declare')

            elif x.initializer:
                #if x has a initializer than add it
                scope_var = ST.scope
                tac.emit(x.variable.name+'_'+str(scope_var),x.initializer.place,'','=')
       #pdb.set_trace()
        #print("sadf")

class MethodDeclaration(SourceElement):

    def __init__(self, name, modifiers=None, type_parameters=None,
                 parameters=None, return_type='void', body=None, abstract=False,
                 extended_dims=0, throws=None):
        super(MethodDeclaration, self).__init__()
        node("MethodDeclaration",self.id, name, modifiers, type_parameters,parameters, body, throws)
        self._fields = ['name', 'modifiers', 'type_parameters', 'parameters',
                        'return_type', 'body', 'abstract', 'extended_dims',
                        'throws','type']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if parameters is None:
            parameters = []
        self.name = name
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.parameters = parameters
        self.return_type = return_type
        self.body = body
        self.abstract = abstract
        self.extended_dims = extended_dims
        self.throws = throws
        self.type = 'void'

class FormalParameter(SourceElement):

    def __init__(self, variable, type, modifiers=None, vararg=False):
        super(FormalParameter, self).__init__()
        node("FormalParameter",self.id, variable, type, modifiers)
        self._fields = ['variable', 'type', 'modifiers', 'vararg']
        if modifiers is None:
            modifiers = []
        self.variable = variable
        self.type = type
        self.modifiers = modifiers
        self.vararg = vararg
        global ST
        ST.Add('variables',self.variable.name,[self.variable.dimensions],self.type,self.modifiers)


class Variable(SourceElement):
    # I would like to remove this class. In theory, the dimension could be added
    # to the type but this means variable declarations have to be changed
    # somehow. Consider 'int i, j[];'. In this case there currently is only one
    # type with two variable declarators;This closely resembles the source code.
    # If the variable is to go away, the type has to be duplicated for every
    # variable...

    def __init__(self, name, dimensions=0):
        super(Variable, self).__init__()
        node("Variable",self.id, name)
        self._fields = ['name', 'dimensions','type']
        self.name = name
        self.dimensions = dimensions
        self.type = 'void'


class VariableDeclarator(SourceElement):

    def __init__(self, variable, initializer=None):
        super(VariableDeclarator, self).__init__()
        node("VariableDeclarator",self.id, variable, initializer)
        self._fields = ['variable', 'initializer','type']
        self.variable = variable
        self.initializer = initializer
        self.type = 'void'

class Throws(SourceElement):

    def __init__(self, types):
        super(Throws, self).__init__()
        node("Throws",self.id, types)
        self._fields = ['types','type']
        self.types = types
        self.type = 'void'

class InterfaceDeclaration(SourceElement):

    def __init__(self, name, modifiers=None, extends=None, type_parameters=None,
                 body=None):
        super(InterfaceDeclaration, self).__init__()
        node("InterfaceDeclaration",self.id, name, modifiers, extends, type_parameters,body)
        self._fields = [
            'name', 'modifiers', 'extends', 'type_parameters', 'body', 'type']
        if modifiers is None:
            modifiers = []
        if extends is None:
            extends = []
        if type_parameters is None:
            type_parameters = []
        if body is None:
            body = []
        self.name = name
        self.modifiers = modifiers
        self.extends = extends
        self.type_parameters = type_parameters
        self.body = body
        self.type = 'void'

class EnumDeclaration(SourceElement):

    def __init__(self, name, implements=None, modifiers=None,
                 type_parameters=None, body=None):
        super(EnumDeclaration, self).__init__()
        node("EnumDeclaration",self.id,  name, implements, modifiers,type_parameters, body)
        self._fields = [
            'name', 'implements', 'modifiers', 'type_parameters', 'body', 'type']
        if implements is None:
            implements = []
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if body is None:
            body = []
        self.name = name
        self.implements = implements
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.body = body
        self.type = 'void'

class EnumConstant(SourceElement):

    def __init__(self, name, arguments=None, modifiers=None, body=None):
        super(EnumConstant, self).__init__()
        node("Throws",self.id,  name, arguments, modifiers, body)
        self._fields = ['name', 'arguments', 'modifiers', 'body', 'type']
        if arguments is None:
            arguments = []
        if modifiers is None:
            modifiers = []
        if body is None:
            body = []
        self.name = name
        self.arguments = arguments
        self.modifiers = modifiers
        self.body = body
        self.type = 'void'

class AnnotationDeclaration(SourceElement):

    def __init__(self, name, modifiers=None, type_parameters=None, extends=None,
                 implements=None, body=None):
        super(AnnotationDeclaration, self).__init__()
        node("AnnotationDeclaration",self.id, name, modifiers, type_parameters, extends,implements, body)
        self._fields = [
            'name', 'modifiers', 'type_parameters', 'extends', 'implements',
            'body', 'type']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if implements is None:
            implements = []
        if body is None:
            body = []
        self.name = name
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extends = extends
        self.implements = implements
        self.body = body
        self.type = 'void'

class AnnotationMethodDeclaration(SourceElement):

    def __init__(self, name, type, parameters=None, default=None,
                 modifiers=None, type_parameters=None, extended_dims=0):
        super(AnnotationMethodDeclaration, self).__init__()
        node("AnnotationMethodDeclaration", self.id, name, type, parameters, default, modifiers, type_parameters)
        self._fields = ['name', 'type', 'parameters', 'default',
                        'modifiers', 'type_parameters', 'extended_dims']
        if parameters is None:
            parameters = []
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        self.name = name
        self.type = type
        self.parameters = parameters
        self.default = default
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extended_dims = extended_dims

class Annotation(SourceElement):

    def __init__(self, name, members=None, single_member=None):
        super(Annotation, self).__init__()
        node("Annotation", self.id, name, members, single_member)
        self._fields = ['name', 'members', 'single_member', 'type']
        if members is None:
            members = []
        self.name = name
        self.members = members
        self.single_member = single_member
        self.type = 'void'


class AnnotationMember(SourceElement):

    def __init__(self, name, value):
        super(SourceElement, self).__init__()
        node("AnnotationMember", self.id, name, value)
        self._fields = ['name', 'value', 'type']
        self.name = name
        self.value = value
        self.type = 'void'

class Type(SourceElement):

    def __init__(self, name, type_arguments=None, enclosed_in=None,
                 dimensions=0):
        super(Type, self).__init__()
        node("Type",self.id, name, type_arguments, enclosed_in)
        self._fields = ['name', 'type_arguments', 'enclosed_in', 'dimensions']
        if type_arguments is None:
            type_arguments = []
        self.name = name
        self.type_arguments = type_arguments
        self.enclosed_in = enclosed_in
        self.dimensions = dimensions


class Wildcard(SourceElement):

    def __init__(self, bounds=None):
        super(Wildcard, self).__init__()
        node("Wildcard", self.id, bounds)
        self._fields = ['bounds', 'type']
        if bounds is None:
            bounds = []
        self.bounds = bounds
        self.type = 'void'


class WildcardBound(SourceElement):

    def __init__(self, type, extends=False, _super=False):
        super(WildcardBound, self).__init__()
        node("WildcardBound", self.id, type, extends)
        self._fields = ['type', 'extends', '_super']
        self.type = type
        self.extends = extends
        self._super = _super


class TypeParameter(SourceElement):

    def __init__(self, name, extends):
        super(TypeParameter, self).__init__()
        node("TypeParameter", self.id, name, extends)
        self._fields = ['name', 'extends']
        if extends is None:
            extends = []
        self.name = name
        self.extends = extends


class Expression(SourceElement):

    def __init__(self):
        super(Expression, self).__init__()
        self._fields = []

class BinaryExpression(Expression):

    def __init__(self, operator, lhs, rhs):
        super(BinaryExpression, self).__init__()
        node("BinaryExpression", self.id, operator, lhs, rhs)
        self._fields = ['operator', 'lhs', 'rhs','type','place','truelist','falselist']
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs
        if lhs.type == rhs.type:
            if not lhs.type == 'char':
                self.type = lhs.type
        elif ((lhs.type in ['double']) and (rhs.type in ['double','int'])) or ((rhs.type in ['double']) and (lhs.type in ['double','int'])) and operator != '=' :
            self.type = 'double'
        else:
            #pdb.set_trace()
            self.type = 'error'
            print("Type Error In Binary Expression")
            print("LHS is " + lhs.type)
            sys.exit("RHS is " + rhs.type)
        if operator != '=':
            name = ST.getTemp(self.type)
            self.place = name
            tac.emit(name, lhs.place, rhs.place, operator)
        else:
            self.place = rhs.place
            tac.emit(lhs.place,rhs.place,'',operator)

        relop = ['==','!=','<','>','<=','>=']
        if operator in relop:
            self.falselist = [len(tac.code)]
            tac.emit("ifgoto",self.place,'eq0','')
            self.truelist = [len(tac.code)]
            tac.emit("goto",'','','')
        else:
            self.truelist = []
            self.falselist =[]

class Assignment(BinaryExpression):
    pass


class Conditional(Expression):

    def __init__(self, predicate, if_true, if_false):
        super(self.__class__, self).__init__()
        node("Conditional", self.id, predicate, if_true, if_false)
        self._fields = ['predicate', 'if_true', 'if_false', 'type']
        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false
        if predicate.type in ['int','float','boolean','long','double'] and if_true.type == if_false.type:
            self.type = if_true.type
        elif predicate.type in ['int','float','boolean','long','double']:
            self.type = 'error'
            print("Type Error : Predicate Must Be A Boolean")
            sys.exit(predicate.type)
        else:
            self.type = 'error'
            print("Type Error")
            print(if_true.type)
            sys.exit(if_false.type)

class ConditionalOr(BinaryExpression):
    pass

class ConditionalAnd(BinaryExpression):
    pass

class Or(BinaryExpression):
    pass


class Xor(BinaryExpression):
    pass


class And(BinaryExpression):
    pass


class Equality(BinaryExpression):
    pass


class InstanceOf(BinaryExpression):
    pass


class Relational(BinaryExpression):
    pass


class Shift(BinaryExpression):
    pass


class Additive(BinaryExpression):
    pass


class Multiplicative(BinaryExpression):
    pass


class Unary(Expression):

    def __init__(self, sign, expression):
        super(Unary, self).__init__()
        node("Unary", self.id, sign, expression)
        self._fields = ['sign', 'expression','type', 'place']
        self.sign = sign
        self.expression = expression
        self.type = expression.type
        self.place = expression.place
        if not expression.type in ['int','float','boolean','long','double']:
            self.type = "error"
            sys.exit("Type Error In Unary Expression")
        temp = ST.getTemp(self.type)
        if "++" in sign or "--" in sign:
            if "++" == sign[1:3] or "--" == sign[1:3]:
                temp1 = ST.getTemp(self.type)
                tac.emit(temp1,expression.place,' ','=')
                self.place = temp1
            if "++" in sign:
                tac.emit(temp,expression.place,'1','+')
                tac.emit(expression.place, temp, ' ' , '=')
            elif "--" in sign:
                tac.emit(temp,expression.place,'1','-')
                tac.emit(expression.place, temp, ' ' , '=')
        elif "-" in sign:
            if self.expression.__class__ is Literal:
                self.place = '-' + self.expression.place
            else:
                tac.emit('neg',expression.place,' ',' ')
class Cast(Expression):

    def __init__(self, target, expression):
        super(Cast, self).__init__()
        node("Cast", self.id, target, expression)
        self._fields = ['target', 'expression','type','place']
        self.target = target
        self.expression = expression
        self.type = target.name
        self.place = expression.place

class Statement(SourceElement):
    pass

class Empty(Statement):
    pass


class Block(Statement):

    def __init__(self, statements=None):
        super(Statement, self).__init__()
        node("Block", self.id, statements)
        self._fields = ['statements','type']
        if statements is None:
            statements = []
        self.statements = statements
        self.type = 'void'

    def __iter__(self):
        for s in self.statements:
            yield s

class VariableDeclaration(Statement, FieldDeclaration):
    pass

class ArrayInitializer(SourceElement):
    def __init__(self, elements=None):
        super(ArrayInitializer, self).__init__()
        node("ArrayInitializer", self.id, elements)
        self._fields = ['elements','type']
        if elements is None:
            elements = []
        self.elements = elements
        self.type = elements.type

class MethodInvocation(Expression):
    def __init__(self, name, arguments=None, type_arguments=None, target=None):
        super(MethodInvocation, self).__init__()
        node("MethodInvocation", self.id, name, arguments, type_arguments, target)
        self._fields = ['name', 'arguments', 'type_arguments', 'target', 'type', 'place']
        if arguments is None:
            arguments = []
        if type_arguments is None:
            type_arguments = []
        self.name = name
        self.arguments = arguments
        self.type_arguments = type_arguments
        self.target = target
        #pdb.set_trace()
        if not target:
            global ST
            if not ST.Search('methods',name):
                self.type = None
                #pdb.set_trace()
                sys.exit(name + ' not declared in current scope')
            else:
                self.type = ST.Search('methods',name)
            scope_method = ST.getScope('methods',name)
            input_method = ST.SymbolTable[scope_method]['methods'][name]['dimension']
            if not len(input_method) == len(arguments):
                sys.exit(name + ' is called with incorrect number of arguments')
            for (x,y) in zip(input_method,arguments):
                if not x.type == y.type:
                    sys.exit(name + ' not called with correct argument type')
        else:
            self.type = 'undefined'

        for x in reversed(self.arguments):
            tac.emit('push',x.place,'','')
        tac.emit('call',name+str(len(arguments)),'','')
        temp = ST.getTemp(self.type)
        if ST.SymbolTableFunction[name]['type'] != 'void':
            tac.emit('pop',temp,'','')
        self.place = temp

class IfThenElse(Statement):

    def __init__(self, predicate, if_true=None, if_false=None):
        super(IfThenElse, self).__init__()
        node("IfThenElse", self.id, predicate, if_true, if_false)
        self._fields = ['predicate', 'if_true', 'if_false','type']
        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false
        self.type = 'void'
        if not predicate.type in ['int','float','boolean','long','double']:
            sys.exit("Boolean not provided inside if Statement")

class While(Statement):

    def __init__(self, predicate, body=None):
        super(While, self).__init__()
        node("While", self.id, predicate, body)
        self._fields = ['predicate', 'body', 'type']
        self.predicate = predicate
        self.body = body
        self.type = 'void'
        #pdb.set_trace()
        if not predicate.type in ['int','float','boolean','long','double']:
            sys.exit("Boolean not provided inside while Statement")

class For(Statement):

    def __init__(self, init, predicate, update, body):
        super(For, self).__init__()
        node("For", self.id, init, predicate, update, body)
        self._fields = ['init', 'predicate', 'update', 'body', 'type']
        self.init = init
        self.predicate = predicate
        self.update = update
        self.body = body
        self.type = 'void'
        #if predicate.type != update.type or update.type != init.type:
        #    print("Type Error : For Loops")

class ForEach(Statement):

    def __init__(self, type, variable, iterable, body, modifiers=None):
        super(ForEach, self).__init__()
        node("ForEach", self.id, type, variable, iterable, body, modifiers)
        self._fields = ['type', 'variable', 'iterable', 'body', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.type = type
        self.variable = variable
        self.iterable = iterable
        self.body = body
        self.modifiers = modifiers


class Assert(Statement):

    def __init__(self, predicate, message=None):
        super(Assert, self).__init__()
        node("Assert", self.id, predicate, message)
        self._fields = ['predicate', 'message','type']
        self.predicate = predicate
        self.message = message
        self.type = 'void'


class Switch(Statement):

    def __init__(self, expression, switch_cases):
        super(Switch, self).__init__()
        node("Switch", self.id, expression, switch_cases)
        self._fields = ['expression', 'switch_cases','type']
        self.expression = expression
        self.switch_cases = switch_cases
        self.type = 'void'

class SwitchCase(SourceElement):

    def __init__(self, cases, body=None):
        super(SwitchCase, self).__init__()
        node("SwitchCase", self.id, cases, body)
        self._fields = ['cases', 'body','type']
        if body is None:
            body = []
        self.cases = cases
        self.body = body
        self.type = 'void'

class DoWhile(Statement):

    def __init__(self, predicate, body=None):
        super(DoWhile, self).__init__()
        node("DoWhile", self.id, predicate, body)
        self._fields = ['predicate', 'body','type']
        self.predicate = predicate
        self.body = body
        self.type = 'void'


class Continue(Statement):

    def __init__(self, label=None):
        super(Continue, self).__init__()
        node("Continue", self.id, label)
        self._fields = ['label','type']
        self.label = label
        self.type = 'void'


class Break(Statement):

    def __init__(self, label=None):
        super(Break, self).__init__()
        node("Break", self.id, label)
        self._fields = ['label','type']
        self.label = label
        self.type = 'void'

class Return(Statement):

    def __init__(self, result=None):
        super(Return, self).__init__()
        node("Return", self.id, result)
        self._fields = ['result','type']
        self.type = 'void'
        self.result = result
        tac.emit('ret',result.place,'','')

class Synchronized(Statement):

    def __init__(self, monitor, body):
        super(Synchronized, self).__init__()
        node("Synchronized", self.id, monitor, body)
        self._fields = ['monitor', 'body', 'type']
        self.monitor = monitor
        self.body = body
        self.type = 'void'

class Throw(Statement):

    def __init__(self, exception):
        super(Throw, self).__init__()
        node("Throw", self.id, exception)
        self._fields = ['exception','type']
        self.exception = exception
        self.type = 'void'

class Try(Statement):

    def __init__(self, block, catches=None, _finally=None, resources=None):
        super(Try, self).__init__()
        node("Try", self.id, block, catches, _finally, resources)
        self._fields = ['block', 'catches', '_finally', 'resources','type']
        if catches is None:
            catches = []
        if resources is None:
            resources = []
        self.block = block
        self.catches = catches
        self._finally = _finally
        self.resources = resources
        self.type = 'void'

    def accept(self, visitor):
        if visitor.visit_Try(self):
            for s in self.block:
                s.accept(visitor)
        for c in self.catches:
            visitor.visit_Catch(c)
        if self._finally:
            self._finally.accept(visitor)


class Catch(SourceElement):

    def __init__(self, variable, modifiers=None, types=None, block=None):
        super(Catch, self).__init__()
        node("Catch", self.id, variable, modifiers, types, block)
        self._fields = ['variable', 'modifiers', 'types', 'block','type']
        if modifiers is None:
            modifiers = []
        if types is None:
            types = []
        self.variable = variable
        self.modifiers = modifiers
        self.types = types
        self.block = block
        self.type = 'void'

class Resource(SourceElement):

    def __init__(self, variable, type=None, modifiers=None, initializer=None):
        super(Resource, self).__init__()
        node("Resource", self.id, variable, type, modifiers, initializer)
        self._fields = ['variable', 'type', 'modifiers', 'initializer']
        if modifiers is None:
            modifiers = []
        self.variable = variable
        self.type = type
        self.modifiers = modifiers
        self.initializer = initializer


class ConstructorInvocation(Statement):
    """An explicit invocations of a class's constructor.
    This is a variant of either this() or super(), NOT a "new" expression.
    """

    def __init__(self, name, target=None, type_arguments=None, arguments=None):
        super(ConstructorInvocation, self).__init__()
        node("ConstructorInvocation", self.id, name, target, type_arguments, arguments)
        self._fields = ['name', 'target', 'type_arguments', 'arguments','type']
        if type_arguments is None:
            type_arguments = []
        if arguments is None:
            arguments = []
        self.name = name
        self.target = target
        self.type_arguments = type_arguments
        self.arguments = arguments
        self.type = 'void'

class InstanceCreation(Expression):

    def __init__(self, type, type_arguments=None, arguments=None, body=None,
                 enclosed_in=None):
        super(InstanceCreation, self).__init__()
        node("InstanceCreation", self.id, type, type_arguments, arguments, body, enclosed_in)
        self._fields = [
            'type', 'type_arguments', 'arguments', 'body', 'enclosed_in']
        if type_arguments is None:
            type_arguments = []
        if arguments is None:
            arguments = []
        if body is None:
            body = []
        self.type = type
        self.type_arguments = type_arguments
        self.arguments = arguments
        self.body = body
        self.enclosed_in = enclosed_in


class FieldAccess(Expression):

    def __init__(self, name, target):
        super(FieldAccess, self).__init__()
        node("FieldAccess", self.id, name, target)
        self._fields = ['name', 'target', 'type']
        self.name = name
        self.target = target
        self.type = name.type

class ArrayAccess(Expression):

    def __init__(self, index, target):
        super(ArrayAccess, self).__init__()
        node("ArrayAccess", self.id, index, target)
        self._fields = ['index', 'target','type','depth','dimension','place','len','pass_dimension']
        self.index = index
        self.target = target
        self.type = target.type
        global ST
        if target.__class__ == ArrayAccess:
            self.depth = target.depth +1
            self.dimension = target.dimension
        else:
            self.depth = 1
            scope_method = ST.getScope('variables',target.value)
            self.dimension = ST.SymbolTable[scope_method]['variables'][target.value]['dimension']
        if self.depth > self.dimension:
            sys.exit("More than allowed dimension accessed")
        if index.type not in 'int':
            sys.exit("Type Error : Array Indices Must Be Integer")
        #import pdb; pdb.set_trace()
        # this is tac code
        if self.depth == 1:
            #this line is for array name to get propogated to all array access
            self.array = target.place
            scope_method = ST.getScope('variables',target.value)
            dimensions = ST.SymbolTable[scope_method]['variables'][target.value]['dimension']
            self.pass_dimension = dimensions

            length = 1
            #import pdb; pdb.set_trace()
            for x in dimensions[self.depth:]:
                length *= int(x)
            temp = ST.getTemp('int')
            tac.emit(temp,index.place,4*length,'*')

            self.len = temp
            self.place = self.array + '['+temp+']'

        else:
            dimensions = target.pass_dimension
            length = 1
            for x in dimensions[self.depth:]:
                length *= int(x)
            temp = ST.getTemp('int')
            tac.emit(temp,index.place,4*length,'*')
            temp1  =ST.getTemp('int')
            #here we can optimize by using temo again
            tac.emit(temp1,temp,target.len,'+')
            self.place = temp1
            self.array = target.array
            if self.depth == len(dimensions):
                self.place = self.array + '['+temp1+']'
            self.pass_dimension = dimensions
            self.len = temp1

class ArrayCreation(Expression):

    def __init__(self, type, dimensions=None, initializer=None):
        super(ArrayCreation, self).__init__()
        node("ArrayCreation", self.id, type, dimensions, initializer)
        self._fields = ['type', 'dimensions', 'initializer']
        if dimensions is None:
            dimensions = []
        self.type = type
        self.dimensions = dimensions
        self.initializer = initializer


class Literal(SourceElement):

    def __init__(self, value):
        super(Literal, self).__init__()
        node("Literal", self.id, value)
        self._fields = ['value' , 'type', 'place']
        self.value = value
        self.place = value
        if value[0] == "'":
            self.type = 'char'
        elif self.value.find('.') == 1:
            self.type = 'double'
        else:
            self.type = 'int'

class ClassLiteral(SourceElement):

    def __init__(self, type):
        super(ClassLiteral, self).__init__()
        node("ClassLiteral", self.id, type)
        self._fields = ['type']
        self.type = type


class Name(SourceElement):

    def __init__(self, value):
        super(Name, self).__init__()
        node("Name",self.id, value)
        self._fields = ['value', 'type', 'place']
        self.value = value
        global ST
        if not ST.Search('variables',value):
            #pdb.set_trace()
            self.type = 'error'
            sys.exit(value + ' not declared in current scope')
        else:
            self.type = ST.Search('variables',value)
        self.place = value + '_'+str(ST.getScope('variables',value))

    def append_name(self, name):
        try:
            self.value = self.value + '.' + name.value
        except:
            self.value = self.value + '.' + name


class ExpressionStatement(Statement):
    def __init__(self, expression):
        super(ExpressionStatement, self).__init__()
        node("ExpressionStatement", self.id, expression)
        self._fields = ['expression','type']
        self.expression = expression
        self.type = 'void'
