import TwoComplement

################################
#Exceptions
################################

class InvalidSyntax(Exception):
    def __init__(self, line):
        self.message = f"Invalid Syntax in line {line}"
    
class InvalidAddress(Exception):
    def __init__(self, address):
        self.message = f"The address {address} does not exist"


def defineStorageSize(count: int):
        storage = []
        for i in range(count):
            storage.append((i, 0))
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
        for i in storage:
            if i[0] == adress:  
                return storage.indexOf(i)
        return -1

    def defineStorageName(self, adress, name: str):
        index = findByAdress(adress)
        self.storage[index][0] = name

    def writeToStorage(adress, value):
        value = TwoComplement(self.bits, value)
        index = findByAdress(adress)
        self.storage[index][1] = value

    def invert(self, value):
        inverted = ""
        for i in value:
            if i == "0":
                inverted += "1"
            elif i == "1":
                inverted += "0"
        return inverted

    def addBinary(self, value: str):
        toAdd = self.akku
        newAkku = value
        temp == "0"
        i = len(value) - 1
        while i >= 0:
            if value[i] == "0" and toAdd[i] == "0" and temp == "0":
                newAkku[i] = "0"

            elif value[i] == "0" and toAdd[i] == "0" and temp == "1":
                newAkku[i] = "1"

            elif ((value[i] == "0" and toAdd[i] == "1") or (value[i] == "1" and toAdd[i] == "0")) and temp == "0":
                newAkku[i] == "1"

            elif ((value[i] == "0" and toAdd[i] == "1") or (value[i] == "1" and toAdd[i] == "0")) and temp == "1":
                newAkku[i] == "0"
                temp = "1"

            elif ((value[i] == "1" and toAdd[i] == "1") or (value[i] == "1" and toAdd[i] == "1")) and temp == "0":
                newAkku[i] == "0"
                temp = "1"
            
            elif ((value[i] == "1" and toAdd[i] == "1") or (value[i] == "1" and toAdd[i] == "1")) and temp == "1":
                newAkku[i] == "1"
                temp = "1"
            
            i -= 1
        
        if temp == "1":
            i = len(newAkku) - 1
            while temp != "0":
                if newAkku[i] == "0" and temp == "1":
                    newAkku[i] = "1"
                    temp = "0"

                elif newAkku[i] == "1" and temp == "1":
                    newAkku[i] = "0"
            
            i -= 1

        self.akku = newAkku

    def compile(self, filePath):
        if not filepath.endswith(".mima"):
            raise InvalidFile
        else:
            with open(filePath) as f:
                self.code = f.readlines()
            
            line = 0

            for i in self.code:
                line += 1
                i = self.code.split(" ")

            if i[0] in ["ADD", "LDV", "AND", "OR", "XOR", "EQL"] and len(i) == 2 and findByAdress(i[1]) != -1:
                self.tokens.append((i[0], i[1]))
            elif i[0] in ["ADD", "LDV", "AND", "OR", "XOR", "EQL"] and findByAdress(i[1]) == -1:
                raise InvalidAdress(i[1])
            elif i[0] == ["LDC", "STV", "JMN", "JMP"] and len(i) == 2:
               self.tokens.append((i[0], i[1])) 
            elif i[0] in ["NOT", "RAR", "HALT"] and len(i) == 1:
               self.tokens.append(i[0])
            else:
                raise InvalidSyntax(line)

################################
#Commands
################################
    def ADD(self, adress):
        index = findByAdress(adress)
        addBinary(storage[index][1].value)
    
    def LOADCONSTANT(self, const: str):
        self.akku = TwoComplement(self.bits, const)

    def LOADVALUE(self, adress):
        if findByAdress(adress) != -1:
            self.akku = self.storage[findByAdress(adress)][1].value
        else:
            raise InvalidAdress(adress)

    def STOREVALUE(self, adress):
        if findByAdress(adress) != -1:
            self.storage[findByAdress(adress)][1].value = self.akku
        else:
            self.defineStorageName(adress, name)#TODO

    def EQUAL(self, adress):
        if (self.akku == self.storage[findByAdress(adress)][1].value):
            self.akku = "1"
        else:
            self.akku = "0"

    def AND(self, adress):
        if (self.akku == "1" and self.storage[findByAdress(adress)][1].value == "1"):
            self.akku = "1"
        else:
            self.akku = "0"

    def OR(self, adress):
        if (self.akku == "1" or self.storage[findByAdress(adress)][1].value == "1"):
            self.akku = "1"
        else:
            self.akku = "0"

    def XOR(self, adress):
        if (self.akku != self.storage[findByAdress(adress)][1].value) and (self.akku == "1" or self.storage[findByAdress(adress)][1].value == "1"):
            self.akku = "1"
        else:
            self.akku = "0"
    
    def JUMP(self, line, conditional=False):
        if conditional:
            if self.akku == "1":
                self.line = line - 1
        else:
            self.line = line - 1

    def INVERT(self):
        self.akku = self.invert(self.akku)
    
    def ROTATRIGHT(self):
        self.akku = self.akku[-1:] + self.akku[:-1]

    def HALT(self):
        #TODO Ausgabe aller Speicheradressen und akku
        exit()