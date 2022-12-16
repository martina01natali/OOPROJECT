# 9 Errors and exceptions

Created: February 10, 2022 9:27 AM
Rate: in progress

# 9 Errors and exceptions

References:
[Errors and exceptions](https://docs.python.org/3/tutorial/errors.html)
[Built-in exceptions](https://docs.python.org/3/library/exceptions.html)
[Warnings](https://docs.python.org/3/library/warnings.html)

## try and except statements

```
try:
    ...
except (typeError_1, typeError_2,...):
    ...

```

To work with more than one type of errors you need to put the types in a tuple in the except statement (as in the above example).
To intercept one specific error the best thing to do is to put the least number of lines in the try statement.

Type of errors:

- ValueError
- IndexError
- ZeroDivisionError
- ...


### else and finally clauses

The clauses `else` and `finally` can be added to the  `try/except` statement. `else` allows you to do something if the exception is not raised, while `finally` allows to do something regardless of what happened before (error yes or error no).

---

## raise statement

The statement `raise` allows to force a specific/arbitrary exception to occur.

---

## warnings

Warning messages are typically issued in situations where it is useful to alert the user of some condition in a program, where that condition (normally) doesn’t warrant raising an exception and terminating the program. For example, one might want to issue a warning when a program uses an obsolete module.
The determination whether to issue a warning message is controlled by the warning filter, which is a sequence of matching rules and actions. Rules can be added to the filter by calling `filterwarnings()` and reset to its default state by calling `resetwarnings()`.

The warnings filter controls whether warnings are ignored, displayed, or turned into errors (raising an exception).
_action_ can be: "default", "error", "ignore", "always", "module", "once"
`warnings.simplefilter(action, category=Warning, lineno=0, append=False)`

Issue a warning, or maybe ignore it or raise an exception:
`warnings.warn(message, category=None, stacklevel=1, source=None)`
