import TwoComplement

def defineStorageSize(count: int):
        storage = []
        for i in range(count):
            storage.append((i, 0))
        return storage

class MIMA:
    def __init__(self, storageSize: int, bits: int):
        self.storage = defineStorageSize(storageSize)
        self.akku = "0"
        self.bits = bits

# Basic functionality

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

    def readFile(self, filePath):
        if not filepath.endswith(".mima"):
            raise InvalidFile
        else:
            with open(filePath) as f:
                self.code = f.readlines()
            
            for i in self.code:
                i = self.code.split(" ")

                if i[0] == "ADD" and findByAdress(i[1]) != -1:
                    self.ADD(i[1])
                elif i[0] == "LDC":
                    self.LOADCONSTANT(i[1])
                elif i[0] == "LDV":
                    self.LOADVALUE(i[1])
                elif i[0] == "STV":
                    self.STOREVALUE(i[1])
                elif i[0] == "NOT":
                    self.INVERT()

# Commands
    def ADD(self, adress):
        index = findByAdress(adress)
        addBinary(storage[index][1].value)
    
    def LOADCONSTANT(self, const: str):
        self.akku = TwoComplement(self.bits, const)

    def LOADVALUE(self, adress):
        if findByAdress(adress) != -1:
            self.akku = self.storage[findByAdress(adress)][1].value
        else:
            raise InvalidAdress #TODO

    def STOREVALUE(self, adress):
        if findByAdress(adress) != -1:
            self.storage[findByAdress(adress)][1].value = self.akku
        else:
            self.defineStorageName(adress, name)#TODO

    def INVERT(self):
        self.akku = self.invert(self.akku)
