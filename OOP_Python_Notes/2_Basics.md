# 2 Basics

Created: February 10, 2022 9:21 AM
Rate: completed

# 2 Basics

[Basics — Object-Oriented Programming in Python 1 documentation](https://python-textbok.readthedocs.io/en/1.0/Python_Basics.html)

## Keywords

```
False      class      finally    is         return
None       continue   for        lambda     try
True       def        from       nonlocal   while
and        del        global     not        with
as         elif       if         or         yield
assert     else       import     pass
break      except     in         raise
```

---

## Identifier names

- It may only contain letters (uppercase or lowercase), numbers or the underscore character (_) (no spaces!).
- it may not start with a number.
- it may not be a keyword.

This is a commonly used naming convention in Python:

- names of classes should be in CamelCase (words capitalised and squashed together).
- names of variables which are intended to be constants should be in CAPITAL_LETTERS_WITH_UNDERSCORES.
- names of all other variables should be in lowercase_with_underscores. In some other languages, like Java, the standard is to use camelCase (with the initial letter lowercase), but this style is less popular in Python.
- names of class attributes and methods which are intended to be “private” and not accessed from outside the class should start with an underscore.

*We refer to the order in which the computer executes instructions as the **flow of control**.*

**Python uses indentation only to delimit blocks, so we must indent our code**.

Python uses ends of lines to determine where instructions end (except in some special cases when the last symbol on the line lets Python know that the instruction will span multiple lines).

---

### Letter case

Python is case-sensitive

---

### More on Comments

Some languages also have support for comments that span multiple lines, but Python does not. If we want to type a very long comment in Python, we need to split it into multiple shorter lines and put a # at the start of each line.

It is possible to insert a multi-line string literal into our code by enclosing it in triple quotes. This is not normally used for comments, except in the special case of docstrings: strings which are inserted at the top of structures like functions and classes, and which document them according to a standard format. It is good practice to annotate our code in this way because automated tools can then parse it to generate documentation automatically. We will discuss docstrings further in a future chapter.

---

## Reading and writing

To query the user for information, we use the input function.

---

### Files

Although the print function prints to the console by default, we can also use it to write to a file.

```
with open('myfile.txt', 'w') as myfile:

    print("Hello!", file=myfile)

```

- with: makes sure that the file is closed when the with block is enclosed
- open: opens the file and assigns it a name

In the with statement (which we will look at in more detail in the chapter on errors and exceptions) the file myfile.txt is opened for writing and assigned to the variable myfile. Inside the with block, Hello! followed by a newline is written to the file. The w character passed to open indicates that the file should be opened for writing.

As an alternative to print, we can use a file’s write method as follows:

```
with open('myfile.txt', 'w') as myfile:

    myfile.write("Hello!")

```

- .write: I am using a method, that is a function attached to an object (myfile), or

We can read data from a file by opening it for reading and using the file’s read method:

```
with open('myfile.txt', 'r') as myfile:

    data = myfile.read()

```

---

## Built-in types

In Python (and other programming languages), the kinds of information the language is able to handle are known as types.

In many languages a distinction is made between built-in types (which are often called “primitive types” for this reason) and classes, but in Python they are indistinguishable. Everything in Python is an object (i.e. an instance of some class) – that even includes lists and functions.

A type consists of two parts: a domain of possible values and a set of possible operations that can be performed on these values.

Python is a dynamically (and not statically) typed language. That means that we don’t have to specify a type for a variable when we create it – we can use the same variable to store values of different types. However, Python is also strongly (and not weakly) typed – at any given time, a variable has a definite type.

The function type can be used to determine the type of an object.

Some other languages (e.g. C, Java) store each integer in a small fixed amount of memory. This limits the size of the integer that may be stored. Common limits are 2\*\*8, 2\*\*16, 2\*\*32 and 2\*\*64. Python has no fixed limit can stored surprisingly large integers such as 2\*\*1000000 as long as there is enough memory and processing power available on the machine where it is running.

### A list of built-in types

The principal built-in types are numerics, sequences, mappings, classes, instances and exceptions.

Numeric Types - int, bool, float, complex

Sequence types - list, tuple, range

Text sequence types - str

Set types - set, frozenset

Mapping types - dict

---

### Floating-point numbers

Floating-point numbers (float type) are numbers with a decimal point or an exponent (or both). Examples are 5.0, 10.24, 0.0, 12. and .3. We can use scientific notation to denote very large or very small floating-point numbers, e.g. 3.8 x 1015. The first part of the number, 3.8, is the mantissa and 15 is the exponent.

In Python, we can write the number 3.8 x 1015 as 3.8e15 or 3.8e+15. We can also write it as 38e14 or .038e17.

Python floating-point numbers conform to a standardised format named IEEE 754. The standard represents each floating-point number using a small fixed amount of memory, so unlike Python’s integers, Python’s floating-point numbers have a limited range. The largest floating-point number that can be represented in Python is 2**1023.

Python includes three other types for dealing with numbers:

- complex (like floating point but for complex numbers; try 1+5j)
- Fraction (for rational numbers; available in the fractions module)
- Decimal (for decimal floating-point arithmetic; available in the decimal module).

Using these is beyond the scope of this module, but it’s worth knowing that they exist in case you have a use for them later.

---

### Strings

In Python 3, the `str` type uses Unicode.

In Python 2, the `str` type used the ASCII encoding. If we wanted to use strings containing Unicode (for example, characters from other alphabets or special punctuation) we had to use the unicode type.

---

### String formatting syntax

The symbols in the string which start with percent signs (%) are placeholders, and the variables which are to be inserted into those positions are given after the string formatting operator, %, in the same order in which they appear in the string. If there is only one variable, it doesn’t require any kind of wrapper, but if we have more than one we need to put them in a tuple (between round brackets). The placeholder symbols have different letters depending on the type of the variable

```
name = "Jane"
age = 23
print("Hello! My name is %s." % name)
print("Hello! My name is %s and I am %d years old." % (name, age))
```

- (name, age) is a tuple, that is a collection of elements

---

### Escape sequences

An escape sequence (of characters) can be used to denote a special character which cannot be typed easily on a keyboard or one which has been reserved for other purposes.

If our string is enclosed in single quotes, we will have to escape apostrophes, and we need to do the same for double quotes in a string enclosed in double quotes. An escape sequence starts with a backslash (\):

```
print('"Hi! I\\'m Jane," she said.')
print("\\"Hi! I'm Jane,\\" she said.")
```

Some of the most commonly used escape sequences:

- \\ literal backslash
- \' single quote
- \" double quote
- \n newline
- \t tab

We can also use escape sequences to output unicode characters.

---

### Raw strings

By adding an r before the opening quote of the string, we indicate that the contents of the string are exactly what we have written, and that backslashes have no special meaning.

In Matplotlib, raw strings can be used inside annotations of plots to contain LaTeX strings.

---

### Triple quotes

In cases where we need to define a *long literal spanning multiple lines*, or containing many quotes, it may be simplest and most legible to enclose it in triple quotes (either single or double quotes, but of course they must match). **Inside the triple quotes, all whitespace is treated literally** – if we type a newline it will be reflected in our string. We also don’t have to escape any quotes.

In Python, strings are immutable – that means that we can’t modify a string once it has been created. However, we can assign a new string value to an existing variable name.

e.g. to convert a string from mixed lower and upper case characters to a only-lower casa string, use

```
lower(string)
```

and assign its value to a new string variable.