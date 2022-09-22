# 12 Packaging and testing

Created: March 10, 2022 6:11 PM
Rate: in progress

[Packaging and testing - Object-Oriented Programming in Python 1 documentation](https://python-textbok.readthedocs.io/en/1.0/Packaging_and_Testing.html)

# 12 Packaging and testing

# Modules

***Modules are files of source code***, that can be installed and can contain classes, functions and so on and so forth.

Modules can be imported if the source is located in the same directory as the script you’re running, but can be also packaged and installed to be accessed from anywhere.

# Packages

***Packages are collections of modules.***

## Using `Distribute`

`Distribute` is a library for crating Python Packages, and can be installed directly with `pip`

```bash
pip install distribute
```

Ref: [https://pypi.org/project/distribute/](https://pypi.org/project/distribute/)

## Step-by-step package building

1. arrange your source codes into the typical directory structure which packaging tools expect:

```python
ourprog/
    ourprog/
        __init__.py
        db.py
        gui.py
        rules.py
    setup.py
```

We have created two new files. `__init__.py` is a special file which marks the inner `ourprog` directory as a package, and also allows us to import all of `ourprog` as a module. We can use this file to import classes or functions from our modules (`db`, `gui` and `rules`) into the package’s namespace, so that they can be imported directly from `ourprog` instead of from `ourprog.db`, and so on – but for now we will leave this file blank.

The other file, `setup.py`, is the specification for our package. Here is a minimal example:

```python
from setuptools import setup

setup(name='ourprog',
    version='0.1',
    description='Our first program',
    url='http://example.com',
    author='Jane Smith',
    author_email='jane.smith@example.com',
    license='GPL',
    packages=['ourprog'],
    zip_safe=False,
)
```

We create the package with a single call of the `setup` function, which we import from the `setuptools` module. We pass in several parameters which describe our package.

### **Installing and importing our modules**

Now that we have written a `setup.py` file, we can run it in order to install our package on our system. Although this isn’t obvious, `setup.py` is a script which takes various command-line parameters – we got all this functionality when we imported `setuptools`. We have to pass an `install` parameter to the script to install the code. We need to input this command on the commandline, while we are in the same directory as `setup.py`:

`python3 setup.py install`

If everything has gone well, we should now be able to import `ourprog` from anywhere on our system.

# Documentation

[Documentation guide](https://www.notion.so/Documentation-guide-aef8cfee8ef04a4f8ad1fe36eaf790e3)

# Testing

[Getting Started With Testing in Python - Real Python](https://realpython.com/python-testing/)