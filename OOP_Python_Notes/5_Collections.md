# 5 Collections

Created: February 10, 2022 9:26 AM
Rate: completed

# 5 Collections

## Lists

***Lists are MUTABLE sequences of objects of any type, separated by commas and limited by square brackets. Elements are callable by their index number between [].***

```
list
```

is the built-in type of list in Python, and is a type of sequence that stores values sequentially.

Lists are mutable types while variables are immutable: this means that an operation that changes the value or the structure of a list affects the list completely, so if you don't assign the value of the modified list to another alias, the starting list will be changed.

We can access the values by their *index number* which starts from 0. The important thing to remember is that negative index values are allowed and -1 corresponds to the last element of the list, -2 to the one before the last and so on and so forth.

Lists can contain different types of values.

### Defining lists

***Naming convention: lower case letters, plural and explicit names without underscores***

```
# define an empty list like this and memory will be dynamically
# allocated, meaning that you can append an arbitrary number of
# elements to the empty-starting list

list = []

list1 = [
    object,
    second object, #trailing comma is allowed
]

```

Checking if a specific value is contained in the list:

```
numbers = [1,2,3]
my_number = 2

if my_number in numbers:
    print("%d is in the list", % number)

```

### Slicing

Consider a portion of a list by defining the range of interest.
Warning: when defining a range, the element at the upper bound is always excluded from the selection.

Ranges

general: `[start:end:step]`

all the elements: [:]

all the elements from the 2nd on (watch the index number): [1:]

### Methods and functions

### Built-in functions

```bash
len(list)
sum(listofnumbers)
any([0,1,0,1]) # is any element True # out = True/False
all([0,1,0,1]) # are all the elements True # out = True/False
newlist = list(oldlist) # Making a copy of a list:
```

### Methods to call on lists

A method is something that acts on an instance of a given class,

```

numbers.append(value_to_add_to_the_end) # we already saw how to add an element to the end

numbers.count(value) # count how many times a value appears in the list

numbers.extend(list) # append an entire list to the initial list

numbers.index(value) # find the index of a value, if it is present more than once, we will get the index of the first one

numbers.index(out_of_range) # if the value is not in the list, we will get a ValueError!

numbers.insert(index, value) # insert a value at a particular index

my_number = numbers.pop(index) # remove an element by its index and assign it to a variable

numbers.remove(value) # remove an element by its value, removes only the first one found with a certain value

# Sorting:
in place        list.sort(**kwargs, reverse = False)
output copy     lists = sorted(list, **kwargs, reverse = False)

# Reversing:
in place        list.reverse()
output copy     listr = list(reversed(list)) # need to cast the output of reversed because it actually returns a generator, not a list

```

### Arithmetic operators

Arithmetic operators act on list in a sense in the same way they act on strings. In fact, you cannot do arithmetic operations on the elements of the list by just making them on the list itself.

Operator    Description
+          concatenate two lists
*          concatenate with itself an arbitrary number of times

```bash
> [1,2]+[3,4] # concatenation
Out: [1,2,3,4]
> [1,2]*2 # concatenated repetition
Out: [1,2,1,2]
```

---

## Arrays VS Lists

[array - Efficient arrays of numeric values - Python 3.10.2 documentation](https://docs.python.org/3/library/array.html)

In Python, there is a built-in `array` type, which can be resized dynamically, as a list, and follows certain rules: needs a specification on the type of elements it will store and it can only store numbers.
The most commonly used array types in python are numpy arrays, that are NOT AT ALL THE BUILT-IN ARRAY TYPE of Python.

## Numpy arrays

[NumPy: the absolute basics for beginners - NumPy v1.22 Manual](https://numpy.org/doc/stable/user/absolute_beginners.html)

The above user guide for beginners contains all the information one would need most of the times. Important things are:

- sum (+) and difference (-) between arrays of equal shape returns an array which elements are the sum of the elements
- .shape gives you the shape of the array/matrix and .reshape(...) makes you able to reshape a linear array in another form

---

## Tuples

***Tuples are IMMUTABLE sequences of objects of any type separated by commas and limited by round brackets. Indexing is made calling index number between [].***

***Naming convention: same as lists, but since they are an IMMUTABLE type, if they are supposed to be constants the name takes the upper case***

Tuples are similar to lists but they are an immutable type, and are useful to define constants that are supposed to not be modified.

Definition for tuple literal: comma-separated list of values inside round brackets.

```
tuple = (object1,) # single element tuple

tuple1 = (object1, object2, ...)

```

Access to elements via index number is the same as for lists (with square brackets). You cannot append, remove or modify any element of the tuple. Tuples are used when you want something that cannot be changed accidentally.

Are mostly used in `print`, e.g.

```
> print('%s %s %s' % ('this','is a nice','string'))
this is a nice string

```

---

## Sets

***A set is MUTABLE collection of UNIQUE, UNORDERED elements. Elements cannot be accessed by their index number or key, because they have no index.***

The Python set type (= ***insieme***) is called `set`.

A `set` can contain only **immutable objects, of any type**, and objects of different types can live together.

If we add multiple copies of the same element to a set, the *duplicates will be eliminated*, and we will be left with one of each element.
Sets are **not ordered**, meaning that each time they are printed the order of the elements change.

Definition for set literal: comma-separated list of values inside curly brackets \{ and \}.
Warning: empty brackets {} will define an *empty dictionary* instead of an empty set. To make an empty set, use the `set` constructor:

```python
empty = set() # this is an empty set
from_iter = set(<iter>) # initialization using an iterable (such as range(), or a string!)
from_item = {item} # this is a set
```

```python
set.add(element) # adds an element, modifies directly the set since this is a mutable object
set.remove(element)
set.discard(element) # removes element but doesn't raise an exception if element is not found
set.pop() # removes random element
set.clear() # removes all elements
```

### Operations on sets

| Operator | Function | Description |
| --- | --- | --- |
| - | .difference() | Subtracts elements |
| | | .union() | Unites elements |
| & | .intersection() | Returns the intersection of two sets |
| ^ | .symmetric_difference() | Xor operation, returns the union minus the intersection |

### Modifying a set

| Operator | Function | Description |
| --- | --- | --- |
| -= | .difference_update() | Subtracts elements |
| |= | .update() | Modify by union of elements |
| &= | .intersection_update() | Returns the intersection of two sets |
| ^= | .symmetric_difference_update() | Xor operation, returns the union minus the intersection |

## Ranges

The type `range` is another kind of **immutable sequence** type of numerical, integer values. It is very specialised – we use it to create ranges of integers. Ranges are also generators. We will find out more about generators in the next chapter, but for now we just need to know that the numbers in the range are generated one at a time as they are needed, and not all at once.

```
range(start,end,step)
```

If we pass a single parameter to the range function, it is used as the upper bound. If we use two parameters, the first is the lower bound and the second is the upper bound. If we use three, the third parameter is the step size. The default lower bound is zero, and the default step size is one. Note that the range includes the lower bound and excludes the upper bound.

## Dictionaries

The Python dictionary type is called `dict`. We can use a dictionary to store key-value pairs.
Definition for a dictionary literal: comma-separated list of key-value pairs between curly brackets. We use a colon to separate each key from its value.

We access values in the dictionary by their *key* as index "number", between square brackets.

The **keys can be *any immutable type*,** including numbers and even tuples. We can *mix different types of keys and different types of values* in one dictionary. **Keys are unique** – if we repeat a key, we will overwrite the old value with the new value.
When we store a new value in a dictionary, we define its key as well even if it didn't exist.

Like sets, **dictionaries are not ordered** – if we print a dictionary, the order will be random.

### Methods and objects

The most important methods are **dict.keys(), dict.values(), dict.items()**.

```
marbles = {"red": 34, "green": 30, "brown": 31, "yellow": 29 }

# Get a value by its key, or None if it doesn't exist
marbles.get("orange")
# We can specify a different default
marbles.get("orange", 0)

# Add several items to the dictionary at once
marbles.update({"orange": 34, "blue": 23, "purple": 36})

# All the keys in the dictionary
marbles.keys()
# All the values in the dictionary
marbles.values()
# All the items in the dictionary
marbles.items()

# Check if a key is in the dictionary using in and not in

print("purple" in marbles)
print("white" not in marbles)

# Check if a value is in the dictionary using in in conjunction with the values method:

print("Smith" in surnames.values())

```

You should avoid using mykey in mydict.keys() to check for key membership, however, because it’s less efficient than mykey in mydict.

---

## Converting between collection types

### Implicit conversions

If we try to iterate over a collection in a for loop, Python will try to convert it into something that we can iterate over if it knows how to.

Sometimes the iterator we get by default may not be what we expected – if we iterate over a dictionary in a for loop, we will iterate over the keys. If what we actually want to do is iterate over the values, or key and value pairs, we will have to specify that ourselves by using the dictionary’s values or items view instead.

### Explicit conversions

We can convert between the different sequence types quite easily by using the type functions to cast sequences to the desired types

If we convert the key-value pairs of a dictionary to a sequence, each pair will be converted to a tuple containing the key followed by the value.

We can also convert a sequence to a dictionary, but only if it’s a sequence of pairs – each pair must itself be a sequence with two values.

---

## Another look at strings

Strings are also a kind of sequence type – they are sequences of characters, and share some properties with other sequences. For example, we can find the length of a string or the index of a character in the string, and we can access individual elements of strings or slices

Remember that strings are immutable – modifying characters in-place isn’t allowed.

The membership operator has special behaviour when applied to strings: we can use it to determine if a string contains a single character as an element, but we can also use it to check if a string contains a substring:

```
print('a' in 'abcd') # True
print('ab' in 'abcd') # also True

# this doesn't work for lists
print(['a', 'b'] in ['a', 'b', 'c', 'd']) # False

```

To join a sequence of characters (or longer strings) together into a single string, we have to use `join`. This is not a function or a sequence method – it’s a **string method** which takes a sequence of strings as a parameter. When we call a string’s join method, we are using that string to glue the strings in the sequence together. For example, to join a list of single characters into a string, with no spaces between them, we call the join method on the empty string. We can use any string we like as a separator between single elements joined together.

```
list = ['a','b','c']
string = "".join(list)
string = ",".join(list) # comma-separated

# a space-separated list
print(" ".join(list))

# a comma-separated list
print(",".join(list))

# a comma-separated list with spaces
print(", ".join(list))
```

The opposite of joining is splitting. We can `split` up a string into a list of strings by using the split method. If called without any parameters, split divides up a string into words, using any number of consecutive whitespace characters as a delimiter. We can use additional parameters to specify a different delimiter as well as a limit on the maximum number of splits to perform:

```
print("cat dog fish\\n".split())
print("cat|dog|fish".split("|"))
print("cat, dog, fish".split(", "))
print("cat, dog, fish".split(", ", 1))
```

---

## Two-dimensional sequences

Most of the sequences we have seen so far have been one-dimensional: each sequence is a row of elements. What if we want to use a sequence to represent a two-dimensional data structure, which has both rows and columns? The easiest way to do this is to make a sequence in which each element is also a sequence.

Of course we can also make a list of lists of lists of lists and so forth – we can nest lists as many times as we like.

```
timetable = [[""] * 24 for day in range(7)]

```

Here we construct the timetable with a list comprehension.