import sys
#binary = sys.stdin.read()

regv = {'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0, 'R5': 0, 'R6': 0, 'FV':0 , 'FL':0, 'FG':0, 'FE':0}
# FV , FL , FG , FE is flag register for overflow, less than, greater than, equal to

reg = {'000':'R0' , '001': 'R1', '010': 'R2', '011': 'R3', '100': 'R4', '101': 'R5', '110': 'R6', '111':'FLAGS'}

typeofins={'00000':'A','00001':'A','00010':'B','00011':'C','00100':'D','00101':'D','00110':'A','00111':'C',
      '01000':'B','01001':'B','01010':'A','01011':'A','01100':'A','01101':'C','01110':'C','01111':'E',
      '10000':'E','10001':'E','10010':'E','10011':'F'}

def toBin(a):
    if(a<0)or(a>255):
        print("Illegal Immediate values")
        sys.exit()
    bn = bin(a).replace('0b','')
    x = bn[::-1]
    while len(x) < 16:
        x += '0'
    bn = x[::-1]
    return bn

def pcout(a):
    if(a<0)or(a>255):
        print("Illegal Immediate values")
        sys.exit()
    bn = bin(a).replace('0b','')
    x = bn[::-1]
    while len(x) < 8:
        x += '0'
    bn = x[::-1]
    return bn

def output(pc):
    print(pcout(pc), end =" ")
    print(toBin(regv['R0']), end =" ")
    print(toBin(regv['R1']), end=" ")
    print(toBin(regv['R2']), end=" ")
    print(toBin(regv['R3']), end=" ")
    print(toBin(regv['R4']), end=" ")
    print(toBin(regv['R5']), end=" ")
    print(toBin(regv['R6']), end=" ")
    print('000000000000',end="")
    print(regv['FV'],end="")
    print(regv['FL'], end="")
    print(regv['FG'], end="")
    print(regv['FE'])

def memorydump():
    print(instruction)


with open('/Users/tanishqashitalsingh/Desktop/assignment-CO/CO_assignment/CO_M21_Assignment-main/automatedTesting/tests/bin/simple/test1','r') as f:
    instruction = f.read()
instructions = instruction.split("\n")

def main():
    pc = 0
    halt = False

    #instructions=binary.split('\n')

    for i in instructions:
        ins=i[0:5]
        type=typeofins[ins]
        if(type=='A'):
            reg1 = reg[i[7:10]]
            reg2 = reg[i[10:13]]
            reg3 = reg[i[13:16]]
            if(ins=='00000'):
                regv[reg1]=regv[reg2]+regv[reg3]
                if(regv[reg1]<0) or (regv[reg1]>255):
                    regv['FV']=1
            elif(ins=='00001'):
                regv[reg1] = regv[reg2] - regv[reg3]
                if (regv[reg1] < 0) or (regv[reg1] > 255):
                    regv['FV'] = 1
            elif(ins=='00110'):
                regv[reg1] = regv[reg2] * regv[reg3]
                if (regv[reg1] < 0) or (regv[reg1] > 255):
                    regv['FV'] = 1
            elif(ins=='01010'):
                regv[reg1] = regv[reg2] ^ regv[reg3]
            elif (ins == '01011'):
                regv[reg1] = regv[reg2] | regv[reg3]
            elif (ins == '01100'):
                regv[reg1] = regv[reg2] & regv[reg3]

        #add rest of instructions

        output(pc)
        pc=pc+1
        regv['FLAGS']=0
    memorydump()

if __name__=="__main__":
    main()





