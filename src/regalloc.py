from model import *

regalloc = ['-1']*6
curr_procedure = ['empty']
flag_for_load = [0]
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


# This function should return a register after allocationg
def getreg(i, var):
    q=-1
    #if var == "b_3":
    #    import pdb; pdb.set_trace()
    if "temp" in tac.code[i][1]:
        for x in range(0,6):
            if(regalloc[x]==tac.code[i][1]):
                q = x
                regalloc[x] = '-1'
                break

    if "temp" in tac.code[i][2]:
        for x in range(0,6):
            if(regalloc[x]==tac.code[i][2]):
                q = x
                regalloc[x] = '-1'
                break

    if q != -1:
        return q

    for q in range(6):
        if regalloc[q] == '-1':
            return q
    flag_for_load[0] = 1;
    # Register Spilling
    for q in range(6):
        if(regalloc[q] != tac.code[i][0] and regalloc[q] != tac.code[i][1] and regalloc[q] != tac.code[i][2] and "temp" not in regalloc[q]):
            print('\tmov '+ regname(q) + ' , ' + '[ebp-' + str(ST.SymbolTableFunction[curr_procedure[0]]['variables'][str(regalloc[q])]['offset']) + ']')
            regalloc[q] = var
            return q

def loadreg(a, var):
        if flag_for_load[0] == 0:
            return
        #import pdb; pdb.set_trace()
        print('\tmov '+ '[ebp-' + str(ST.SymbolTableFunction[curr_procedure[0]]['variables'][var]['offset']) + ']' + ' , ' + regname(a))

# Assigns a register to varisble, var, if not already assigned and returns register name
def regs(i, var, load=0):
    flag_for_load[0] = 0
    tmp=isAssigned(var)
    if(tmp!="-1"):
        a=regname(tmp)
    else:
        a=getreg(i, var)
        if load == 1:
            loadreg(a, var)
        regalloc[a] = var
        a = regname(a)
    return a
