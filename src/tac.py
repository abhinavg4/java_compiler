import sys
import pdb
import SymbolTable


global ST
ST = SymbolTable.SymbolTable()


class TAC:

    def __init__(self):
        self.labelCount = 0
        self.code = []

    def newLabel(self):
        label = "l" + str(self.labelCount)
        self.labelCount += 1
        return label

    def emit(self, lhs, rhs, rhs1, operator):
        rhs = str(rhs)
        rhs1 = str(rhs1)
        self.code.append([lhs,rhs,rhs1,operator])
        #import pdb; pdb.set_trace()
        if 'temp' == rhs[0:5]:
            ind = int(rhs[4])
            ST.tempNo[ind] = 0 #Free this temporary
        if 'temp' in rhs1[0:5]:
            ind = int(rhs1[4])
            ST.tempNo[ind] = 0 #Free this temporary


    def backpatch(self,list1,label):
        #pdb.set_trace()
        for x in list1:
            self.code[x][3] = label
