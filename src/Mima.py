import click
import ast

################################
#Exceptions
################################
class InvalidSyntax(Exception):
    def __init__(self, line):
        self.message = f"Invalid Syntax in line {line}"
    
class InvalidAdress(Exception):
    def __init__(self, address, line):
        self.message = f"The address *{address}* does not exist (line: {line})"
    
class InvalidNumber(Exception):
    def __init__(self, number):
        self.message = f"The number *{number}* is not a valid"

################################
#Two Complement System
################################
class TwoComplement:

    def __init__(self, length, value):
        self.length = length
        self.value = self.convert(value)

    def convert(self, num):
        firstBit = "0"

        if (len(num) > self.length):
            raise InvalidNumber(num)

        for i in num:
            if i != "1" and i != "0":
                raise InvalidNumber(num)

        if len(num) < self.length:
            num = "0" * (self.length - len(num)) + num

        return num

################################
#Other util methods
################################
        
#The Method defines the initial Storage size and creates placeholder cells
def defineStorageSize(count: int):
        storage = []
        for i in range(count):
            storage.append([i, 0])
        return storage

#The Method reads a files storage/code section, depending on the bool that is passed and returns the lines as array
def readFile(path: str, isCode: bool):
    if not path.endswith(".mima"):
        raise InvalidFile()

    result = []

    if not isCode:

        with open(path) as file:
            lines = file.readlines()

            for i in range(len(lines)):
                if (i > 0) and (lines[i-1].strip("\n") == "storage:"):
                    for line in lines[i:len(lines)]:
                        if line.strip("\n") == ":endStorage":
                            break
                        result.append(line.strip("\n"))
                    break
    else:
        with open(path) as file:
            lines = file.readlines()

            for i in range(len(lines)):
                if (i > 0) and (lines[i-1].strip("\n") == "code:"):
                    for line in lines[i:len(lines)]:
                        result.append(line.strip("\n"))
                    break

    return result        

################################
#MIMA Interpreter Class
################################
class MIMA:
    def __init__(self, storageSize: int, bits: int):
        self.storage = defineStorageSize(storageSize)
        self.akku = "0"
        self.bits = bits
        self.tokens = []
        self.line = 0

################################
#Basic functions
################################
    def findByAdress(self, adress):
        for i in self.storage:
            if i[0] == adress:  
                return self.storage.index(i)
        return -1

    def defineStorageName(self, adress, name: str):
        index = self.findByAdress(adress)
        self.storage[index][0] = name

    def writeToStorage(self, adress, value):
        value = TwoComplement(self.bits, value)
        index = self.findByAdress(adress)
        self.storage[index][1] = value

    def addNewStorageCell(self, name: str, value: str):
        self.storage.append([name, TwoComplement(self.bits, value)])

    def invert(self, value):
        inverted = ""
        for i in value:
            if i == "0":
                inverted += "1"
            elif i == "1":
                inverted += "0"
        return inverted

    def TwoComplementAddition(self, value: str):
        toAdd = [char for char in self.akku]
        valueList = [char for char in value]
        newValue = ["0" for _ in range(self.bits)]
        i = self.bits - 1
        temp = "0"
        
        while i >= 0:
            if toAdd[i] == "0" and valueList[i] == "0":
                newValue[i] = temp
                temp = "0"

            elif toAdd[i] != valueList[i]:
                if temp == "0":
                    newValue[i] = "1"
                else:
                    newValue[i] = "0"

            elif toAdd[i] == "1" and valueList[i] == "1":
                if temp == "0":
                    newValue[i] = "0"
                    temp = "1"
                else:
                    newValue[i] = "1"
            
            i -= 1
        
        i = self.bits - 1

        while temp == "1":
            if newValue[i] == "1":
                newValue[i] = "0"
            else:
                newValue[i] = "1"
                temp = "0"
            
            i -= 1

        return "".join(newValue)

################################
#Code Interpretation
################################
    def compile(self, path):
        if not path.endswith(".mima"):
            raise InvalidFile
        else:
            self.code = readFile(path, True)    

            line = 0
            runtimeStorage = []

            for codeSegment in self.code:
                line += 1
                i = codeSegment.strip("\n").split(" ")

                if i[0] in ["ADD", "LDV", "AND", "OR", "XOR", "EQL"] and len(i) == 2 and (self.findByAdress(i[1]) != -1 or i[1] in runtimeStorage):
                    self.tokens.append((i[0], i[1]))
                elif i[0] in ["ADD", "LDV", "AND", "OR", "XOR", "EQL"] and len(i) == 2:
                    raise InvalidAdress(i[1], line)
                elif i[0] in ["LDC", "STV", "JMN", "JMP"] and len(i) == 2:
                    self.tokens.append((i[0], i[1])) 
                    if i[0] == "STV":
                        runtimeStorage.append(i[1])
                elif i[0] in ["NOT", "RAR", "HALT"] and len(i) == 1:
                    self.tokens.append((i[0],))
                    if i[0] == "HALT":
                        break
                else:
                    raise InvalidSyntax(line)

    def run(self):
        while self.line < len(self.tokens):
            if len(self.tokens[self.line]) == 1:
                command = getattr(self, self.tokens[self.line][0])
                command()
            elif len(self.tokens[self.line]) == 2:
                command = getattr(self, self.tokens[self.line][0])
                command(self.tokens[self.line][1])
            self.line += 1


################################
#Commands
################################
    def ADD(self, adress):
        self.akku = self.TwoComplementAddition(self.storage[self.findByAdress(adress)][1].value)
    
    def LDC(self, const: str):
        self.akku = TwoComplement(self.bits, const).value

    def LDV(self, adress):
        if self.findByAdress(adress) != -1:
            self.akku = self.storage[self.findByAdress(adress)][1].value
        else:
            raise InvalidAdress(adress, line)

    def STV(self, adress):
        if self.findByAdress(adress) != -1:
            self.writeToStorage(adress, self.akku)
        else:
            self.addNewStorageCell(adress, self.akku)

    def EQL(self, adress):
        if (self.akku == self.storage[self.findByAdress(adress)][1].value):
            self.akku = "1" * self.bits
        else:
            self.akku = "0" * self.bits

    def AND(self, adress):
        desiredValue = ("0" * (self.bits - 1)) + "1" 
        if (self.akku == desiredValue and self.storage[self.findByAdress(adress)][1].value == self.akku):
            self.akku = desiredValue
        else:
            self.akku = "0" * self.bits

    def OR(self, adress):
        desiredValue = ("0" * (self.bits - 1)) + "1" 
        if (self.akku == desiredValue or self.storage[self.findByAdress(adress)][1].value == desiredValue):
            self.akku = desiredValue
        else:
            self.akku = "0" * self.bits

    def XOR(self, adress):
        desiredValue = ("0" * (self.bits - 1)) + "1"
        if (self.akku != self.storage[self.findByAdress(adress)][1].value) and (self.akku == desiredValue or self.storage[self.findByAdress(adress)][1].value == desiredValue):
            self.akku = desiredValue
        else:
            self.akku = "0" * self.bits
    
    def JMP(self, line):
        self.line = int(line) - 2

    def JMN(self, line):
        if self.akku[0] == "1":
            self.line = int(line) - 2

    def NOT(self):
        self.akku = self.invert(self.akku)
    
    def RAR(self):
        self.akku = self.akku[-1:] + self.akku[:-1]

    def HALT(self):
        for i in self.storage:
            print(str(i[0]) + ": " + str(i[1].value))
        print("Akku: " + self.akku)    
        exit()

################################
#Run Program
################################
@click.command() #TODO: fix Invalid value fo rpredefined Error (maybe move predefined storage into .mima file?)
@click.argument("path")
@click.option("--bits", type=int, required=True, help="The size of your Two's Complement values (amount of bits)")
def main(path, bits):
    predefined = readFile(path, False)
    initialSize = len(predefined)

    mima = MIMA(initialSize, bits)
   
    for i in range(initialSize):
           adressAti = predefined[i].split(":")[0].strip("(")
           valueAti = predefined[i].split(":")[1].strip(")")
           mima.defineStorageName(i, adressAti)
           mima.writeToStorage(adressAti, valueAti)

    try:
        mima.compile(path)
    except Exception as e:
        print(str(e))
        exit()

    mima.run()

if __name__ == "__main__":
    main()