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

opcodesA={'add':'00000','sub':'00001','mul':'00110','xor':'01010','or':'01011','and':'01100'}
opcodesB={'mov':'00010','rs':'01000','ls':'01001'}
opcodesC={'mov':'00011','div':'00111','not':'01101','cmp':'01110'}
opcodesD={'ld':'00100','st':'00101'}
opcodesE={'jmp':'01111','jlt':'10000','jgt':'10001','je':'10010'}
opcodesF={'hlt':'1001100000000000'}

registers = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110'}
# write for registers and flags

def isType(inst,val=""):
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


with open('/Users/tanishqashitalsingh/Desktop/assignment-CO/CO_assignment/CO_M21_Assignment-main/automatedTesting/tests/assembly/simpleBin/test4','r') as f:
    instructions = f.read()

def toBin(a):
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

    rslt=""
    num=0
    for i in instruction:
        ins=i.split()
        if(ins[0]=="hlt"):
            rslt+="\n"+opcodesF['hlt']
        elif(':' in ins[0]):
            pass
# here we will use that ra function with
# the elements in the  list ins other omitting the first element which is the label.
        else:
            if(ins[0]=="mov"):
                opcodes = isType(ins[0],ins[2])
            else : opcodes=isType(ins[0])
            rslt+="\n"
            rslt+=opcodes[ins[0]]
            if(opcodes==opcodesA):
                rslt+='00'
                rslt+=registers[ins[1]]
                rslt+=registers[ins[2]]
                rslt+=registers[ins[3]]
            elif(opcodes==opcodesB):
                rslt=rslt+registers[ins[1]]
                rslt=rslt+str(toBin(int((ins[2])[1:])))
            elif(opcodes==opcodesC):
                rslt=rslt+"00000"+registers[ins[1]]+registers[ins[2]]
            elif(opcodes==opcodesD):
                rslt = rslt + registers[ins[1]] + varIn[ins[2]]
            elif(opcodes==opcodesE):
                rslt = rslt + "000" + varIn[ins[1]]

    print(rslt)

if __name__=="__main__":
    main()