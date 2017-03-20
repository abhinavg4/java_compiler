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
        self.SymbolTableFunction = {}
        self.SymbolTableFunction['start'] = {
            'variables' : {},
            'type' : None,
            'input' : None
        }
        self.func = 'start'
        self.scope = 1
        self.new_s = 1
        
    def Add(self,key, name, dimension, type, modifiers,less=0):#dimension wil have input parameters for a function
        if less:
            store_scope = self.scope
            self.scope = self.SymbolTable[self.scope]['parent']
        curr_scope = self.getScope(key,name)
        if curr_scope != self.scope:
            self.SymbolTable[self.scope][key][name] = {
                'type' : type,
                'dimension' : dimension,
                'modifiers' : modifiers
            }
        else:
            sys.exit(name + 'Already present in current scope')
        if key == 'methods':
            self.SymbolTableFunction[self.func]['type'] = type
            self.SymbolTableFunction[self.func]['input'] = dimension
        else:
            self.SymbolTableFunction[self.func]['variables'][name+"."+str(self.scope)] = {
                'type' : type,
                'dimension' : dimension,
                'modifiers' : modifiers
            }
        if less:
            self.scope = store_scope

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

    def inc_scope(self,name=None):
        if name:
            self.SymbolTableFunction[name] = {
                'variables' : {},
                }
            self.func = name
        self.SymbolTable.append({
                'scope_name' : 'start',
                'variables' : {},
                'methods' : {},
                'classes': {},
                'type' : 'start',
                'parent' : self.scope,
            })
        self.new_s +=1
        self.scope = self.new_s
        print(self.scope)

    def dec_scope(self):
        self.scope = self.SymbolTable[self.scope]['parent']
        #self.SymbolTable.pop()
        print("dsfasd"+str(self.scope))
