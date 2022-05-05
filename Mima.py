################################
#Exceptions
################################
class InvalidSyntax(Exception):
    def __init__(self, line):
        self.message = f"Invalid Syntax in line {line}"
    
class InvalidAdress(Exception):
    def __init__(self, address):
        self.message = f"The address *{address}* does not exist"
    
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
        
#The Method defines the initial Storage size and creates placeholder cells
def defineStorageSize(count: int):
        storage = []
        for i in range(count):
            storage.append([i, 0])
        return storage

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
    def compile(self, filePath):
        if not filepath.endswith(".mima"):
            raise InvalidFile
        else:
            with open(filePath) as f:
                self.code = f.readlines()
            
            line = 0

            for codeSegment in self.code:
                line += 1
                i = codeSegment.strip("\n").split(" ")

                if i[0] in ["ADD", "STV", "LDV", "AND", "OR", "XOR", "EQL"] and len(i) == 2 and self.findByAdress(i[1]) != -1:
                    self.tokens.append((i[0], i[1]))
                elif i[0] in ["ADD", "STV", "LDV", "AND", "OR", "XOR", "EQL"] and self.findByAdress(i[1]) == -1:
                    raise InvalidAdress(i[1])
                elif i[0] in ["LDC", "JMN", "JMP"] and len(i) == 2:
                    self.tokens.append((i[0], i[1])) 
                elif i[0] in ["NOT", "RAR", "HALT"] and len(i) == 1:
                    self.tokens.append((i[0],))
                else:
                    raise InvalidSyntax(line)

    def run(self):
        for i in self.tokens:
            if len(i) == 1:
                command = getattr(mima, i[0])
                command()
            elif len(i) == 2:
                command = getattr(mima, i[0])
                command(i[1])


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
            raise InvalidAdress(adress)

    def STV(self, adress):
        if self.findByAdress(adress) != -1:
            self.writeToStorage(adress, self.akku)
        else:
            self.defineStorageName(adress, name)#TODO

    def EQL(self, adress):
        if (self.akku == self.storage[self.findByAdress(adress)][1].value):
            self.akku = "1"
        else:
            self.akku = "0"

    def AND(self, adress):
        if (self.akku == "1" and self.storage[self.findByAdress(adress)][1].value == "1"):
            self.akku = "1"
        else:
            self.akku = "0"

    def OR(self, adress):
        if (self.akku == "1" or self.storage[self.findByAdress(adress)][1].value == "1"):
            self.akku = "1"
        else:
            self.akku = "0"

    def XOR(self, adress):
        if (self.akku != self.storage[self.findByAdress(adress)][1].value) and (self.akku == "1" or self.storage[self.findByAdress(adress)][1].value == "1"):
            self.akku = "1"
        else:
            self.akku = "0"
    
    def JMP(self, line):
        self.line = line - 1

    def JMN(self, line):
        if self.akku == "1":
            self.line = line - 1

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
if __name__ == "__main__":
    filepath = input("Please specify a .mima file to run:\n")
    bits = int(input("Please specify the number of bits per storage cell:\n"))
    storageSize = int(input("Please specify the initial size of the storage (the number of already present storage cells):\n"))
    predefindedStorage = input("Please specify the predefinded storage seperated by semicolons in format: (*name of cell*:*value of cell*)):\n")

    while storageSize != len(predefindedStorage.split(";")):
        storageSize = input("Please specify the initial size of the storage (the number of already present storage cells):\n")
        predefindedStorage = input("Please specify the predefinded storage seperated by semicolons in format: (*name of cell*:*value of cell*)):\n")
    
    mima = MIMA(storageSize, bits)

    predefinedList = predefindedStorage.split(";")

    for i in range(storageSize):
        adressAti = predefinedList[i].split(":")[0].strip("(")
        valueAti = predefinedList[i].split(":")[1].strip(")")
        mima.defineStorageName(i, adressAti)
        mima.writeToStorage(adressAti, valueAti)

    try:
        mima.compile(filepath)
    except Exception as e:
        print(e.message)

    mima.run()