
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
            'input' : None,
            'offset' : 0
        }
        self.func = 'start'
        self.scope = 1
        self.new_s = 1
        self.tempNo = [0]*500 #0 implies available
        self.labelNo = 1
        self.offset = 0

    def Add(self,key, name, dimension, type, modifiers,less=0):#dimension wil have input parameters for a function
        if less:
            store_scope = self.scope
            self.scope = self.SymbolTable[self.scope]['parent']
        curr_scope = self.getScope(key,name)
        if curr_scope != self.scope or (key == 'methods' and self.SymbolTable[self.scope][key][name]['modifiers'] == 'abs'):
            self.SymbolTable[self.scope][key][name] = {
                'type' : type,
                'dimension' : dimension,
                'modifiers' : modifiers
            }
        else:
            sys.exit('Scope Error : ' + name + ' already present in current scope')
        if key == 'methods':
            self.SymbolTableFunction[self.func]['type'] = type
            self.SymbolTableFunction[self.func]['input'] = dimension

        else:
            self.offset = self.offset + 4
            self.SymbolTableFunction[self.func]['variables'][name+"_"+str(self.scope)] = {
                'type' : type,
                'dimension' : dimension,
                'modifiers' : modifiers,
                'offset' : self.offset
            }
        if less:
            self.scope = store_scope

    def Search(self, key, name):
        if(self.getType(key,name)):
            return self.getType(key,name)
        else:
            return None

    def getTemp(self,type):
        ind = 0
        while self.tempNo[ind]!=0:
            ind = ind + 1
        self.tempNo[ind]=1 #mark this index as occupied
        name = 'temp' + str(ind)
        #self.Add('variables',name,0,type,None) Not adding temporaries t SymbolTable
        return name

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
            self.offset = 0
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

    def dec_scope(self):
        self.scope = self.SymbolTable[self.scope]['parent']
        #self.SymbolTable.pop()
    def makeMethodArgument(self):
        self.offset = 0;
        for x in self.SymbolTableFunction[self.func]['variables']:
            self.SymbolTableFunction[self.func]['variables'][x]['offset']= -1*self.SymbolTableFunction[self.func]['variables'][x]['offset'] - 4
    def new_label(self):
        label = 'label'+str(self.labelNo)
        self.labelNo+=1
        return label
