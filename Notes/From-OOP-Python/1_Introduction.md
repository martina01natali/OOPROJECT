# 1 Introduction

Created: February 10, 2022 9:21 AM
Rate: completed

## References

[Object-Oriented Programming in Python - Object-Oriented Programming in Python 1 documentation](https://python-textbok.readthedocs.io/en/1.0/index.html)

---

# 1 Introduction

[Introduction — Object-Oriented Programming in Python 1 documentation](https://python-textbok.readthedocs.io/en/1.0/Introduction.html)

Here are some examples of simple computer instructions:

- arithmetic
- comparison: comparing two numbers to see which is greater, or whether they are equal. These are often called logical operations.
- branching: jumping to another instruction in the program, and continuing from there.

## Components of a computer

- input
- processing: the components of the computer which process information. The main processing component of a computer is the central processing unit, or CPU, but in a modern computer there are likely to be other processing units too. For example, many graphics cards come with graphics processing units, or GPUs
- memory: components where information is stored
- output: anything that the computer uses to display information to the user

Two important characteristics of a CPU are:

- clock speed: the CPU contains a clock which produces a regular signal. All the low-level operations (switches) that the CPU performs in order to process instructions are synchronised to this signal. The faster the clock, the faster the CPU can (in theory) operate
- instruction set: this is the set of instructions (more accurately, the machine language instructions) that the CPU understands

A CPU has several important subcomponents:

- the arithmetic/logic unit (ALU) performs arithmetic and comparison operations.
- the control unit determines which instruction to execute next.
- registers form a high-speed storage area for temporary results.

### Memory

A computer stores information in its memory for later reference. There are two types of memory: primary and secondary.

- Primary memory is connected directly to the CPU (or other processing units) and is usually referred to as RAM (random-access memory). Most primary memory loses its contents when the computer is switched off (i.e. it is volatile).
- Secondary memory is cheaper than primary memory, and can thus be made available in much larger sizes. Although it is much slower, it is non-volatile – that is, its contents are preserved even after the computer is switched off. Examples of this type of memory include hard disks and flash disks.

A computer’s operating system provides high-level interfaces to secondary memory. These interfaces allow us to refer to clusters of related information called files which are arranged in a hierarchy of directories. Both the interfaces and the hierarchies are often referred to as filesystems.

## Types of computers

- single-user personal computers: these computers are designed for home use by a single person at a time
- batch computer systems: some computers were designed to process large batches of instructions non-interactively – that is, large amounts of work was scheduled to be done without the possibility of further input from the user while it was being done.
- time-share computer systems: these computer systems were an improvement over batch processing systems which allowed multiple users to access the same central computer remotely at the same time.
- computer networks: these are multiple computers connected to each other with digital or analog cables or wirelessly, which are able to communicate with each other. Today almost all computers can be connected to a network.

In most networks there are specialised computers called servers which provide services to other computers on the network (which are called clients).

The Internet is a very large international computer network. Many computers on the Internet are servers. When you use a web browser, you send requests to web servers which respond by sending you webpages.

## Programming a computer

### Algorithms

An algorithm is a series of steps which must be followed in order for some task to be completed or for some problem to be solved.

There are 2 main approaches to programming:

- **structured approach**
- **object-oriented approach**

The object-oriented approach to programming is an attempt to simulate the real world by including several actors in the algorithm

In the OO programming approach, multiple objects act together to accomplish a goal

### Programming languages

To make use of an algorithm in a computer, we must first convert it to a program. We do this by using a programming language which the computer is able to convert unambiguously into computer instructions, or machine language

### assembly language

Each assembly instruction corresponds to one machine language instruction, but it is more easily understood by humans

Programs written in assembly language cannot be understood by the computer directly, so a translation step is needed. This is done using an assembler, whose job it is to translate from assembly language to machine language.

High-level languages were developed to make programming even easier.

### Compilers, interpreters and the Python programming language

*Programs written in high-level languages must also be translated into machine language before a computer can execute them*. We can have different types of languages depending on how the instructions are actually stored and passed to the machine.

- ***compiled languages*: programming languages that translate the whole program at once in machine language and store the result in another file which is then executed.**
- ***interpreted languages*: languages that translate and execute programs line-by-line.**

A compiled language comes with a compiler, which is a program which compiles source files to executable binary files.

An interpreted language comes with an interpreter, which interprets source files and executes them. Interpretation can be less efficient than compilation, so interpreted languages have a reputation for being slow.

C++ is a compiled language, like C is, while Bash and Python are interpreted languages.

### Understanding the problem

### Programming languages

***Programs can be categorised into four major groups – procedural, functional, logic and object-oriented languages***

### Procedural languages

A program written in a procedural language consists of a list of statements, which the computer follows in order. Different parts of the program communicate with one another using variables. A variable is actually a named location in primary memory. The value stored in a variable can usually be changed throughout the program’s execution. In some other programming language paradigms (such as logic languages), variables act more like variables used in mathematics and their values may not be changed.

Examples of procedural languages are C, FORTRAN, Pascal, Java (that is also OO).

### Functional and logic languages

A functional language is based on mathematical functions. It usually consists of functions and function calls. In the language’s pure form, variables do not exist: instead, parts of program communicate through the use of function parameters.

> # This Lisp program calculates the
# sum of 20 and 17. It then displays the result.
(format t "The sum of 20 and 17 is \~D~%" (+ 20 17))
>

A logic language is based on formal rules of logic and inference. An example of such a language is Prolog. Prolog’s variables cannot be changed once they are set, which is typical of a logic language.

Prolog programs can consist of a set of known facts, plus rules for inferring new facts from existing ones.

### Object-oriented languages

In this approach, programmers model each **real-world entity as an object, with each object having its own set of values and behaviours (methods and attributes)**. This makes an object an active entity, whereas a variable in a procedural language is passive.

C++ is a hybrid OO language in that it has the procedural aspects of C. A C++ program can be completely procedural, completely OO or a hybrid. Most OO languages make use of variables in a similar fashion to procedural languages.

Java was introduced in 1995 by Sun Microsystems, who were purchased by Oracle Corporation during 2009-2010. It is an OO language but not as pure as Smalltalk. For example, in Java primitive values (numbers and characters) are not objects – they are values.

**Python is a general-purpose interpreted and object-oriented language**, which was originally created in the late 1980s, but only became widely used in the 2000s after the release of version 2.0. It is known for its clear, simple syntax and its dynamic typing – the same variables in Python can be reused to store values of different types; something which would not be allowed in a statically-typed language like C or Java. Everything in Python is an object, but Python can be used to write code in multiple styles – procedural, object-oriented or even functional.
