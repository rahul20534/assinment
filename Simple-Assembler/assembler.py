instructions ={
    "add" : {
        "type": "A",
        "opcode" : "00000",
    },
    "sub" : {
        "type": "A",
        "opcode" : "00001",
    },
    "mov" : {
        "type": "B",
        "opcode" : "00010",
    },
    # if performsmov register
    "mov1" : {
        "type": "C",
        "opcode" : "00011",
    },
    "ld" : {
        "type": "D",
        "opcode" : "00100",
    },
    "st" : {
        "type": "D",
        "opcode" : "00101",
    },
    "mul" : {
        "type": "A",
        "opcode" : "00110",
    },
    "div" : {
        "type": "A",
        "opcode" : "00111",
    },
    "rs" : {
        "type": "B",
        "opcode" : "01000",
    },
    "ls" : {
        "type": "B",
        "opcode" : "01001",
    },
    "xor" : {
        "type": "A",
        "opcode" : "01010",
    },
    "or" : {
        "type": "A",
        "opcode" : "01011",
    },
    "and" : {
        "type": "A",
        "opcode" : "01100",
    },
    "not" : {
        "type": "C",
        "opcode" : "01101",
    },
    "cmp" : {
        "type": "C",
        "opcode" : "01110"
    },
    "jmp" : {
        "type": "E",
        "opcode" : "01111",
    },
    "jlt" :{
        "type": "E",
        "opcode" : "10000"
    },
    "jgt" : {
        "type": "E",
        "opcode" : "10001"
    },
    "je" : {
        "type": "E",
        "opcode" : "10010"
    },
    "hlt":{
        "type": "F",
        "opcode" : "10011"
    }
}

register ={
    "R0" : "000",
    "R1" : "001",
    "R2" : "010",
    "R3" : "011",
    "R4" : "100",
    "R5" : "101",
    "R6" : "110",
    "FLAGS" : "111",
    
}
variables = dict()
labels = []

def assembler(line,count,finalcount,flag1,flag2,temp):
   
    with open('stdout.txt', 'a') as f:
        temp = False

        input_arr = line.split()

        if input_arr[0]=="hlt":
            temp = True

        if input_arr[0] == "mov":
            if (not input_arr[2][0]=="$"):
                input_arr[0]="mov2"

        if input_arr[0]=="var":
            variables[input_arr[1]] = int(count) 

        if input_arr[0] not in instructions and input_arr[0][:-1]==":":
            if input_arr[0][0:-2] in variables:
                print ("Misuse of label as a variable"+"at line"+str(count))
            else:
                input_arr[0] = input_arr[0][1:]
                labels.append(input_arr[0])  

        if "FLAGS" in input_arr and not input_arr[0]=="mov":
            print("Illegal use of FLAGS Register"+"at line"+str(count))
        
        if input_arr[0]=="var" and flag2 ==True:
            print("Variables not declared at the beginning"+"at line"+str(count))

        if input_arr[0] in instructions:

            if flag1==False:
                flag1=True
                flag2=True

            if instructions[input_arr[0]]["type"] == "A":
                if len(input_arr)!=4:
                    print("Wrong Syntax for this type of instruction"+"at line"+str(count))
                if input_arr[1] not in register or input_arr[2] not in register or input_arr[3] not in register:
                    print("Typo in Register Name"+"at line"+str(count))
            
                print(instructions[input_arr[0]]["opcode"]+"00"+register[input_arr[1]]+register[input_arr[2]]+register[input_arr[3]])
            
            elif instructions[input_arr[0]]["type"] == "B":
                if len(input_arr)!=3:
                    print("Wrong Syntax for this type of instruction"+"at line"+str(count))

                if input_arr[1] not in register:
                    print("Typo in Register Name"+"at line"+str(count))

                if int(input_arr[2][1:])<0 or int(input_arr[2][1:])>255:
                    print("Illegal Immediate Value"+"at line"+str(count))

                print(instructions[input_arr[0]]["opcode"]+register[input_arr[1]]+'{0:08b}'.format(int(input_arr[2][1:])))
            
            elif instructions[input_arr[0]]["type"] == "C":
                if len(input_arr)!=3:
                    print("Wrong Syntax for this type of instruction"+"at line"+str(count))
                if input_arr[1] or input_arr[2] not in register:
                    print("Typo in Register Name"+"at line"+str(count))
                print(instructions[input_arr[0]]["opcode"]+"00000"+register[input_arr[1]]+register[input_arr[2]])
            elif instructions[input_arr[0]]["type"] == "D":
                if len(input_arr)!=3:
                    print("Wrong Syntax for this type of instruction"+"at line"+str(count))
                if input_arr[2] not in variables:
                    print("Use of Undefined Variable"+"at line"+count)
                if input_arr[1] not in register:
                    print("Typo in Register Name"+"at line"+count)
                print(instructions[input_arr[0]]["opcode"]+register[input_arr[1]]+'{0:08b}'.format((finalcount-len(variables))+variables[input_arr[2]]))
            elif instructions[input_arr[0]]["type"] == "E":
                if len(input_arr)!=2:
                    print("Wrong Syntax for this type of instruction"+"at line"+str(count))
                if input_arr[2] not in variables:
                    print("Use of Undefined Variable"+"at line"+str(count))
                if input_arr[2] not in labels:
                    print("Use of Undefined Labels"+"at line"+str(count))
                print(instructions[input_arr[0]]["opcode"]+"000"+input_arr[1])

            elif instructions[input_arr[0]]["type"] == "F":
                
                if len(input_arr)!=1:
                    print("Wrong Syntax for this type of instruction"+"at line"+str(count))

                if count != finalcount:
                    print("hlt not being used as last instruction"+"at line"+str(count))

                print(instructions[input_arr[0]]["opcode"]+"0"*11)
            
            else:
                print("Typos in Instruction name"+"at line"+str(count))
        
        
        if input_arr[0] not in instructions and input_arr[0] != "var" and input_arr[0][:-1]!=":" :
            print("General Syntax Error"+str(count))

            
        

# Assembler's function

# Code to read file from EOD Line wise.
def main():
    finalcount = 0 #Size of File Line Wise
    count = 0
    with open('Simple-Assembler/stdin.txt' , 'r') as f1:
        for line in f1:
            finalcount += 1

    temp = False
    flag1 = False
    flag2 = False    
    with open('Simple-Assembler/stdin.txt', 'r') as f1:
        for line in f1:
            if line == '': # If empty string is read then stop the loop
                break
            count+=1
            assembler(line,count,finalcount,flag1,flag2,temp) # perform some operation(s) on given string
        if temp == False:
                print("Missing hlt instruction")

if __name__ == '__main__':
	main()




    