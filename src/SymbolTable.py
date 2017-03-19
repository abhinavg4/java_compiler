import sys

class SymbolTable:

    def __init__(self):
        self.SymbolTable = [0,{
                'scope_name' : 'start',
                'variables' : {},
                'methods' : {},
                'classes': {},
                'type' : 'start',
                'parent' : 0,
            }
        ]
        self.scope = 1

    def AddVar(self, name, dimension, type, modifiers):
        curr_scope = self.getScopeOfVar(name)
        if curr_scope != self.scope:
            self.SymbolTable[self.scope]['variables'][name] = {
                'type' : type,
                'dimension' : dimension,
                'modifiers' : modifiers
            }
        else:
            sys.exit(name + 'Already present in current scope')

    def SearchVar(self, name):
        if(self.getTypeOfVar(name)):
            return self.getTypeOfVar(name)
        else:
            return None

    def getScopeOfVar(self,name):
        scope_curr = self.scope
        while scope_curr != 0:
            if name in self.SymbolTable[scope_curr]['variables']:
                return scope_curr
            scope_curr = self.SymbolTable[scope_curr]['parent']
        return 0

    def getTypeOfVar(self,name):
        scope_curr = self.scope
        while scope_curr != 0:
            if name in self.SymbolTable[scope_curr]['variables']:
                return self.SymbolTable[scope_curr]['variables'][name]['type']
            scope_curr = self.SymbolTable[scope_curr]['parent']
        return None

    def inc_scope(self):
        self.SymbolTable.append({
                'scope_name' : 'start',
                'variables' : {},
                'methods' : {},
                'classes': {},
                'type' : 'start',
                'parent' : self.scope,
            })
        self.scope +=1
        print(self.scope)

    def dec_scope(self):
        self.scope = self.SymbolTable[self.scope]['parent']
        self.SymbolTable.pop()
        print("dsfasd"+str(self.scope))
