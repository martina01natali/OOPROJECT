# 9 Errors and exceptions

Created: February 10, 2022 9:27 AM
Rate: in progress

# 9 Errors and exceptions

Useful links:
[Errors and exceptions](https://docs.python.org/3/tutorial/errors.html)

## try and except statements

```
try:
    ...
except (typeError_1, typeError_2,...):
    ...

```

To work with more than one type of errors you need to put the types in a tuple in the except statement.
To intercept one specific error the best thing to do is to put the least number of lines in the try statement.

Type of errors:

- ValueError
- IndexError
- ZeroDivisionError

[Built-in exceptions](https://docs.python.org/3/library/exceptions.html)

### else and finally clauses

The clauses `else` and `finally` can be added to the  `try/except` statement. `else` allows you to do something if the exception is not raised, while `finally` allows to do something regardless of what happened before (error yes or error no).

---

## raise statement

The statement `raise` allows to force a specific exception to occur.
