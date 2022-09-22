# 4 If statements

Created: February 10, 2022 9:25 AM
Rate: completed

# 4 If statements, or selection control statements

The flow of control is the order in which a program executes the statements of which it is made of. In procedural languages, the flow of control is given by the order in which the statements are written. On the other hand, in object-oriented programming languages the flow of control is given by the order of the functions and methods that are used and their implementation.

Selection control statements are one of the ways in which programmers can change the flow of control, by using conditions to move the direction and the order in which actions are executed.

## Selection control statements: if statements

If is a compound statement, that is comprised by one or more *clauses*, each with a *header* (if, elif, else, etc.) and a *suite* (the body) which contents are delimited with indentation.

```
if condition:
    print("bodyodyodyody")
```

Shorthand sintax: use anything as it was a boolean and python will read it as it was so. Recall that everything that is non-null is True, while 0 and other built-ins that are considered "empty" (e.g. None, NaN) are False. So if something is not null, by shorthand sintax it will evaluated as True. E.g.

```
string = "String!"
if string:
    print("It is indeed True")

# Out: It is indeed True
```

### Relational operators

| Operator | Description |
| --- | --- | 
| ==          | equal or value comparison|
| !=          | not equal|
| <=/>=       | less or equal/greater or equal|
| is          | identity comparison: true if (;)) the objects that are compared are actually different aliases of the same object|
| is not    | opposite of identity comparison|

### Clauses

- `else`: allows to specify an alternative instruction to be executed if the condition is not met
- `elif`: allows to create an *if ladder*, meaning an if clause followed by an arbitrary number of elif clauses that provide alternative conditions without the need for nesting multiple ifs

### Conditions with boolean operations

- `and`: true if both true: notice that is a short-circuit evaluation, meaning that if the first element is false, it does not evaluate the second one: this can be used as an advantage when evaluating expressions that could possibly give an error if their argument is empty, in which case you just have to check that it is not empty beforehand in the first part of the AND;
- `not`: elegant way to do something if something is False; notice that the sintax is `if not something`;
- `or`: true if at least one is true;


### Dictionaries and collections of things

Similar to if ladders are switch statements, that in python don't exist. Switch statements test the value of a single variable and makes a decision on the basis of that value. We can achieve something similar using dictionaries, that are collections in which a certain object is retrieved via its key. The object can be a string, a number of even a function. To use a function funct(**args) as an object in a dictionary be sure to call it without the brackets, just by its name `funct`.

“Switch statements” in python written with a dictionary can be made by iterating on the keys or values or all items of the dictionary.

```
DICTIONARY = {
    "key" = object
    ...
}

if key in DICTIONARY: # tests if key is an actual key of DICTIONARY
	print(DICTIONARY[key]) # prints the values of the keys of DICTIONARY
```

## Conditional operator

The conditional operator is also known as *ternary operator* because it has *three* operands. We can find it in both python and c++, among others.
Basic sintax: true expression `if` condition `else` false expression

```
result = "Pass" if (score >= 18) else "Fail"

```
