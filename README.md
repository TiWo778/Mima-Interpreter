# Mima-Interpreter
Simple Interpreter for the Minimal Machine
***
## How to write a Program
* The entire code needs to be written in a text-file, which must have the extension ".mima"
* Every command must be written in a new line, followed by its parameter (if necessary). The two have to be seperated by a whitespace.
* All code under the *code:* keyword will be executed
* Every program needs to end with **HALT**
* Text may be added after the "HALT" command
* All numbers used inside of the Program must be in Two's Complement format ([Wikipedia](https://en.wikipedia.org/wiki/Two%27s_complement))
* If a provided number is not in x-Bit format, it will be filled with leading 0's until it is (**LDC** *10* in 4-Bit format will automatically be converted to **LDC** *0010*)
### How to define storage cells that already have a value
* You can define storage cells anywhere in your file (with the exception of between the *code:* Keyword and the **HALT** command)
* You define storage cells in format: *(adress:value)* , where *adress* will be the name of the cell (any String not containing whitespaces) and *value* will be the stored value (In Two's Complement format)
* You dont have to define all the storage you will need, if you try to store a value at a non-existent cell using **STV** *adress*, a cell with name *adress* will be created
* You have to to write all storage cells directly after the *storage:* keyword and put the *:endStorage* keyword directly under your storage cells 

### <div align="center">(See example.mima for demonstration)</div>
---
## Overview of valid Commands
* **LDC** *x* | loads the Number x into the Akkumulator
* **LDV** *a* | loads the Value at the adress a into the Akkumulator
* **STV** *a* | stores the Value in the Akkumulator at the adress a
* **ADD** *a* | adds the Value stored at the adress a to the Value in the Akkumulator
* **EQL** *a* | writes the Two's Complement Value of -1 into the Akkumulator if the Value in the Akkumulator equals the Value at adress a, and 0 if not
* **AND** *a* | writes 1 into the Akkumulator if the Value in the Akkumulator and the Value at adress a both are 1, and 0 if not
* **OR**  *a* | writes 1 into the Akkumulator if the Value in the Akkumulator or the Value at adress a, or both are 1, and 0 if not
* **XOR** *a* | writes 1 into the Akkumulator if either the Value in the Akkumulator, or the Value at adress a, but not both, are 1, and 0 if not
* **JMN** *y* | continues the code execution at the line y, if the Value in the Akkumulator is negative
* **JMP** *y* | continues the code execution at the line y, regardless of the Value in the Akkumulator
* **NOT** | negates the Two's Complement Value in the Akkumulator (every 1 turns into a 0 and vice versa)
* **RAR** | rotates the Two's Complement Value in the Akkumulator one Bit to the right, filling with 0's (10011 --> 01001)
* **HALT** | stops the execution of the program. **Every program has to end with this command!**
---
## How to execute your code
* python 3.x has to be installed (see [Guide](https://realpython.com/installing-python/))
* click module needs to be installed:
    ```
    pip install click 
    ```

The command:

python Mima.py *(Path to .mima file)* --bits *(number of bits you will use for your Numbers)* 

will run the specified .mima file (assuming you run the command from the folder that Mima.py is saved in).

For example:
```
python Mima.py ./myProgram.mima --bits 16
```
will run *myProgram.mima*, which is stored in the same directory as *Mima.py*, interpreting all numbers as 16-Bit Two's Complement.
