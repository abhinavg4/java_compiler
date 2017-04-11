import sys
class TAC:

    def __init__(self):
        self.labelCount = 0
        self.code = []

    def newLabel(self):
        label = "l" + str(self.labelCount)
        self.labelCount += 1
        return label

    def emit(self, lhs, rhs, rhs1, operator):
        self.code.append([lhs,rhs,rhs1,operator])
