from regalloc import *

frodNo = 0 #used for label numbering of COMPARE
reloplatest='-1' #used to store info for compare and jump


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
            a=regs(i,tac.code[i][0],0,1)
            printins("M",tac.code[i][1],a)
            if(isadd==1):
                printins("A",tac.code[i][2],a)
            else:
                printins("S",tac.code[i][2],a)
        elif(isInt(tac.code[i][1])):
            b=regs(i,tac.code[i][2], 1)
            a=regs(i,tac.code[i][0],0,1)
            printins("M",b,a)
            if(isadd==1):
                printins("A",tac.code[i][2],a)
            else:
                printins("S",tac.code[i][2],a)
        else:
            b=regs(i,tac.code[i][1], 1)
            a=regs(i,tac.code[i][0],0,1)
            printins("M",b,a)
            if(isadd==1):
                printins("A",tac.code[i][2],a)
            else:
                printins("S",tac.code[i][2],a)
    else:
        b=regs(i,tac.code[i][1], 1)
        c=regs(i,tac.code[i][2], 1)
        a=regs(i,tac.code[i][0],0,1)
        printins("M",c,a)
        if(isadd==1):
            printins("A",b,a)
        else:
            printins("S",b,a)

def MUL(insNo):
    i=insNo
    b = -1
    c = -1
    b1 = getreg(i)
    c1 = getreg(i)
    if(c1==4 or b1==5):
        b1,c1 = c1,b1
    if (b1==4 or regalloc[4]=='-1'):
        b = 4
    if (c1==5 or regalloc[5]=='-1'):
        c = 5
    if(b==-1):
        printins("M","eax",regname(b1))
        regalloc[b1]=regalloc[4]
        regalloc[4]='-1'
    if(c==-1):
        printins("M","edx",regname(c1))
        regalloc[c1]=regalloc[5]
        regalloc[5]='-1'
    tmp=isAssigned(tac.code[i][1])
    if(tmp!="-1"):
        printins("M",regname(tmp),"eax")
        regalloc[4] = tac.code[i][1]
    tmp=isAssigned(tac.code[i][2])
    if(tmp!="-1"):
        printins("M",regname(tmp),"edx")
        regalloc[5] = tac.code[i][2]
    if(regalloc[4]=='-1'):
        if(isInt(tac.code[i][1])):
            printins("M",tac.code[i][1],"eax")
        else:
            if '[' in tac.code[i][1]:
                regsarrmul(4,tac.code[i][1])
            else:
                loadreg(4,tac.code[i][1])
    if(regalloc[5]=='-1'):
        if(isInt(tac.code[i][2])):
            printins("M",tac.code[i][2],"edx")
        else:
            if '[' in tac.code[i][1]:
                regsarrmul(5,tac.code[i][1])
            else:
                loadreg(5,tac.code[i][1])
    spillaregister(4)
    spillaregister(5)

    printins("MUL","edx")
    regalloc[4] = tac.code[i][0]
    removeregalloc(tac.code[i][0],4)
    regalloc[5] = '-1'



def EQUAL(insNo):
    i = insNo
    #Abhinav - Need to handle array here
    if(isInt(tac.code[i][1])):
        a=regs(i,tac.code[i][0],0,1)
        printins("M",tac.code[i][1],a)
        # print("movl $"+ g.splitins[i].src1 + " , " + str(a))
    else:
        #import pdb; pdb.set_trace()
        if "temp" == tac.code[i][1][0:4] and '[' not in tac.code[i][0]:
            b= regs(i, tac.code[i][1], 1)
            regalloc[regNo(b)] = tac.code[i][0]
            removeregalloc(tac.code[i][0], regNo(b))
            return

        b=regs(i, tac.code[i][1], 1)
        a=regs(i, tac.code[i][0],0,1)
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
    flag_for_pop=0
    fgl =0
    #Create data section of Assembly Code
    #g.debug(g.marker)
    # UNCOMMENTED
    # updatejumpttrgt()
    #print_functions()
    #import pdb; pdb.set_trace()
    print "section .text"
    print "\tglobal main"
    print("\textern printInt1")

    for i in range(len(tac.code)):
        #import pdb; pdb.set_trace()
        if(tac.code[i][0]=="func"):
            curr_procedure[0] = tac.code[i][1][:-1]
        if(tac.code[i][0]=="func"):
            if(tac.code[i][1][:4]=="main"):
                print "\nmain:"
            else:
                print"\n" + tac.code[i][1] + ":"
            print"\tpush ebp"
            print"\tmov ebp , esp"
            print"\tsub esp , 100"
        elif(tac.code[i][0]=="call"):
            spillbeforecall()
            print"\tcall " + tac.code[i][1]
            flag_for_pop = 1
            #import pdb; pdb.set_trace()
            #curr_procedure[1] = curr_procedure[0]
            #curr_procedure[0] = tac.code[i][1][:-1]
        elif(tac.code[i][0]=="pop" and flag_for_pop != 0):
            #import pdb; pdb.set_trace()
            regalloc[4] = tac.code[i][1]
            flag_for_pop = 0
        elif(tac.code[i][0]=="ret"):
            #import pdb; pdb.set_trace()
            #spillall()
            if curr_procedure[0] != "main":
                if isInt(tac.code[i][1]):
                    printins("M",tac.code[i][1],"eax")
                else:
                    tmp = isAssigned(tac.code[i][1])
                    if(tmp!='-1'):
                        printins("M",regname(tmp),"eax")
                    else:
                        if ST.SymbolTableFunction[curr_procedure[0]]['variables'][tac.code[i][1]]['offset'] > 0:
                            print('\tmov ' + 'eax' + ' , ' + '[ebp-' + str(ST.SymbolTableFunction[curr_procedure[0]]['variables'][tac.code[i][1]]['offset'])+']')
                        else:
                            print('\tmov ' + 'eax' + ' , ' + '[ebp+' + str(abs(ST.SymbolTableFunction[curr_procedure[0]]['variables'][tac.code[i][1]]['offset']))+']')
                printins("M","ebp","esp")
                print"\tpop ebp"
                print"\tret"
            else:
                print"\tpop ebp"
            #curr_procedure[0] = curr_procedure[1]
            spillall()
        elif(tac.code[i][0]=='push'):
            if(isInt(tac.code[i][1])):
                printins("P",tac.code[i][1])
                # print("mov $"+ g.splitins[i].src1 + " , " + str(a))
            else:
                a=regs(i, tac.code[i][1],1,0)
                # print("mov "+ str(b) + " , " + str(a))
                printins("P",a)

        elif(tac.code[i][3]=='+'):
            #import pdb; pdb.set_trace()
            ADDSUB(i)
        elif(tac.code[i][3]=='-'):
            ADDSUB(i,0)
        elif(tac.code[i][3]=='*'):
            MUL(i)
        elif(tac.code[i][3]=='='):
            #import pdb; pdb.set_trace()
            EQUAL(i)
        elif(tac.code[i][0]=='goto'):
            printins("J",tac.code[i][3])
        elif(tac.code[i][0]=='label :'):
            printins("L", tac.code[i][3])
        elif(tac.code[i][0]=="ifgoto"):
            IFGOTO(i)
        elif(tac.code[i][3]=='||' or tac.code[i][3]=='&&'):
            pass
        elif(tac.code[i][3]=='<'or tac.code[i][3]=='<='or tac.code[i][3]=='>'or tac.code[i][3]=='>='or tac.code[i][3]=='=='or tac.code[i][3]=='!='):
            COMPARE(i)
        elif(tac.code[i][0]=="neg"):
            printins("neg",tac.code[1])
            pass
        for arr in array_access:
            #import pdb; pdb.set_trace()
            printins("A","ebp",regname(arr[1]))
            printins("S",str(ST.SymbolTableFunction[curr_procedure[0]]['variables'][arr[2]]['offset']),regname(arr[1]))
            printins("M",regname(arr[0]),'['+ regname(arr[1])+ ']')
            regalloc[arr[0]] = '-1'
            regalloc[arr[1]] = '-1'
        array_access[:] = []


    print("\n\tmov eax , 1")
    print("\tmov ebx , 0")
    print("\tint 0x80")
