# 11 Object-oriented programming, aggregation and inheritance

Created: March 2, 2022 10:55 AM
Rate: in progress

[Object-oriented programming - Object-Oriented Programming in Python 1 documentation](https://python-textbok.readthedocs.io/en/1.0/Object_Oriented_Programming.html)

[Understand Inheritance in Python](https://towardsdatascience.com/understand-inheritance-in-python-74f8e3025f3c)

[Master Class Inheritance in Python](https://towardsdatascience.com/master-class-inheritance-in-python-c46bfda63374)

[OOP 3 mar](https://www.notion.so/OOP-3-mar-6beaccfdb757437f9d1f5693c6a080ec)

# 11 Object-oriented programming paradigm

# Introduction

Two paradigms can be applied to object-oriented languages such as C++, Pyhton and Java: **procedural** programming and **object-oriented** programming.

Procedural programming means that you’re building functions and using them by themselves, applying them to some objects, constantly having to check if those functions can actually be applied to your objects. This approach is fast and good for most simple programs.

Object-oriented programming is based on the aggregation of objects and functions into local subgroups that bind them: in this way, the functions that can be applied to some objects are stored only when those objects are defined, and cannot be used outside of that environment (that can be a class, for instance). 

The most important principle of object orientation is ***encapsulation***: the idea that data inside the object should only be accessed through a public *interface* – that is, the object’s methods.

In C++, private and public interfaces are rigorously separated by the `private:` and `public:` magic words, inside a class. **In Python, everything is public**, but there are conventional ways to define private attributes and methods: most of the times, we pre-pend an underscore `_` to the attribute or method that we are making “private”, so that it is, in a way, more difficult to access if you don’t have access to the source code.

Remember that OOP is meant to make life easier for the user: methods and objects are hidden inside classes and their implementation and documentation must be such that the user is not required to know the details to make the program work.  

It is customary to **set and get simple attribute values directly**, and only **write setter and getter methods for values which require some kind of calculation**. In the last chapter we learned how to use the property decorator to replace a simple attribute with a method without changing the object’s interface.

## Tips and ideas on how to build aggregated objects in a smart and effective way

- visualize your object (class) and add the attributes it should have (make arrows, draw!), even those attributes that you want to get after calculations
- define those calculations (methods): what enters and what is given out
- connect attributes with calculations
- do you need to make something private? remember you can do this with underscores and then provide @property decorated methods to return the attributes, and also setters, getters, deleters.
- if an attribute has a lot of methods that only are defined upon it, consider making another class and aggregating the two: to do this,

# Composition

Composition is a way of *aggregating* objects together by making some objects attributes of other objects.

This happens, in the most simple case, when you use an object of some class as an attribute of another class: having a DataFrame object as an attribute of a custom-defined class is an example of composition.

Composition is established between objects that are strongly linked to each other, as one belonged exclusively to the other. Aggregation is established between objects that can exist one without the other.

# Inheritance

Inheritance is a way of arranging objects in a hierarchy from the most general to the most specific. One can have one *parent class* or *superclass* with many *child classes* or *subclasses.* It can help in aggregating objects which have some common features and more specialized ones. 

## More about inheritance

# Avoiding inheritance