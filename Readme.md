# Java Compiler
This work is combined effort of me and  [Anuj Nagpal](https://github.com/anujnag)

This repository contains code for the compiler of **_Java_** language. Some details are:-

**Source language** :- Java

**Implementation language** :- Python

**Target language** :- x86 assembly language

## Description

This project was done in 4 steps. Each step getting us from Java code to x86 code. The description of those 4 steps are:-

1. Java scanner and parser written in python which outputs the syntax tree(parse tree) in a graphical form.
In this step, we took the raw Java code and converted it to its alternative representation i.e. In syntax Tree format
To draw the trees we used pydot. This step also checks for syntax errors

  Note:- graphical representation (made using pydot) is just to our soul satisfaction and is not needed in next steps. This step returned us a python class representation of parse tree that we use in next step.

2. In this step, we used our class represented tree and converted it to AST and also built symbol table using our parse tree. This step also checks for some compilation errors

3. In this step, we used AST and symbol table to generate an efficient TAC. We tried to optimise the number of TAC instructions wherever possible.

4. In this step, we used TAC and symbol table to generate the assembly code. Optimisations and other details of this step can be found below

### Running

Run the following command. It has 3 arguments (in this order)

1. -o, if you want to remove jump over jumps in the code
2. -f the java file name you want to compile 
3. -h for help 
```
python bin/final.py -f test/ackermann.java 
python bin/final.py -o 1 -f test/ackermann.java
```

This will output assembly code on your terminal window and also store it in output.s. Also, this will produce an executable file output.o
### Advance Features

This compiler has most of the basic features like loops, functions, nested loops, array, multidimensional arrays, etc. Apart from this it has some advanced features like:-

1. Short-circuiting
2. File IO
3. Recursion
4. etc....

More can be found in test folder where each program tests one/more of the feature of our compiler.

The main feature though was __register allocation optimization__. We tried to optimise the number of CPU registers used while execution of our program. For most of our test cases, we were able to achieve same/better register allocation performance when benchmarked with GCC compiler for a similar program in C.

## Performance and Appreciations

Our compiler was able to pass 19/20 tests specified by course instructor which included some of the advanced tests like matrix mul, mutual recursion, graph as list etc. The full list of these 19 tests can be found in the test folder.

We didn't had floating point unit due to which one test was unable to pass.

This work was highly appreciated by the course instructor and was awarded Full points.

## License

This project is licensed under the MIT License

## Acknowledgments

* Amey Karkare (Course Instructor CS335)
