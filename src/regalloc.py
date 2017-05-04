from model import *

regalloc = ['-1']*6
curr_procedure = ['empty','main']
flag_for_load = [0]
array_access = []
counter = [0]
array_in_argument =[0]
def printins(ins,op1,op2='0'):
    if ins == 'M':
        if op1 != op2: # To skip some redundant code like mov ebx, ebx
            print('\tmov '+ op2 +' , '+op1)
    elif ins == 'A':
        print('\tadd '+op2+' , '+op1)
    elif ins == 'S':
        print('\tsub '+op2+' , '+op1)
    elif ins == "MUL":
        print('\timul '+ op1)
    elif ins == "L":
        spillbeforecall()
        print('\n'+op1+':')
        spillall()
    elif ins == "J":
        #import pdb; pdb.set_trace()
        spillbeforecall()
        print('\tjmp '+op1)
    elif ins == "C":
        #if isInt(op2):
        #    op1,op2 = op2,op1
        print('\tcmp '+op2+' , '+op1)
    elif ins == ">=":
        spillbeforecall()
        print('\tjge '+op1)
    elif ins == ">":
        spillbeforecall()
        print('\tjg '+op1)
    elif ins == "<=":
        spillbeforecall()
        print('\tjle '+op1)
    elif ins == "<":
        spillbeforecall()
        print('\tjl '+op1)
    elif ins == "==":
        spillbeforecall()
        print('\tje '+op1)
    elif ins == "!=":
        spillbeforecall()
        print('\tjne '+op1)
    elif ins == "P":
        print('\tpush ' +op1)
    elif ins=="neg":
        print('\tneg '+op1)
    elif ins=="AND":
        print('\tand '+op1 + ' , '+op2)
    elif ins == "DIV":
        print('\tdiv '+op1)

def isInt(x):
    x=str(x).strip(' ')
    if(x[0]=='-'):
        x=x[1:]
        return x.isdigit()
    else:
        return x.isdigit()

def isAssigned(var):
    for i in range(0,6):
        if(regalloc[i]==var):
            return i
    return "-1"

# Mapping register to some integer
def regname(regno):
    #ebx=1 ,ecx=2, esi=3, edi=4, eax=5, edx=6
    if(regno==0):
        return 'ebx'
    if(regno==1):
        return 'ecx'
    if(regno==2):
        return "esi"
    if(regno==3):
        return 'edi'
    if(regno==4):
        return 'eax'
    if(regno==5):
        return 'edx'

def regNo(regname):

    if(regname=="ebx"):
        return 0
    if(regname=="ecx"):
        return 1
    if(regname=="esi"):
        return 2
    if(regname=="edi"):
        return 3
    if(regname=="eax"):
        return 4
    if(regname=="edx"):
        return 5
def removeregalloc(var , i):
    for q in range(6):
        if q != i and regalloc[q] == var:
            regalloc[q]='-1'

def spillall(): #function o spill all the registers
    for q in range(6):
        regalloc[q] = '-1'
    return
def spillbeforecall():
    for q in range(6):
        if(regalloc[q]!='-1') and not "temp" in regalloc[q]:
        #Search for the function where the variable in that register was defined
            #if str(regalloc[q])=='i_11':
            #    import pdb; pdb.set_trace()
            if(ST.SymbolTableFunction[curr_procedure[0]]['variables'][str(regalloc[q])]['offset']<0):
                print('\tmov '+ '[ebp+' + str(abs(ST.SymbolTableFunction[curr_procedure[0]]['variables'][str(regalloc[q])]['offset'])) + ']' + ' , ' + regname(q))
            else:
                print('\tmov '+ '[ebp-' + str(ST.SymbolTableFunction[curr_procedure[0]]['variables'][str(regalloc[q])]['offset']) + ']' + ' , ' + regname(q))
        regalloc[q] = '-1'


def spillaregister(i):

    if(regalloc[i]!='-1') and not "temp" in regalloc[i]:
    #Search for the function where the variable in that register was defined
        if(ST.SymbolTableFunction[curr_procedure[0]]['variables'][str(regalloc[i])]['offset']<0):
           print('\tmov '+ '[ebp+' + str(abs(ST.SymbolTableFunction[curr_procedure[0]]['variables'][str(regalloc[i])]['offset'])) + ']' + ' , ' + regname(i))
        else:
           print('\tmov '+ '[ebp-' + str(ST.SymbolTableFunction[curr_procedure[0]]['variables'][str(regalloc[i])]['offset']) + ']' + ' , ' + regname(i))
    regalloc[i] = '-1'
# This function should return a register after allocationg
def getreg(i):
    q=-1
    #if var == "b_3":
    #    import pdb; pdb.set_trace()

    if q != -1:
        return q

    for q in range(6):
        if regalloc[q] == '-1':
            return q
    flag_for_load[0] = 1;
    # Register Spilling
    br = 0
    for q in range(6):
        if(regalloc[q] != tac.code[i][0] and regalloc[q] != tac.code[i][1] and regalloc[q] != tac.code[i][2] and "temp" not in regalloc[q]):
            #Search for the function where the variable in that register was defined
            for proc in ST.SymbolTableFunction:
                for var_names in ST.SymbolTableFunction[proc]['variables']:
                    if regalloc[q] == var_names:
                        req_procedure = proc
                        br = 1
                        break
                if ( br ==1 ):
                    break

            if(ST.SymbolTableFunction[req_procedure]['variables'][str(regalloc[q])]['offset']<0):
                print('\tmov '+ '[ebp+' + str(abs(ST.SymbolTableFunction[req_procedure]['variables'][str(regalloc[q])]['offset'])) + ']' + ' , ' + regname(q))
            else:
                print('\tmov '+ '[ebp-' + str(ST.SymbolTableFunction[req_procedure]['variables'][str(regalloc[q])]['offset']) + ']' + ' , ' + regname(q))
            regalloc[q] = '-1'
            return q
    for q in range(6):
        if "temp" not in regalloc[q]:
            #Search for the function where the variable in that register was defined
            for proc in ST.SymbolTableFunction:
                for var_names in ST.SymbolTableFunction[proc]['variables']:
                    if regalloc[q] == var_names:
                        req_procedure = proc
                        br = 1
                        break
                if ( br ==1 ):
                    break

            if(ST.SymbolTableFunction[req_procedure]['variables'][str(regalloc[q])]['offset']<0):
                print('\tmov '+ '[ebp+' + str(abs(ST.SymbolTableFunction[req_procedure]['variables'][str(regalloc[q])]['offset'])) + ']' + ' , ' + regname(q))
            else:
                print('\tmov '+ '[ebp-' + str(ST.SymbolTableFunction[req_procedure]['variables'][str(regalloc[q])]['offset']) + ']' + ' , ' + regname(q))
            regalloc[q] = '-1'
            return q


def loadreg(a, var):
    #if "temp" in var:
    #    import pdb; pdb.set_trace()
    if(ST.SymbolTableFunction[curr_procedure[0]]['variables'][var]['offset']<0):
        print('\tmov '+ regname(a) + ' , ' + '[ebp+' + str(abs(ST.SymbolTableFunction[curr_procedure[0]]['variables'][var]['offset'])) + ']')
    else:
        print('\tmov '+ regname(a) + ' , ' + '[ebp-' + str(ST.SymbolTableFunction[curr_procedure[0]]['variables'][var]['offset']) + ']')

def loadregarr(a, temp, var):
        if not regname(temp):
            import pdb; pdb.set_trace()
        if array_in_argument[0] == 1:
            printins("A",'[ebp+' + str(abs(ST.SymbolTableFunction[curr_procedure[0]]['variables'][var]['offset']))+']',regname(temp))
            printins("M",'['+ regname(temp)+ ']',regname(a))
        else:
            printins("A","ebp",regname(temp))
            printins("S",str(ST.SymbolTableFunction[curr_procedure[0]]['variables'][var]['offset']),regname(temp))
            printins("M",'['+ regname(temp)+ ']',regname(a))
        regalloc[temp] = '-1'
        array_access.append([a,"NOA",var])
        array_in_argument[0] = 0
# Assigns a register to varisble, var, if not already assigned and returns register name
def regsarrmul(a,var):
    counter[0] = counter[0] +1
    temp = var.partition('[')[-1].rpartition(']')[0]
    vari = var.split('[')
    var = vari[0]
        #if(var=="temp0"):
            #import pdb; pdb.set_trace()
    if isAssigned(temp) == '-1':
        import pdb; pdb.set_trace()
    loadregarr(a, isAssigned(temp),var)
    regalloc[a] = var + 'temp' + str(counter[0])

def regs(i, var, load=0, lhs=0):
    flag_for_load[0] = 0
    #if var == "r_4[temp35]":
        #import pdb; pdb.set_trace()
    if "[" in var:
        #import pdb; pdb.set_trace()
        counter[0] = counter[0] +1
        temp = var.partition('[')[-1].rpartition(']')[0]
        vari = var.split('[')
        var = vari[0]
        if ST.SymbolTableFunction[curr_procedure[0]]['variables'][var]['offset'] < 0:
            array_in_argument[0] = 1
        a=getreg(i)
        if load == 0:
            array_access.append([a,isAssigned(temp),var])
        if load == 1:
            #if(var=="temp0"):
                #import pdb; pdb.set_trace()
            loadregarr(a, isAssigned(temp),var)
        regalloc[a] = var + 'temp' + temp
        a = regname(a)
    else:
        tmp=isAssigned(var)
        #import pdb; pdb.set_trace()

        if(tmp!="-1"):
            a=regname(tmp)
        else:
            a=getreg(i)
            #import pdb; pdb.set_trace()
            if load == 1:
                #if(var=="temp0"):
                    #import pdb; pdb.set_trace()
                loadreg(a, var)
            #if not a:
            #    import pdb; pdb.set_trace()
            regalloc[a] = var
            a = regname(a)
    if lhs == 1:
        if "temp" == tac.code[i][1][0:4] and tac.code[i][1] != tac.code[i][0]:
            for x in range(0,6):
                if(regalloc[x]==tac.code[i][1]):
                    q = x
                    regalloc[x] = '-1'
                    break

        if "temp" == tac.code[i][2][0:4] and tac.code[i][2] != tac.code[i][0]:
            for x in range(0,6):
                if(regalloc[x]==tac.code[i][2]):
                    q = x
                    regalloc[x] = '-1'
                    break
    return a
