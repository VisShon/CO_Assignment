# Type A:opcode(5),unnused(2),reg 1 (3),reg 2 (3),reg 3 (3)
#       Add, Sub, Multiply, Exclusive OR, OR ,And
# Type B:opcode(5),reg 1 (3),Immediate value(8)
#       Move immediate, Right Shift, Left Shift
# Type C:opcode(5),unnused(5),reg 1 (3),reg 2 (3)
#       Move Register, Divide, Invert, Compare
# Type D:opcode(5),reg 1 (3),Address(8)
#       Load, Store
# Type E:opcode(5),unnused(3),Address(8)
#       Unconditional jump, jump if </>/==
# Type F:opcode(5),unused(11)
#       hlt

import sys

opcodesA={'add':'00000','sub':'00001','mul':'00110','xor':'01010','or':'01011','and':'01100'}
opcodesB={'mov':'00010','rs':'01000','ls':'01001'}
opcodesC={'mov':'00011','div':'00111','not':'01101','cmp':'01110'}
opcodesD={'ld':'00100','st':'00101'}
opcodesE={'jmp':'01111','jlt':'10000','jgt':'10001','je':'10010'}
opcodesF={'hlt':'1001100000000000'}

registers = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110'}
# write for registers and flags

def isType(inst,val=" "):
    if(inst in opcodesA.keys()):
        return opcodesA
    elif(inst in opcodesB.keys()) and (val[0]=='$'):
        return opcodesB
    elif(inst in opcodesC.keys()):
        return opcodesC
    elif(inst in opcodesD.keys()):
        return opcodesD
    elif(inst in opcodesE.keys()):
        return opcodesE
    elif(inst in opcodesF.keys()):
        return opcodesF
    else:
        print("Invalid instruction")
        sys.exit()

def getrgst(reg):
    if(reg in registers.keys()):
        return registers[reg]
    else:
        print("Invalid register")
        sys.exit()

def error():
    print("Wrong syntax used for instruction")
    sys.exit()

with open('/Users/tanishqashitalsingh/Desktop/assignment-CO/CO_assignment/CO_M21_Assignment-main/automatedTesting/tests/assembly/errorGen/test2','r') as f:
    instructions = f.read()

def toBin(a):
    if(a<0)or(a>255):
        print("Illegal Immediate values")
        sys.exit()
    bn = bin(a).replace('0b','')
    x = bn[::-1]
    while len(x) < 8:
        x += '0'
    bn = x[::-1]
    return bn

def main():

# handel input

    instruction = instructions.split("\n")
    count = 0
    varIn={}
    labelIn={}
    addrType={}

#   traversing the program once to add labels, variables and addresses
    for i in instruction:
        inst=i.split()
        if(len(inst)==0):
            continue
        if(':' in inst[0]):
            labelIn[(inst[0])[:-1]]=str(toBin(count))
            #addrType[str(count)]=isType(inst[1])
        #elif(inst[0]=='hlt'):
            #addrType[str(count)] = isType(inst[0])
        #elif(inst[0]!='var'):
            #addrType[str(count)]=isType(inst[1])
        count+=1
    varerror=0
    for i in instruction:
        if (len(inst) == 0):
            continue
        if(inst[0]=='var'):
            varIn[inst[1]]=str(toBin(count))
            count+=1
            if(varerror==1):
                print("Variable not declared in beginning")
        else:
            varerror=1

    for key in varIn:
        if key in labelIn:
            print("Misuse of labels as variables or vice-versa")
            sys.exit()

    rslt=""
    hlterror=0
    for i in instruction:
        if (len(inst) == 0):
            continue
        if(hlterror==1):
            print("hlt not being used as the last instruction")
            sys.exit()
        ins=i.split()
        if(ins[0] == "hlt"):
            hlterror=1
            if(len(ins)!=1):
                error()
            rslt+="\n"+opcodesF['hlt']
        elif(':' in ins[0]):
            if(ins[1]=="mov"):
                if (len(ins) != 4):
                    error()
                opcodes = isType(ins[1],ins[3])
            else : opcodes=isType(ins[1])
            rslt+="\n"
            rslt+=opcodes[ins[1]]
            if opcodes == opcodesA:
                if(len(ins)!=5):
                    error()
                rslt += '00'
                rslt += getrgst(ins[2])
                rslt += getrgst(ins[3])
                rslt += getrgst(ins[4])
            elif opcodes == opcodesB:
                if (len(ins) != 4):
                    error()
                rslt = rslt+getrgst(ins[2])
                rslt = rslt+str(toBin(int((ins[3])[1:])))
            elif opcodes == opcodesC:
                if (len(ins) != 4):
                    error()
                rslt = rslt + "00000" + getrgst(ins[2])+getrgst(ins[3])
            elif opcodes == opcodesD:
                if (len(ins) != 4):
                    error()
                rslt = rslt + getrgst(ins[2]) + varIn[ins[3]]
            elif opcodes == opcodesE:
                if (len(ins) != 3):
                    error()
                rslt = rslt + "000" + varIn[ins[2]]
            
# here we will use that ra function with
# the elements in the  list ins other omitting the first element which is the label.
        else:
            if(ins[0]=="mov"):
                if (len(ins) != 3):
                    error()
                opcodes = isType(ins[0],ins[2])
            else : opcodes=isType(ins[0])
            rslt+="\n"
            rslt+=opcodes[ins[0]]
            if opcodes == opcodesA:
                if(len(ins)!=4):
                    error()
                rslt += '00'
                rslt += getrgst(ins[1])
                rslt += getrgst(ins[2])
                rslt += getrgst(ins[3])
            elif opcodes == opcodesB:
                if (len(ins) != 3):
                    error()
                rslt = rslt+getrgst(ins[1])
                rslt = rslt+str(toBin(int((ins[2])[1:])))
            elif opcodes == opcodesC:
                if (len(ins) != 3):
                    error()
                rslt = rslt + "00000" + getrgst(ins[1])+getrgst(ins[2])
            elif opcodes == opcodesD:
                if (len(ins) != 3):
                    error()
                rslt = rslt + getrgst(ins[1]) + varIn[ins[2]]
            elif opcodes == opcodesE:
                if (len(ins) != 2):
                    error()
                rslt = rslt + "000" + varIn[ins[1]]
    if(hlterror==0):
        print("Missing hlt instruction")
        sys.exit()
    print(rslt)

if __name__=="__main__":
    main()
