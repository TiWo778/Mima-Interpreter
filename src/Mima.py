import click

__author__ = "Tim Wolk"
__version__ = "1.2"

'''
################################
# Exceptions
################################
'''


class InvalidSyntax(Exception):
    def __init__(self, line):
        self.message = f"Invalid Syntax in line *{line}* of your code"

    def __str__(self):
        return self.message


class InvalidAddress(Exception):
    def __init__(self, address, line):
        self.message = f"The address *{address}* referenced at line *{line}* of your code does not exist"

    def __str__(self):
        return self.message


class InvalidNumber(Exception):
    def __init__(self, number):
        self.message = f"The number *{number}* is not a valid"

    def __str__(self):
        return self.message


class InvalidFile(Exception):
    def __init__(self, path):
        self.message = f"The file *{path}* does not exist"

    def __str__(self):
        return self.message


class InvalidLabel(Exception):
    def __init__(self, label, line):
        self.message = f"The label *{label}*, referenced at line *{line}* of your code does not exist"

    def __str__(self):
        return self.message


'''
################################
# Two Complement System
################################
'''


class TwoComplement:

    def __init__(self, length, value):
        self.length = length
        self.value = self.convert(value)

    def convert(self, num):

        if len(num) > self.length:
            raise InvalidNumber(num)

        for i in num:
            if i != "1" and i != "0":
                raise InvalidNumber(num)

        if len(num) < self.length:
            num = "0" * (self.length - len(num)) + num

        return num


'''
################################
# Other util methods
################################
'''


# The Method defines the initial Storage size and creates placeholder cells
def define_storage_size(count: int, bits: int):
    storage = []
    for i in range(count):
        storage.append([str(i), TwoComplement(bits, "0")])
    return storage


# The Method reads a files' storage/code section, depending on the bool that is passed and returns the lines as array
def read_file(path: str, is_code: bool):
    if not path.endswith(".mima"):
        raise InvalidFile(path)

    result = []

    if not is_code:

        with open(path) as file:
            lines = file.readlines()

            for i in range(len(lines)):
                if (i > 0) and (lines[i - 1].strip("\n") == "storage:"):
                    for line in lines[i:len(lines)]:
                        if line.strip("\n") == ":endStorage":
                            break
                        result.append(line.strip("\n"))
                    break
    else:
        with open(path) as file:
            lines = file.readlines()

            for i in range(len(lines)):
                if (i > 0) and (lines[i - 1].strip("\n") == "code:"):
                    for line in lines[i:len(lines)]:
                        result.append(line.strip("\n"))
                        if line.__contains__("HALT"):
                            break
                    break

    return result


'''
################################
# MIMA Interpreter Class
################################
'''


class MIMA:
    def __init__(self, storage_size: int, bits: int, overflow: bool):
        self.jump_labels = {}
        self.code = []
        self.storage = define_storage_size(storage_size, bits)
        self.akku = "0"
        self.bits = bits
        self.tokens = []
        self.line = 0
        self.overflow = overflow
        self.valid_tokens = ["ADD", "LDV", "AND", "OR", "XOR", "EQL", "LDC", "STV", "JMN", "JMP", "NOT", "RAR", "HALT"]

    ################################
    # Basic functions
    ################################
    def find_by_address(self, address):
        for i in self.storage:
            if i[0] == address:
                return self.storage.index(i)
        return -1

    def define_storage_name(self, address, name: str):
        index = self.find_by_address(address)
        self.storage[index][0] = name

    def write_to_storage(self, address, value):
        value = TwoComplement(self.bits, value)
        index = self.find_by_address(address)
        self.storage[index][1] = value

    def add_new_storage_cell(self, name: str, value: str):
        self.storage.append([name, TwoComplement(self.bits, value)])

    def invert(self, value):
        inverted = ""
        for i in value:
            if i == "0":
                inverted += "1"
            elif i == "1":
                inverted += "0"
        return inverted

    def two_complement_addition(self, value: str):
        to_add = [char for char in self.akku]
        value_list = [char for char in value]
        new_value = ["0" for _ in range(self.bits)]
        i = self.bits - 1
        temp = "0"

        while i >= 0:
            if to_add[i] == "0" and value_list[i] == "0":
                new_value[i] = temp
                temp = "0"

            elif to_add[i] != value_list[i]:
                if temp == "0":
                    new_value[i] = "1"
                else:
                    new_value[i] = "0"

            elif to_add[i] == "1" and value_list[i] == "1":
                if temp == "0":
                    new_value[i] = "0"
                    temp = "1"
                else:
                    new_value[i] = "1"

            i -= 1

        if self.overflow:
            i = self.bits - 1

            while temp == "1":
                if new_value[i] == "1":
                    new_value[i] = "0"
                else:
                    new_value[i] = "1"
                    temp = "0"

                i -= 1

        return "".join(new_value)

    '''
    ################################
    # Code Interpretation
    ################################
    '''

    def compile(self, path):
        if not path.endswith(".mima"):
            raise InvalidFile(path)
        else:
            self.code = read_file(path, True)

            jump_to = {}
            line = 0
            runtime_storage = []

            for code_segment in self.code:
                if code_segment == "":
                    continue
                line += 1
                i = code_segment.strip("\n").split(" ")

                if i[0] in self.valid_tokens[0:10] and len(i) >= 2:
                    if i[0] in self.valid_tokens[0:6] and (
                            self.find_by_address(i[1]) != -1 or i[1] in runtime_storage):
                        self.tokens.append((i[0], i[1]))

                    elif i[0] in self.valid_tokens[0:6]:
                        raise InvalidAddress(i[1], line)

                    elif i[0] in self.valid_tokens[6:10]:
                        self.tokens.append((i[0], i[1]))
                        if i[0] == "STV":
                            runtime_storage.append(i[1])
                        elif i[0] in ["JMP", "JMN"]:
                            jump_to[i[1]] = line

                    if len(i) > 2 and i[2] != "":
                        self.jump_labels[i[2]] = line - 1

                elif i[0] in self.valid_tokens[10:] and len(i) >= 1:
                    self.tokens.append((i[0],))
                    if len(i) > 1 and i[1] != "":
                        self.jump_labels[i[1]] = line - 1
                    if i[0] == "HALT":
                        break

                else:
                    raise InvalidSyntax(line)

        for label in jump_to:
            if label not in self.jump_labels:
                raise InvalidLabel(label, jump_to[label])

    def run(self, debug: bool):
        while self.line < len(self.tokens):
            if len(self.tokens[self.line]) == 1:
                command = getattr(self, self.tokens[self.line][0])
                command()
                self.line += 1
            elif len(self.tokens[self.line]) == 2:
                if self.tokens[self.line][0] in ["JMP", "JMN"]:
                    self.line = self.jump_labels[self.tokens[self.line][1]]
                else:
                    command = getattr(self, self.tokens[self.line][0])
                    command(self.tokens[self.line][1])
                    self.line += 1

            if debug:
                click.echo("Line: " + str(self.line))

                if len(self.tokens[self.line - 1]) > 1:
                    command_str = self.tokens[self.line - 1][0] + " " + self.tokens[self.line - 1][1]
                else:
                    command_str = self.tokens[self.line - 1][0]

                click.echo("Command: " + command_str)
                click.echo("Akku: " + self.akku)
                click.echo("Storage: ")
                for i in self.storage:
                    click.echo(i[0] + ": " + i[1].value)
                input("")

    '''
    ################################
    # Commands
    ################################
    '''

    def ADD(self, address):
        self.akku = self.two_complement_addition(self.storage[self.find_by_address(address)][1].value)

    def LDC(self, const: str):
        self.akku = TwoComplement(self.bits, const).value

    def LDV(self, address):
        self.akku = self.storage[self.find_by_address(address)][1].value

    def STV(self, address):
        if self.find_by_address(address) != -1:
            self.write_to_storage(address, self.akku)
        else:
            self.add_new_storage_cell(address, self.akku)

    def EQL(self, address):
        if self.akku == self.storage[self.find_by_address(address)][1].value:
            self.akku = "1" * self.bits
        else:
            self.akku = "0" * self.bits

    def AND(self, address):
        desired_value = ("0" * (self.bits - 1)) + "1"
        if self.akku == desired_value and self.storage[self.find_by_address(address)][1].value == self.akku:
            self.akku = desired_value
        else:
            self.akku = "0" * self.bits

    def OR(self, address):
        desired_value = ("0" * (self.bits - 1)) + "1"
        if self.akku == desired_value or self.storage[self.find_by_address(address)][1].value == desired_value:
            self.akku = desired_value
        else:
            self.akku = "0" * self.bits

    def XOR(self, address):
        desired_value = ("0" * (self.bits - 1)) + "1"
        if (self.akku != self.storage[self.find_by_address(address)][1].value) \
                and (self.akku == desired_value
                     or self.storage[self.find_by_address(address)][1].value == desired_value):
            self.akku = desired_value
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
        self.akku = "0" + self.akku[:-1]

    def HALT(self):
        output = ""
        for i in self.storage:
            output += (str(i[0]) + ": " + str(i[1].value) + "\n")
        output += ("Akku: " + self.akku) + "\n"
        click.echo(output)
        exit()


################################
# Run Program
################################
@click.command()
@click.argument("path")
@click.option("--d", is_flag=True, default=False, help="Runs your code in debug mode, meaning that the excecution will "
                                                       "be paused after each line and the current state of the machine"
                                                       " will be printed. To continue the execution, press enter.")
def main(path, d):
    with open(".config", "r") as config:
        lines = config.readlines()
        bits = int(lines[0].strip("\n").split("=")[1])
        code_path = lines[1].strip("\n").split("=")[1]
        overflow = eval(lines[2].strip("\n").split("=")[1])

    if code_path == "None":
        file_path = "./mimaCode/" + path
    else:
        file_path = code_path + "/" + path

    predefined = read_file(file_path, False)
    initial_size = len(predefined)

    mima = MIMA(initial_size, bits, overflow)

    for i in range(initial_size):
        address_ati = predefined[i].split(":")[0].strip("(")
        value_ati = predefined[i].split(":")[1].strip(")")
        mima.define_storage_name(i, address_ati)
        mima.write_to_storage(address_ati, value_ati)

    try:
        mima.compile(file_path)
    except Exception as e:
        click.echo("Error: " + str(e))
        exit()

    mima.run(d)


if __name__ == "__main__":
    main()
