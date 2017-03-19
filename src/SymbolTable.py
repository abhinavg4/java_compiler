import sys
import pdb
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

    def Add(self,key, name, dimension, type, modifiers,less=0):#dimension wil have input parameters for a function
        if less:
            self.scope -= less
        curr_scope = self.getScope(key,name)
        if curr_scope != self.scope:
            self.SymbolTable[self.scope][key][name] = {
                'type' : type,
                'dimension' : dimension,
                'modifiers' : modifiers
            }
        else:
            sys.exit(name + 'Already present in current scope')
        if less:
            self.scope += less

    def Search(self, key, name):
        if(self.getType(key,name)):
            return self.getType(key,name)
        else:
            return None

    def getScope(self,key,name):
        scope_curr = self.scope
        while scope_curr != 0:
            if name in self.SymbolTable[scope_curr][key]:
                return scope_curr
            scope_curr = self.SymbolTable[scope_curr]['parent']
        return 0

    def getType(self,key,name):
        scope_curr = self.scope
        while scope_curr != 0:
            if name in self.SymbolTable[scope_curr][key]:
                return self.SymbolTable[scope_curr][key][name]['type']
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
