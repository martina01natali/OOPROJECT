# 7 Functions

Created: February 10, 2022 9:27 AM
Rate: completed

# 7 Functions

A function is a sequence of statements which performs some kind of task. We use functions to eliminate code duplication – instead of writing all the statements at every place in our code where we want to perform the same task, we define them in one place and refer to them by the function name.

*def* callable: you can call it as a function (with () at the end) and you could also define new objects of the same class as the callable we are using.

```python
> def my_func():
> 	print("Hello!")
> alias = my_func
> alias()
Out: Hello!
```

**A function has only a single return**, BUT the return of a function can be made up by a lot of elements: in this case the return ***packs*** them into a tuple (if they are separated by commas). Once a tuple is returned, you have to ***unpack*** it by assigning a number of variables to the output of the function equal to the number of elements in the tuple

```python
def multiple_returns(a,b,c)
	return a,b,c
a, b, c = multiple_returns(1,2,3)
```

---

## Default parameters

In C the *signature* of a function is defined by its *name + # parameters*.

In Python the *signature* of a function is defined ***only by its name***.

Optional parameters: need to be put at the end of the sequence of parameters, and must be defined with a **default value** so that we can neglect them when passing arguments.
To pass arguments to the function one has to **pass positional arguments BEFORE arguments passed with their keyword**.

### Mutable types

Be damn careful when passing lists and mutable types as parameters of a function, cause if you modify them in place and return them you could make big mistakes. The right thing to do is the following:

```
def add_pet_to_list(pet, pets=None):
    if pets is None:
        pets = []
    pets.append(pet)
    return pets
```

---

## *args and **kwargs

Sometimes we may want to pass a variable-length list of positional or keyword parameters into a function. We can put *** before a parameter name to indicate that it is a *variable-length tuple of positional parameters***, and we can use ** to indicate that a parameter is a ***variable-length dictionary of keyword parameters*.** By convention, the parameter name we use for the tuple is args and the name we use for the dictionary is kwargs.
Inside the function, we can access args as a normal tuple, but the * means that args isn’t passed into the function as a single parameter which is a tuple: instead, it is passed in as a series of individual parameters. Similarly, ** means that kwargs is passed in as a series of individual keyword parameters, rather than a single parameter which is a dictionary.
If we decide to pass a previously-defined tuple or dictionary, we need to unpack them inside the signature of the function, and to do that we have to use * or ** when we are calling a function to unpack a sequence or a dictionary into a series of individual parameters.

---

## Decorators

***Decorators are functions that modify other functions.***

**Once you have defined a decorator** (in this case, `log`), there is a shorthand syntax for applying it to functions: we can use the @ symbol together with the decorator name before the definition of each function that we want to decorate.

```python
# we define a decorator
def log(original_function):
    def new_function(*args, **kwargs):
        with open("log.txt", "w") as logfile:
            logfile.write("Function '%s' called with positional arguments %s and keyword arguments %s.\n" % (original_function.__name__, args, kwargs))

        return original_function(*args, **kwargs)

    return new_function

# here is a function to decorate
def my_function(message):
    print(message)

# and here is how we decorate it
my_function = log(my_function)
```

```python
@log
def my_function(message):
    print(message)
```

@log before the function definition means exactly the same thing as my_function = log(my_function) after the function definition.

---

## Lambda Functions

Lambda functions are very simple functions (they are meant to be so) that can be written inline.

```python
summed = lambda x,y : x+y
summed(1,2)
Out: 3
```

---

## **Generator functions and `yield`**

We have already encountered generators – sequences in which new elements are generated as they are needed, instead of all being generated up-front. We can create our own generators by writing functions which make use of the `yield` statement.

Consider this simple function which returns a range of numbers as a list:

```python
def my_list(n):
    i = 0
    l = []

    while i < n:
        l.append(i)
        i += 1

    return l
```

This function builds the full list of numbers and returns it. We can change this function into a generator function while preserving a very similar syntax, like this:

```python
def my_gen(n):
    i = 0

    while i < n:
        yield i
        i += 1
```

The first important thing to know about the `yield` statement is that if we use it in a function, that function will return a generator. We can test this by using the `type` function on the return value of `my_gen`. We can also try using it in a `for` loop, like we would use any other generator, to see what sequence the generator represents:

```python
g = my_gen(3)

print(type(g))

for x in g:
    print(x)
```

What does the `yield` statement do? Whenever a new value is requested from the generator, for example by our `for` loop in the example above, the generator begins to execute the function until it reaches the `yield` statement. The `yield` statement causes the generator to return a single value.

After the `yield` statement is executed, execution of the function does not end – when the *next* value is requested from the generator, it will go back to the beginning of the function and execute it *again*.

If the generator executes the entire function without encountering a `yield` statement, it will raise a `StopIteration` exception to indicate that there are no more values. A `for` loop automatically handles this exception for us. In our `my_gen` function this will happen when `i` becomes equal to `n` – when this happens, the `yield` statement inside the `while` loop will no longer be executed.