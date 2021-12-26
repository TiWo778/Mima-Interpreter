
class TwoComplement:

    def __init__(self, length, value):
        self.length = length
        try:
            self.value = self.convert(value)
        except:
            print("please enter a valid number")
            self.value = 0

    def convert(self, num):
        if type(num) == int:
            num = f"{bin(num)[2::]}"
            if len(num) > self.length:
                raise Exception
            else:
                return num

        elif type(num) == str:
            for i in num:
                if i != "1" or i != "0":
                    raise Exception
            return num
        
        else: 
            raise Exception