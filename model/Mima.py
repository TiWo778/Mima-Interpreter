from TwoComplement import TwoComplement

def defineStorageSize(count: int):
        storage = []
        for i in range(count):
            storage.append((i, 0))
        return storage

class MIMA:
    def __init__(self, storageSize: int, bits: int):
        self.storage = defineStorageSize(storageSize)
        self.akku = 0
        self.bits = bits

# Basic functionality

    def findByAdress(self, adress):
        for i in storage:
            if i[0] == adress:  
                return storage.indexOf(i)

    def defineStorageName(self, adress, name: str):
        index = findByAdress(adress)
        self.storage[index][0] = name

    def writeToStorage(adress, value):
        value = TwoComplement(self.bits, value)
        index = findByAdress(adress)
        self.storage[index][1] = value

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
            
            #TODO CODE INTERPRETATION

# Commands
    def ADD(self, adress):
        index = findByAdress(adress)
        addBinary(storage[index][1].value)
    
    def ADDCONST(self, const: str):
        addBinary(const)

    #TODO REST OF COMMANDS
