# 3 Variables and scope

Created: February 10, 2022 9:21 AM
Rate: completed

# 3 Variables and Scope

[Variables and Scope — Object-Oriented Programming in Python 1 documentation](https://python-textbok.readthedocs.io/en/1.0/Variables_and_Scope.html)

## Variable scope and lifetime

We call the part of a program where a variable is accessible its scope, and the duration for which the variable exists its lifetime.

def scope(var): the area of the code where the variable exists

def lifetime(var): the interval of time during which the variable lives

A variable which is defined in the main body of a file is called a global variable. It will be visible throughout the file, and also inside any file which imports that file. Global variables can have unintended consequences because of their wide-ranging effects – that is why we should almost never use them. Only objects which are intended to be used globally, like functions and classes, should be put in the global namespace.

A variable which is defined inside a function is local to that function. It is accessible from the point at which it is defined until the end of the function, and exists for as long as the function is executing.

The inside of a class body is also a new local variable scope. Variables which are defined in the class body (but outside any class method) are called class attributes. They can be referenced by their bare names within the same scope, but they can also be accessed from outside this scope if we use the attribute access operator (.) on a class or an instance (an object which uses that class as its type). An attribute can also be set explicitly on an instance or class from inside a method. Attributes set on instances are called instance attributes. Class attributes are shared between all instances of a class, but each instance has its own separate instance attributes.

## The assignment operator

Assigning an initial value to variable is called initialising the variable. In some languages defining a variable can be done in a separate step before the first value assignment.

In Python a variable is defined and assigned a value in a single step

An assignment statement may have multiple targets separated by equals signs. The expression on the right hand side of the last equals sign will be assigned to all the targets. All the targets must be valid:

```
# both a and b will be set to zero:
a = b = 0
# this is illegal, because we can't set 0 to b:
a = 0 = b
```

By default, the assignment statement creates variables in the local scope. So the assignment inside the function does not modify the global variable a – it creates a new local variable called a, and assigns the value 3 to that variable.

What if we really want to modify a global variable from inside a function? We can use the global keyword:

```
a = 0

def my_function():
    global a
    a = 3
    print(a)

my_function()
print(a)
```

We may not refer to both a global variable and a local variable by the same name inside the same function. This program will give us an error:

```
a = 0

def my_function():

    print(a)

    a = 3

    print(a)

my_function()

```

Because we haven’t declared a to be global, the assignment in the second line of the function will create a local variable a. This means that we can’t refer to the global variable a elsewhere in the function, even before this line! The first print statement now refers to the local variable a – but this variable doesn’t have a value in the first line, because we haven’t assigned it yet!

There is also a nonlocal keyword in Python – when we nest a function inside another function, it allows us to modify a variable in the outer function from inside the inner function (or, if the function is nested multiple times, a variable in one of the outer functions). If we use the global keyword, the assignment statement will create the variable in the global scope if it does not exist already. If we use the nonlocal keyword, however, the variable must be defined, because it is impossible for Python to determine in which scope it should be created.

## Modifying values

### Constants

In some languages, it is possible to define special variables which can be assigned a value only once – once their values have been set, they cannot be changed. We call these kinds of variables constants. Python does not allow us to set such a restriction on variables, but there is a widely used convention for marking certain variables to indicate that their values are not meant to change: we write their names in all caps, with underscores separating words:

Literal numbers scattered throughout a program are known as “magic numbers” – using them is considered poor coding style.

Sometimes we want to use a variable to distinguish between several discrete options. It is useful to refer to the option values using constants instead of using them directly if the values themselves have no intrinsic meaning:

```
# We define some options

LOWER, UPPER, CAPITAL = 1, 2, 3

name = "jane"

# We use our constants when assigning these values...

print_style = UPPER

# ...and when checking them:

if print_style == LOWER:

    print(name.lower())

elif print_style == UPPER:

    print(name.upper())

elif print_style == CAPITAL:

    print(name.capitalize())

else:

    # Nothing prevents us from accidentally setting print_style to 4, 90 or

    # "spoon", so we put in this fallback just in case:

    print("Unknown style option!")

```

Some Python libraries define common constants for our convenience, for example:

```
# we need to import these libraries before we use them

import string

import math

import re

# All the lowercase ASCII letters: 'abcdefghijklmnopqrstuvwxyz'

print(string.ascii_lowercase)

# The mathematical constants pi and e, both floating-point numbers

print(math.pi) # ratio of circumference of a circle to its diameter

print(math.e) # natural base of logarithms

# This integer is an option which we can pass to functions in the re

# (regular expression) library.

print(re.IGNORECASE)

```

## More about input

What if we want the user to input numbers or other types of variables? We still use the input function, but we must convert the string values returned by input to the types that we want. Here is a simple example:

```
height = int(input("Enter height of rectangle: "))

width = int(input("Enter width of rectangle: "))

print("The area of the rectangle is %d" % (width * height))

```

When we write a program which relies on user input, which can be incorrect, we need to add some safeguards so that we can recover if the user makes a mistake. For example, we can detect if the user entered bad input and exit with a nicer error message:

```
try:

    height = int(input("Enter height of rectangle: "))

    width = int(input("Enter width of rectangle: "))

except ValueError as e: # if a value error occurs, we will skip to this point

    print("Error reading height and width: %s" % e)

```

## Type conversion

### Implicit conversion

Recall from the section about floating-point operators that we can arbitrarily combine integers and floating-point numbers in an arithmetic expression – and that the result of any such expression will always be a floating-point number. This is because Python will convert the integers to floating-point numbers before evaluating the expression. This is an implicit conversion – we don’t have to convert anything ourselves. There is usually no loss of precision when an integer is converted to a floating-point number.

### Explicit conversion

Converting numbers from float to int will result in a loss of precision.

The int function converts a float to an int by discarding the fractional part – it will always round down! If we want more control over the way in which the number is rounded, we will need to use a different function:

```
# the floor and ceil functions are in the math module

import math

# ceil returns the closest integer greater than or equal to the number

# (so it always rounds up)

i = math.ceil(5.834)

# floor returns the closest integer less than or equal to the number

# (so it always rounds down)

i = math.floor(5.834)

# round returns the closest integer to the number

# (so it rounds up or down)

# Note that this is a built-in function -- we don't need to import math to use it.

i = round(5.834)

```

Explicit conversion is sometimes also called casting – we may read about a float being cast to int or vice-versa.

## Converting to and from strings

To convert numbers to strings, we can use string formatting – this is usually the cleanest and most readable way to insert multiple values into a message. If we want to convert a single number to a string, we can also use the str function explicitly:

```
# These lines will do the same thing

print("3%d" % 4)

print("3" + str(4))

```

Values of type `bool` can contain the value True or False.

This usually behaves in the way that you would expect: non-zero numbers are True values and zero is False. However, we need to be careful when using strings – the empty string is treated as False, but any other string is True – even "0" and "False"!