# 10 Classes

Created: February 10, 2022 9:53 AM
Rate: completed

# 10 Classes

A class is a kind of data type. When we create an object of the class data type, we call it an instance of a class.
In Python, everything is an object. I.e. every type of object is an instance of the class of that data type.

A class has attributes and methods:

- attribute: data values stored inside an object
- method: a function that can be applied to the instances of the class

# Defining and using a class

## Basic sintax

To make a class, use the keyword `class` followed by the name of this new class. It is conventional to use CamelCase for classes’ names. Then, follow the name with a colon.

The body of the class must be indented, of course, and no ending statement is required.

```python
class Person:
-->|
```

```python
import datetime # we will use this for date objects

class Person:

	# Initializer
    def __init__(self, name, surname, birthdate, address, telephone, email):
        self.name = name    # attributes are initialized with parameters passed to init
        self.surname = surname
        self.birthdate = birthdate
        self.address = address
        self.telephone = telephone
        self.email = email

	# Methods
    def age(self):
        today = datetime.date.today()
        age = today.year - self.birthdate.year
        if today < datetime.date(today.year, self.birthdate.month, self.birthdate.day):
            age -= 1
        return age

#----------------------------------- end of class -------------------------------------#

person = Person( # initialize an instance of the class via its __init__ method
    "Jane",
    "Doe",
    datetime.date(1992, 3, 12), # year, month, day
    "No. 12 Short Street, Greenville",
    "555 456 0987",
    "jane.doe@example.com"
)

print(person.name)
print(person.email)
print(person.age())
```

# Instance attributes

Instances' attributes can be specified by using the `init` method or by initializing them as variables inside the body of the `class` statement.
The parameter `self` is a variable that refers to the instance itself on which the method or the attribute is called. `self` is a conventional name, it would be the same to call it `pippo`. `self` is included as a parameter for any method of the class.

**Any attribute can be added to an instance on the fly: you can do it inside a method or even from outside the object.** Nonetheless, ***adding attributes outside `__init__` is BAD PRACTICE*** .

```
object.attribute
Out: value

object.method(parameters)
Out: result of method on object
```

## `__init__`

When we define a class we define all its methods as we would define normal functions.

A special method is `__init__`, called *initialiser* of the class, and does the same thing that the *constructor* of other languages (e.g. C++) does. **The method `init` initializes some attributes of the instances of the class.**

Note: `__init__` **can be omitted** (such as default constructors in C++).

## Private and public attributes

In Python, **all the attributes are public**, so we always have access to them. It is conventional to use the underscore `_` before the name of an attribute or a method to define that that object is private, but it's just a convention.

```python
class Person:
		# Initializer
    def __init__(self, name, surname, birthdate, address, telephone, email):
        self.name = name    # attributes are initialized with parameters passed to init
        self.surname = surname
        self.birthdate = birthdate
        self.address = address
        self.telephone = telephone
        self.email = email
				self._age = 0

	# Methods
    def age(self):
        today = datetime.date.today()
        age = today.year - self.birthdate.year
        if today < datetime.date(today.year, self.birthdate.month, self.birthdate.day):
            age -= 1
	###################### add a private attribute ######################
	# adding age as private only means that the correct way to get the age of the person
	# is to use the self.age() method, since the value stored in _age may be deprecated
	# after a while. Also if you call object.age from the outside you get nothing eheh
				self._age = age
        return age
```

## Set this, get that, has it?

In Python, there are built-in functions to set and get attributes’ values and check if an attribute exists. I repeat, these are **built-in functions** and not methods, they cannot be called on the class’ object, but instead they accept it as a parameter

```python
setattr(myobject, attribute, new_value)
getattr(myobject, attribute, new_value)
hasattr(myobject, attribute, new_value)
```

# Class attributes

```python
class Person:
	PRONOUNS = ('he','she','they') # notice that this is an immutable type
	def __init__(name, surname, pronouns, legal_pron=PRONOUNS)
		self.name = name
		self.surname = surname
		self.pronouns = []
		for pron in pronouns:
			if pron not in legal_pron:
				raise NameError("Please provide legal pronoun/s.\n")
			else:
				self.pronouns.append(pron)
	
#--------------------------------------#
Person.PRONOUNS # gives the tuple 'he', 'she', 'they'
Jacob = Person(Jacob, Malcom, ['he','they'])
Jacob.PRONOUNS # gives the same tuple, common to all instances of type Person
```

Instances' attributes make sense if we have created an instance of a certain class and passed some values for the attributes of the instance: so, instance attributes are all and only the attributes that can be passed to the *initializer* method `__init__`.

Class' attributes are fixed attributes that can be passed or are passed to all the new instances of the class. Since it is an attribute of the class, if the type defined by the class is, e.g. "Person", then we can access the class' attributes by `Person.ATTRIBUTES`.

Instances' attributes precede, in order of importance, class' attributes.

Class' attributes MUST BE OF IMMUTABLE TYPE because mutable types lead to casini mostruosi and would be changed for all instances of the same class. One can use mutable types for instance attributes, by using the `__init__` method to initialize them.

---

# Decorators

It happened to me to inspect a module (Pandas, for instance) while I was studying how to document my code in a tidy and uniform way. I looked at the class’ methods and I discovered tiny @ before some functions. Those are decorators.

Decorators (which exist for functions also) are “tags” appended to methods to “decorate” them with special properties. Decorated methods are more than just what the function tells you it’s doing.

```python
@decorator
def method():
	"""This is a decorated method"""
	...
```

## @classmethod

Allows the method to contain the class object itself as a parameter.

The `self` parameter must be renamed `cls` to make explicit that you may be acting on the class.

Common uses:

- setup() methods: they pre-process data and return it directly as an instance of the class

  

```python
class Person:

    def __init__(self, name, surname, birthdate, address, telephone, email):
        self.name = name
        # (...)

    @classmethod
    def from_text_file(cls, filename):
        # extract all the parameters from the text file...
        return cls(*params) # this is the same as calling Person(*params)

	#----------------------------------------------------------#

Jacob = Person.from_text_file("Jack.txt") # I have created an instance Jacob of Person
```

## @staticmethod

Makes the method independent from the parameter `self`, that is not passed to it.

```python
class Person:
    TITLES = ('Dr', 'Mr', 'Mrs', 'Ms')

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def fullname(self): # instance method
        # instance object accessible through self
        return "%s %s" % (self.name, self.surname)

    @classmethod
    def allowed_titles_starting_with(cls, startswith): # class method
        # class or instance object accessible through cls
        return [t for t in cls.TITLES if t.startswith(startswith)]

    @staticmethod
    def allowed_titles_ending_with(endswith): # static method
        # no parameter for class or instance object
        # we have to use Person directly
        return [t for t in Person.TITLES if t.endswith(endswith)]

	#----------------------------------------------------------#

# default initialization
jane = Person("Jane", "Smith")

# use instance method to access instance attribute
print(jane.fullname())

# use classmethod to access class attributes via cls or self
print(jane.allowed_titles_starting_with("M"))
print(Person.allowed_titles_starting_with("M"))

# use staticmethod to access class attributes via cls or self
print(jane.allowed_titles_ending_with("s"))
print(Person.allowed_titles_ending_with("s"))

# the main difference bet classmethod and staticmethod is in the implementation
# of the function itself
```

Common uses:

- in classes that are built just as a collection of methods, but in which all those methods do not call each, and there’s no instance to access
- methods that are free functions that you’re putting inside the class but you want to preserve as free
- to access both class and instance attributes

## @property, setters and getters

Makes the method behave like an attribute: when you call it, no brackets! 

Common uses:

- to make (true) setters and deleters, methods that access the attributes and change their value or delete the objects

```python
class Person:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    @property
    def fullname(self):
        return "%s %s" % (self.name, self.surname)

    @fullname.setter
    def fullname(self, value):
        # this is much more complicated in real life
        name, surname = value.split(" ", 1)
        self.name = name
        self.surname = surname

    @fullname.deleter
    def fullname(self):
        del self.name
        del self.surname

	#----------------------------------------------------------#

jane = Person("Jane", "Smith")
print(jane.fullname)

jane.fullname = "Jane Doe"
print(jane.fullname)
print(jane.name)
print(jane.surname)
```

# Objects’ properties

## Magic methods

- `__init__`: the initialisation method of an object, which is called when the object is created.
- `__str__`: the string representation method of an object, which is called when you use the `str` function to convert that object to a string (ex. print(str(object)) will work)
- `__dir__`: it returns the list of all the attributes, methods and properties of an object, and all of its inherited features
- `__class__`: an attribute which stores the the class (or type) of an object – this is what is returned when you use the `type` function on the object.
- `__eq__`: a method which determines whether this object is equal to another. There are also other methods for determining if it’s not equal, less than, etc.. These methods are used in object comparisons, for example when we use the equality operator `==` to check if two objects are equal.
- `__add__` is a method which allows this object to be added to another object. There are equivalent methods for all the other arithmetic operators. Not all objects support all arithemtic operations – numbers have all of these methods defined, but other objects may only have a subset.
- `__iter__`: a method which returns an iterator over the object – we will find it on strings, lists and other iterables. It is executed when we use the `iter` function on the object.
- `__len__`: a method which calculates the length of an object – we will find it on sequences. It is executed when we use the `len` function of an object.
- `__dict__`: a dictionary which contains all the instance attributes of an object, with their names as keys. It can be useful if we want to iterate over all the attributes of an object. `__dict__` does not include any methods, class attributes or special default attributes like `__class__`.

### Magic methods overload

- `__init__`: is overridden almost by default if you want a non-default initializer
- `__str__`: useful to override to print all the interesting attributes of the instance

```python
# overridden string representation that is more useful than just the class name and an ID for identification of the object (default str return)

def __str__(self):
        return "%s %s, born %s\nAddress: %s\nTelephone: %s\nEmail:%s" % (self.name, self.surname, self.birthdate, self.address, self.telephone, self.email)
```

- `__eq__` and other comparison methods: you are encouraged to override them since it would make no sense to check if a Person is bigger than another, but you could compare their heights!

```python
class Person:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def __eq__(self, other): # does self == other?
        return self.name == other.name and self.surname == other.surname

    def __gt__(self, other): # is self > other?
        if self.surname == other.surname:
            return self.name > other.name
        return self.surname > other.surname

    # now we can define all the other methods in terms of the first two

    def __ne__(self, other): # does self != other?
        return not self == other # this calls self.__eq__(other)

    def __le__(self, other): # is self <= other?
        return not self > other # this calls self.__gt__(other)

    def __lt__(self, other): # is self < other?
        return not (self > other or self == other)

    def __ge__(self, other): # is self >= other?
        return not self < other
```

- `__add__` is a method which allows this object to be added to another object. There are equivalent methods for all the other arithmetic operators. Not all objects support all arithemtic operations – numbers have all of these methods defined, but other objects may only have a subset.
- `__iter__`: a method which returns an iterator over the object – we will find it on strings, lists and other iterables. It is executed when we use the `iter` function on the object.
- `__len__`: a method which calculates the length of an object – we will find it on sequences. It is executed when we use the `len` function of an object.
- `__dict__`: a dictionary which contains all the instance attributes of an object, with their names as keys. It can be useful if we want to iterate over all the attributes of an object. `__dict__` does not include any methods, class attributes or special default attributes like `__class__`.

---

# Defyning functions outside the class’ body and a bit of object-orientation

[Define a method outside of class definition?](https://stackoverflow.com/questions/9455111/define-a-method-outside-of-class-definition)

> Yes. You can define a function outside of a class and then use it in the class body as a method:
> 

> def func(self):
    print("func")

class MyClass:
    myMethod = func
> 

> You can also add a function to a class after it has been defined:
> 

> class MyClass:
    pass

def func(self):
    print("func")

MyClass.myMethod = func
> 

> You can define the function and the class in different modules if you want, but I'd advise against defining the class in one module then importing it in another and adding methods to it dynamically (as in my second example), because then you'd have surprisingly different behaviour from the class depending on whether or not another module has been imported.
> 

> I would point out that while this is possible in Python, it's a bit unusual. You mention in a comment that "users are allowed to add more" methods. That sounds odd. If you're writing a library you probably don't want users of the library to add methods dynamically to classes in the library. It's more normal for users of a library to create their own subclass that inherits from your class than to change yours directly.
> 

> I'd also add a reminder that functions don't have to be in classes at all. Python isn't like Java or C# and you can just have functions that aren't part of any class. If you want to group together functions you can just put them together in the same module, and you can nest modules inside packages. Only use classes when you need to create a new data type, not just to group functions together.
>