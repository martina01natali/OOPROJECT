# 6 Loops

Created: February 10, 2022 9:27 AM
Rate: completed

# 6 Loop Control statements

There are two types of statements in python: `for` and `while`.
In general, programming loops can be divided in **counting loops** (for) and **event-controlled loops** (while).

## while statement

***Body of while is repeated until the condition is not met anymore.***

```
while condition:
    body
```

`while` is an event-controlled kinda loop that **checks that the condition is true *before* doing anything**. It is composed by three parts:

- initialisation: variable definition
- condition: test on the variable, if true go on and execute the body
- update: update of the variable

---

## for statement

***Body of for is repeated for every element of a collection: mind that I said collection, not sequence ;) You can iterate on lists, sets, tuples, ranges (so generators even).***

```python
for element in collection: # iteration over a collection
	do this...

for i in range(10): # this is what I would do with a counter
	print(i)

for n, element in enumerate(collection): # with enumerate I can loop over the indexes and the values
	print("Element n. %d is %f" % (n, element))
```

### Important examples

### Modifying a list

You should avoid removing or adding elements to a list: by doing so you would modify the indexes and inevitably make some errors. You should do instead a list comprehension.

### for loops in other languages

**Java**

```java
for (int count = 1; count <= number; count++) {
    System.out.println(count);
}
// this syntax is equal in C++
```

In Java, as in C and C++, `for` loops are just special cases of the while loop where the initialisation of the variable, the condition and the update are all inside the parentheses of the statement. Basically, you use `for` loops to perform an operation on every element of some sequential collection.
In Python, on the other hand, you can iterate over sequences directly, assigning your variable as an element of the sequence itself and removing the need to iterate on the index number and updating the variable.

---

## Iterables, iterators and generators

Any type of object which can be iterated over in a for loop is an iterable.

Any variable that keeps your place in an iteration is an iterator.

A **generator** is an **iterable function** that restitutes a value for the iterator only when *called inside an iteration*.

### Built-in generator functions

- range(start,end,step)
- enumerate(list) = returns a tuple (index,element)
- zip(iterable1,iterable2,...) = combines multiple iterables pairwise, iterating over the n-th entry of all the iterables each time
- many functions in the `itertools` module, that are called as methods of the module:
    - itertools.count(lower_bound,step) = similar to range, but with no upper bound
    - itertools.cycle(iterable) = repeats the values of iterable
    - itertools.repeat(value,ntimes) = to repeat value an infinite number of times you only have to omit ntimes
    - itertools.chain(iterable1,iterbale2,...) = combines iterables sequentially

---

## Comprehensions

You know this is what the hype's all about.

***Comprehensions are a way to produce an iterable by filtering another iterable in a compact way. You can produce any type of collection with comprehensions.***

Basic sintax:
new_iterable = (new_element for iterator in old_iterable if condition)

- new_element = the "body" of the loop, so the element to be inserted in iterable at each iteration
- for iterator in old_iterable = a normal for loop that we use to iterate over old_iterable
- if condition = if you want you can add an if condition
- **parentheses** define what kind of iterable our comprehension will give us:
    - ( ) = generator
    - [ ] = list
    - { } = set
    - { } = dict if new_element = key:value

Be aware that you can pass a comprehension as an argument of a function, as always. E.g. if you're making a generator comprehension, and passing it inside a function, you can leave the round parentheses out,

```
sum_even = sum(2*number for number in range(11))

```

---

## Break or continue your journey

The statements `break` and `continue` are used to modify the flow of control of the loop.
The `break` statement causes the immediate exit from the loop body.
The `continue` statement, on the other hand, breaks the single iteration that is happening and makes the loop jump to the next one.

### `break`ing down *do-while* statements

Python doesn't have a built-in `do-while` statement: this kinda loop checks the condition *after* the execution of the body, that in such a way is executed at least once. One can make amend for it in 2 ways:

- while loop that is always true (while True:) and using a nested if statement that contains `break`
- assigning the variable outside of the loop in such a way that at least for the first iteration the while is true, and then the variable is updated inside the body

---

## Exercises

### Exercise 1

**a)** Write a program which uses a while loop to sum the squares of integers (starting from 1) until the total exceeds 200. Print the final total and the last number to be squared and added.
**Answ**

```
total = 0
number = 0

while total <= 200:
    total += number**2
    number += 1

print(total, i)

```

**b)** Write a program which keeps prompting the user to guess a word. The user is allowed up to ten guesses – write your code in such a way that the secret word and the number of allowed guesses are easy to change. Print messages to give the user feedback.

```
i = 0
nguess = 10
MAGIC_WORD = "Grazie"

while i<nguess:
    guess = input("Qual è la parolina magica?: ")
    if guess != MAGIC_WORD:
        print("Parolina magica sbagliata! Ritenta, hai ancora %d tentativi\\n" % 9-i)
        i += 1
    else:
        print('Parolina giusta ;)')
        i = nguess

```

### Exercise 3

**1.** Write a program which uses a nested for loop to populate a three-dimensional list representing a calendar: the top-level list should contain a sub-list for each month, and each month should contain four weeks. Each week should be an empty list.
**Ans**

```
i = 0
j = 0
calendar = []

for i in range(12):
    month = []
    for j in range(4):
        month.append([])
    calendar.append(month)

print(calendar)

```

**2.** Modify your code to make it easier to access a month in the calendar by a human-readable month name, and each week by a name which is numbered starting from 1. Add an event (in the form of a string description) to the second week in July.

```
# Recall that you want something that is ordered, so you need a sequential collection, not a set, nor a calendar, only lists are the correct iterable to use
MONTHS = ['January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September'
        'October',
        'November',
        'December',
        ]

for month in MONTHS:

```

**Sol**

```
i = 0
j = 0
calendar = []

for i in range(12):
    month = []
    for j in range(4):
        month.append([])
    calendar.append(month)

(January,February,March,April,May,June,July,August,September,October,November,December,) = range(12)
(w1,w2,w3,w4) = range(4)

calendar[July][w2].append('What is this aaaah') # it works dammit

```