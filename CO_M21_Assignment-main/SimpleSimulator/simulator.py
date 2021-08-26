import sys
import matplotlib.pyplot as plt

x=[]
y=[]

regv = {'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0, 'R5': 0, 'R6': 0, 'FV':0 , 'FL':0, 'FG':0, 'FE':0}
# FV , FL , FG , FE is flag register for overflow, less than, greater than, equal to

reg = {'000':'R0' , '001': 'R1', '010': 'R2', '011': 'R3', '100': 'R4', '101': 'R5', '110': 'R6', '111':'FLAGS'}

typeofins={'00000':'A','00001':'A','00010':'B','00011':'C','00100':'D','00101':'D','00110':'A','00111':'C',
      '01000':'B','01001':'B','01010':'A','01011':'A','01100':'A','01101':'C','01110':'C','01111':'E',
      '10000':'E','10001':'E','10010':'E','10011':'F'}
mem={}
lst=[]

def toBin(a):
    if(a>0):
        if(a>255):
            print("illegal immediate value")
            sys.exit()
        bn = bin(a).replace('0b','')
        x = bn[::-1]
        while len(x) < 16:
            x += '0'
        bn = x[::-1]
    else:
        if(a<-256):
            print("Illegal Immediate values")
            sys.exit()
        bn = bin(a).replace('0b','')
        bn=bn[1:]
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
    count=0
    for i in instructions:
        if(not(i and i.strip())):
            continue
        print(i)
        count=count+1
    i=0
    while(i!=len(mem)):
        x=mem[str(pcout(count))]
        print(toBin(x))
        count=count+1
        i=i+1
    while(count!=256):
        print("0000000000000000")
        count=count+1

binary = sys.stdin.read()
instructions=binary.split("\n")
# with open('/Users/tanishqashitalsingh/Desktop/assignment-CO/CO_assignment/CO_M21_Assignment-main/automatedTesting/tests/bin/simple/test5','r') as f:
#     instruction = f.read()
# instructions = instruction.split("\n")

def main():
    pc = -1
    halt = False
    reset=0
    cycle=-1
    while(halt==False):
        cycle=cycle+1
        if reset == 1:
            pc+=1
            i=instructions[pc]
            ins=i[0:5]
            type=typeofins[ins]

            if(type=='A'):
                y.append(pc)
                reg1 = reg[i[7:10]]
                reg2 = reg[i[10:13]]
                reg3 = reg[i[13:16]]
                if(ins=='00000'):
                    regv[reg1]=regv[reg2]+regv[reg3]
                    if(regv[reg1]<0) or (regv[reg1]>255):
                        regv['FV']=1
                        regv[reg1]=0
                        reset = 1
                elif(ins=='00001'):
                    regv[reg1] = regv[reg2] - regv[reg3]
                    if(regv[reg1]<0) or (regv[reg1]>255):
                        regv['FV']=1
                        regv[reg1]=0
                        reset = 1
                elif(ins=='00110'):
                    regv[reg1] = regv[reg2] * regv[reg3]
                    if(regv[reg1]<0) or (regv[reg1]>255):
                        regv['FV']=1
                        regv[reg1]=0
                        reset = 1
                elif(ins=='01010'):
                    regv[reg1] = regv[reg2] ^ regv[reg3]
                elif (ins == '01011'):
                    regv[reg1] = regv[reg2] | regv[reg3]
                elif (ins == '01100'):
                    regv[reg1] = regv[reg2] & regv[reg3]
            elif(type== 'B'):
                y.append(pc)
                reg1 = reg[i[5:8]]
                immediate = int(i[8:16],2)
                if(ins=='00010'):
                    regv[reg1]=immediate
                    if(regv[reg1]<0) or (regv[reg1]>255):
                        regv['FV']=1
                        regv[reg1]=0
                        reset = 1
                elif(ins=='01000'):
                    regv[reg1] = regv[reg1]*2^(immediate)
                elif(ins=='01001'):
                    regv[reg1] = regv[reg1]/2^(immediate)
            elif(type== 'C'):
                y.append(pc)
                reg1 = reg[i[10:13]]
                reg2 = reg[i[13:16]]
                if(ins=='00011'):
                    if (reg2 == 'FLAGS'):
                        regv[reg1]=regv['FV']+regv['FL']+regv['FG']+regv['FE']
                    else:
                        regv[reg1]=regv[reg2]
                elif(ins=='00111'):
                    regv['R0']=regv[reg1]/regv[reg2]
                    regv['R1']=regv[reg1]%regv[reg2]
                elif(ins=='01101'):
                    regv[reg1] = ~regv[reg2]
                elif(ins=='01110'):
                    a=regv[reg1]
                    b=regv[reg2]
                    if(a==b):
                        regv['FE']=1
                        reset = 1
                    elif(a>b):
                        regv['FG']=1
                        reset = 1
                    elif(a<b):
                        regv['FL']=1
                        reset = 1
            elif(type=='D'):
                reg1=reg[i[5:8]]
                adr=i[8:16]
                y.append(int(adr))
                y.append(pc)
                x.append(cycle)
                if(ins=='00100'):
                    regv[reg1]=mem[adr]
                elif(ins=='00101'):
                    mem[adr]=regv[reg1]
            elif(type=='E'):
                adr=int(i[8:16],2)
                y.append(int(adr))
                y.append(pc)
                x.append(cycle)
                if(ins=='01111'):
                    pc=adr
                    pc=pc-1
                elif(ins=='10000'):
                    if(regv['FL']>0):
                        pc=adr
                        pc=pc-1
                elif(ins=='10001'):
                    if(regv['FG']>0):
                        pc=adr
                        pc=pc-1
                elif(ins=='10010'):
                    if(regv['FE']>0):
                        pc=adr
                        pc=pc-1
            elif(type=='F'):
                y.append(pc)
                halt=True

            regv['FE'] = 0
            regv['FV'] = 0
            regv['FL'] = 0
            regv['FG'] = 0
            reset = 0
            output(pc)
        else:
            reset = 0
            regv['FE'] = 0
            regv['FV'] = 0
            regv['FL'] = 0
            regv['FG'] = 0
            pc+=1
            i=instructions[pc]
            ins=i[0:5]
            type=typeofins[ins]
            if(type=='A'):
                y.append(pc)
                reg1 = reg[i[7:10]]
                reg2 = reg[i[10:13]]
                reg3 = reg[i[13:16]]
                if(ins=='00000'):
                    regv[reg1]=regv[reg2]+regv[reg3]
                    if(regv[reg1]<0) or (regv[reg1]>255):
                        regv['FV']=1
                        regv[reg1]=0
                        reset = 1
                elif(ins=='00001'):
                    regv[reg1] = regv[reg2] - regv[reg3]
                    if(regv[reg1]<0) or (regv[reg1]>255):
                        regv['FV']=1
                        regv[reg1]=0
                        reset = 1
                elif(ins=='00110'):
                    regv[reg1] = regv[reg2] * regv[reg3]
                    if(regv[reg1]<0) or (regv[reg1]>255):
                        regv['FV']=1
                        regv[reg1]=0
                        reset = 1
                elif(ins=='01010'):
                    regv[reg1] = regv[reg2] ^ regv[reg3]
                elif (ins == '01011'):
                    regv[reg1] = regv[reg2] | regv[reg3]
                elif (ins == '01100'):
                    regv[reg1] = regv[reg2] & regv[reg3]
            elif(type== 'B'):
                y.append(pc)
                reg1 = reg[i[5:8]]
                immediate = int(i[8:16],2)
                if(ins=='00010'):
                    regv[reg1]=immediate
                    if(regv[reg1]<0) or (regv[reg1]>255):
                        regv['FV']=1
                        regv[reg1]=0
                        reset = 1
                elif(ins=='01000'):
                    regv[reg1] = regv[reg1]*2^(immediate)
                elif(ins=='01001'):
                    regv[reg1] = regv[reg1]/2^(immediate)
            elif(type== 'C'):
                y.append(pc)
                reg1 = reg[i[10:13]]
                reg2 = reg[i[13:16]]
                if(ins=='00011'):
                    if (reg2 == 'FLAGS'):
                        regv[reg1] = regv['FV'] + regv['FL'] + regv['FG'] + regv['FE']
                    else:
                        regv[reg1] = regv[reg2]
                elif(ins=='00111'):
                    regv['R0']=regv[reg1]/regv[reg2]
                    regv['R1']=regv[reg1]%regv[reg2]
                elif(ins=='01101'):
                    regv[reg1] = ~regv[reg2]
                elif(ins=='01110'):
                    a=regv[reg1]
                    b=regv[reg2]
                    if(a==b):
                        regv['FE']=1
                        reset = 1
                    elif(a>b):
                        regv['FG']=1
                        reset = 1
                    elif(a<b):
                        regv['FL']=1
                        reset = 1
            elif(type=='D'):
                reg1=reg[i[5:8]]
                adr=i[8:16]
                y.append(int(adr))
                y.append(pc)
                x.append(cycle)
                if(ins=='00100'):
                    regv[reg1]=mem[adr]
                elif(ins=='00101'):
                    mem[adr]=regv[reg1]
            elif(type=='E'):
                adr=int(i[8:16],2)
                y.append(int(adr))
                y.append(pc)
                x.append(cycle)
                if(ins=='01111'):
                    pc=adr
                elif(ins=='10000'):
                    if(regv['FL']>0):
                        pc=adr
                elif(ins=='10001'):
                    if(regv['FG']>0):
                        pc=adr
                elif(ins=='10010'):
                    if(regv['FE']>0):
                        pc=adr
            elif(type=='F'):
                y.append(pc)
                halt=True
            output(pc)
            regv['FLAGS']=0
        x.append(cycle)
    memorydump()
    plt.scatter(x, y, c="blue")
    plt.show()

if __name__=="__main__":
    main()
