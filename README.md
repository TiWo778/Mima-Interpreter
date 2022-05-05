# Mima-Interpreter
Simple Interpreter for the Minimal Machine
***
## How to write a Program
* The entire code needs to be written in a text-file, which must have the extension ".mima"
* Every command must be written in a new line, followed by its parameter (if necessary). The two have to be seperated by a whitespace.
* There must not be any other Text in the same line as a command or preceding the start of the Program
* Text may be added after the "HALT" command
* All numbers used inside of the Program must be in Two's Complement Format ([Wikipedia](https://en.wikipedia.org/wiki/Two%27s_complement))
---
## Overview of valid Commands
* **LDC** *x* | loads the Number x into the Akkumulator
* **LDV** *a* | loads the Value at the adress a into the Akkumulator
* **STV** *a* | stores the Value in the Akkumulator at the adress a
* **ADD** *a* | adds the Valuestored at the adress a to the Value in the Akkumulator
* **EQL** *a* | writes the Two's Complement Value of -1 into the Akkumulator if the Value in the Akkumulator equals the Value at adress a, and 0 if not
* **AND** *a* | writes the Two's Complement Value of -1 into the Akkumulator if the Value in the Akkumulator and the Value at adress a both are smaller than 0, and 0 if not
* **OR**  *a* | writes the Two's Complement Value of -1 into the Akkumulator if the Value in the Akkumulator or the Value at adress a, or both are smaller than 0, and 0 if not
* **XOR** *a* | writes the Two's Complement Value of -1 into the Akkumulator if either the Value in the Akkumulator, or the Value at adress a are smaller than 0, and 0 if not
* **JMN** *y* | continues the code execution at the line y, if the Value in the Akkumulator is negative
* **JMP** *y* | continues the code execution at the line y, regardless of the Value in the Akkumulator
* **NOT** | negates the Two's Complement Value in the Akkumulator (every 1 turns into a 0 and vice versa)
* **RAR** | rotates the Two's Complement Value in the Akkumulator one Bit to the right (10010 --> 01001)
* **HALT** | stops the execution of the program. **Every program has to end with this command!**
---
## How to execute your code
1. Run the Mima.py file with "python *PathToFile*/Mima.py
2.  
