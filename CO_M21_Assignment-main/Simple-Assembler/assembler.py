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

# dictionary for opcodes
opcodesA={'add':'00000','sub':'00001','mul':'00110','xor':'01010','or':'01011','and':'01100'}
opcodesB={'mov':'00010','rs':'01000','ls':'01001'}
opcodesC={'mov':'00011','div':'00111','not':'01101','cmp':'01110'}
opcodesD={'ld':'00100','st':'00101'}
opcodesE={'jmp':'01111','jlt':'10000','jgt':'10001','je':'10010'}
opcodesF={'hlt':'1001100000000000'}

# register dictionary
registers = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110', 'FLAGS':'111'}

# flags dictionary
Flags={'V':'0','L':'0','G':'0','E':'0'}

# function to return type of instruction
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

# function to check if register exists
def getrgst(reg):
    if(reg in registers.keys()):
        return registers[reg]
    else:
        print("Invalid register")
        sys.exit()

# function to print syntax error
def error():
    print("Wrong syntax used for instruction")
    sys.exit()

# function to convert immediates to binary
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

#to read input
instructions = sys.stdin.read()

def main():

    instruction = instructions.split("\n") # create list of instructions
    count = 0 # program counter
    varIn={} # to store variables
    labelIn={} # to store labels

# traversing the program once to store labels and their location
    for i in instruction:
        inst=i.split()
        if(len(inst)==0):
            continue
        if(':' in inst[0]):
            labelIn[(inst[0])[:-1]]=str(toBin(count))
        if (inst[0] != 'var')or(len(inst)==0):
            count += 1

    varerror=0 # to check is variables are not defined in the beginning

# traversing the program once to store variables and their location
    for i in instruction:
        ins = i.split()
        if (len(ins) == 0):
            continue
        if(ins[0]=='var'):
            if(len(ins)!=2):
                print("Variable not defined")
                sys.exit()
            varIn[ins[1]]=str(toBin(count))
            count+=1
            if(varerror==1):
                print("Variable not declared in beginning")
                sys.exit()
        else:
            varerror=1

# to check Misuse of labels as variables or vice-versa
    for key in varIn:
        if key in labelIn:
            print("Misuse of labels as variables or vice-versa")
            sys.exit()

    rslt="" # final output

    hlterror=0 # to check if hlt not being used as the last instruction

# print binary syntax
    for i in instruction:
        ins = i.split()

        if (len(ins) == 0): # to avoid empty lines
            continue

        if(hlterror==1):
            print("hlt not being used as the last instruction")
            sys.exit()

        if(ins[0] == "hlt"):
            hlterror=1
            if(len(ins)!=1): # check syntax of instruction, whether all arguments present or not
                error()
            rslt+="\n"+opcodesF['hlt']

        elif(':' in ins[0]): # to execute statements with labels
            if(len(ins)<1):
                print("empty label")
                sys.exit()
            if(ins[1]!='mov') and ('FLAGS' in ins): # Check illegal use of FLAG register
                print("Illegal use of FLAG register")
                sys.exit()
            if(ins[1]=="mov"):
                if (len(ins) != 4): # check syntax of instruction, whether all arguments present or not
                    error()
                opcodes = isType(ins[1],ins[3])
            else : opcodes=isType(ins[1])

            rslt+="\n"
            rslt+=opcodes[ins[1]]

            if(ins[1]=='hlt'):
                hlterror=1

            if opcodes == opcodesA:
                if(len(ins)!=5): # check syntax of instruction, whether all arguments present or not
                    error()
                rslt += '00'
                rslt += getrgst(ins[2])
                rslt += getrgst(ins[3])
                rslt += getrgst(ins[4])

            elif opcodes == opcodesB:
                if (len(ins) != 4): # check syntax of instruction, whether all arguments present or not
                    error()
                rslt = rslt+getrgst(ins[2])
                rslt = rslt+str(toBin(int((ins[3])[1:])))

            elif opcodes == opcodesC:
                if (len(ins) != 4): # check syntax of instruction, whether all arguments present or not
                    error()
                rslt = rslt + "00000" + getrgst(ins[2]) + getrgst(ins[3])

            elif opcodes == opcodesD:
                if (len(ins) != 4): # check syntax of instruction, whether all arguments present or not
                    error()
                try:
                    rslt = rslt + getrgst(ins[2]) + varIn[ins[3]]
                except KeyError:
                    print("Invalid variable")
                    sys.exit()

            elif opcodes == opcodesE:
                if (len(ins) != 3): # check syntax of instruction, whether all arguments present or not
                    error()
                if (ins[1] in varIn.keys()):
                    rslt = rslt + "000" + varIn[ins[2]]
                elif (ins[1] in labelIn.keys()):
                    rslt = rslt + "000" + labelIn[ins[2]]
                else:
                    print("Invalid label or variable")
                    sys.exit()

        elif(ins[0]=='var'): #skip variable instructions
            continue

        else:

            if (ins[0] != 'mov') and ('FLAGS' in ins): # Check illegal use of FLAG register
                print("Illegal use of FLAG register")
                sys.exit()

            if(ins[0]=="mov"):
                if (len(ins) != 3): # check syntax of instruction, whether all arguments present or not
                    error()
                opcodes = isType(ins[0],ins[2])
            else : opcodes=isType(ins[0])

            rslt+="\n"
            rslt+=opcodes[ins[0]]

            if opcodes == opcodesA:
                if(len(ins)!=4): # check syntax of instruction, whether all arguments present or not
                    error()
                rslt += '00'
                rslt += getrgst(ins[1])
                rslt += getrgst(ins[2])
                rslt += getrgst(ins[3])

            elif opcodes == opcodesB:
                if (len(ins) != 3): # check syntax of instruction, whether all arguments present or not
                    error()
                rslt = rslt+getrgst(ins[1])
                rslt = rslt+str(toBin(int((ins[2])[1:])))

            elif opcodes == opcodesC:
                if (len(ins) != 3): # check syntax of instruction, whether all arguments present or not
                    error()
                rslt = rslt + "00000" + getrgst(ins[1]) + getrgst(ins[2])

            elif opcodes == opcodesD:
                if (len(ins) != 3): # check syntax of instruction, whether all arguments present or not
                    error()
                try:
                    rslt = rslt + getrgst(ins[1]) + varIn[ins[2]]
                except KeyError:
                    print("Use of undefined Variable")
                    sys.exit()

            elif opcodes == opcodesE:
                if (len(ins) != 2): # check syntax of instruction, whether all arguments present or not
                    error()
                if(ins[1] in varIn.keys()):
                    rslt = rslt + "000" + varIn[ins[1]]
                elif (ins[1] in labelIn.keys()):
                    rslt = rslt + "000" + labelIn[ins[1]]
                else:
                    print("Invalid label or variable")
                    sys.exit()

    if(hlterror==0): # to check missing hlt instruction
        print("Missing hlt instruction")
        sys.exit()

    print(rslt) # print the final binary

if __name__=="__main__":
    main()
