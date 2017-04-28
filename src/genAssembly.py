
from regalloc import *

frodNo = 0 #used for label numbering of COMPARE
reloplatest='-1' #used to store info for compare and jump
def printins(ins,op1,op2='0'):
    if ins == 'M':
        if op1 != op2: # To skip some redundant code like movl %ebx, %ebx
            print('\tmovl '+op1 +' , '+op2)
    elif ins == 'A':
        print('\taddl '+op1+' , '+op2)
    elif ins == 'S':
        print('\tsubl '+op1+' , '+op2)
    elif ins == "MUL":
        print('\timull '+op1+' , '+op2)
    elif ins == "L":
        print('\n'+op1+':')
    elif ins == "J":
        print('\tjmp '+op1)
    elif ins == "C":
        print('\tcmp '+op1+' , '+op2)
    elif ins == ">=":
        print('\tjge '+op1)
    elif ins == ">":
        print('\tjg '+op1)
    elif ins == "<=":
        print('\tjle '+op1)
    elif ins == "<":
        print('\tjl '+op1)
    elif ins == "==":
        print('\tje '+op1)
    elif ins == "!=":
        print('\tjne '+op1)

def nrelop(relop): #outputs the negation of reloplatest
    if relop == "==":
        return "!="
    if relop == "!=":
        return "=="
    if relop == "<=":
        return ">"
    if relop == "<":
        return ">="
    if relop == ">=":
        return "<"
    if relop == ">":
        return "<="

def ADDSUB(insNo,isadd=1):
    i=insNo
    if(isInt(tac.code[i][1]) or isInt(tac.code[i][2])):
        if(isInt(tac.code[i][1]) and isInt(tac.code[i][2])  ):
            a=regs(i,tac.code[i][0])
            printins("M",tac.code[i][1],a)
            if(isadd==1):
                printins("A",tac.code[i][2],a)
            else:
                printins("S",tac.code[i][2],a)
        elif(isInt(tac.code[i][1])):
            b=regs(i,tac.code[i][2], 1)
            a=regs(i,tac.code[i][0])
            printins("M",b,a)
            if(isadd==1):
                printins("A",tac.code[i][2],a)
            else:
                printins("S",tac.code[i][2],a)
        else:
            b=regs(i,tac.code[i][1], 1)
            a=regs(i,tac.code[i][0])
            printins("M",b,a)
            if(isadd==1):
                printins("A",tac.code[i][2],a)
            else:
                printins("S",tac.code[i][2],a)
    else:
        b=regs(i,tac.code[i][1], 1)
        c=regs(i,tac.code[i][2], 1)
        a=regs(i,tac.code[i][0])
        printins("M",c,a)
        if(isadd==1):
            printins("A",b,a)
        else:
            printins("S",b,a)

def MUL(insNo):
    i=insNo
    if(isInt(tac.code[i][1]) or isInt(tac.code[i][2])):
        if(isInt(tac.code[i][1]) and isInt(tac.code[i][2])):
            a=regs(i,tac.code[i][0])
            printins("M",tac.code[i][1],a)
            printins("MUL",tac.code[i][2],a)
        elif(isInt(tac.code[i][1])):
            b=regs(i,tac.code[i][2], 1)
            a=regs(i,tac.code[i][0])
            printins("M",b,a)
            printins("MUL",tac.code[i][1],a)
        else:
            b=regs(i,tac.code[i][1], 1)
            a=regs(i,tac.code[i][0])
            printins("M",b,a)
            printins("MUL",tac.code[i][2],a)
    else:
        b=regs(i,tac.code[i][1], 1)
        c=regs(i,tac.code[i][2], 1)
        a=regs(i,tac.code[i][0])
        printins("M",c,a)
        printins("I",b,a)
def EQUAL(insNo):
    i = insNo
    #Abhinav - Need to handle array here
    if(isInt(tac.code[i][1])):
        a=regs(i,tac.code[i][0])
        printins("M",tac.code[i][1],a)
        # print("movl $"+ g.splitins[i].src1 + " , " + str(a))
    else:
        if "temp" in tac.code[i][1]:
            b= regs(i, tac.code[i][1], 1)
            regalloc[regNo(b)] = tac.code[i][0]
            return

        a=regs(i, tac.code[i][0])
        b=regs(i, tac.code[i][1], 1)
        # print("movl "+ str(b) + " , " + str(a))
        printins("M",b,a)

def COMPARE(insNo):
    i=insNo
    #import pdb; pdb.set_trace()
    if(isInt(tac.code[i][1]) or isInt(tac.code[i][2])):
        if(isInt(tac.code[i][1]) and isInt(tac.code[i][2])  ):
            printins("C",tac.code[i][1],tac.code[i][2])
        elif(isInt(tac.code[i][1])):
            b=regs(i, tac.code[i][2], 1)
            printins("C",tac.code[i][1],b)
        else:
            b=regs(i, tac.code[i][1], 1)
            printins("C",b, tac.code[i][2])
    else:
        b=regs(i, tac.code[i][1], 1)
        c=regs(i, tac.code[i][2], 1)
        printins("C",b, c)
    global reloplatest
    reloplatest = nrelop(tac.code[i][3])

def IFGOTO(insNo):
    i = insNo
    #import pdb; pdb.set_trace()
    global reloplatest
    printins(reloplatest,tac.code[i][3])
#Converts every instruction to corresponding assembly code
def generate():
    flag=0
    fgl =0
    #Create data section of Assembly Code
    #g.debug(g.marker)
    # UNCOMMENTED
    # updatejumpttrgt()
    #print_functions()
    #import pdb; pdb.set_trace()
    for i in range(len(tac.code)):
        if(tac.code[i][1][:4]=="main"):
            print "\n_start:"
            flag=1
        elif(tac.code[i][3]=='+'):
            ADDSUB(i)
        elif(tac.code[i][3]=='-'):
            ADDSUB(i,0)
        elif(tac.code[i][3]=='*'):
            MUL(i)
        elif(tac.code[i][3]=='='):
            EQUAL(i)
        elif(tac.code[i][0]=='goto'):
            printins("J",tac.code[i][3])
        elif(tac.code[i][0]=='label :'):
            printins("L", tac.code[i][3])
        elif(tac.code[i][0]=="ifgoto"):
            IFGOTO(i)
        elif(tac.code[i][3]=='||' or tac.code[i][3]=='&&'):
            pass
        else:
            COMPARE(i)
