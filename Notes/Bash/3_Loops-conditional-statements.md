# 3 - Loops and conditional statements

Created: March 10, 2022 10:34 AM
Status: Completed

# References

[]()

[]()

## Loops

But first: variables
To define a variable in bash
`namevariable=value` 		(NO VOIDS!)
To call the value of the variable
`echo $namevariable`		(prints value of variable)

### General form of a loop in bash:

```bash
for thing in list_of_things
do
operation using $thing
done
```

- list_of_things is an actual list of files whose names are not separated by anything ie file1.txt file2.txt; don't try to cheat: you can't pipe a file whose lines are the list_of_things that you want, cause it won't see it like that. But you can use wildcards as you would do with ls: something like "in *.dat" will give you a loop over all .dat files
    - you can have spaces-separated names in bash: if so, just enclose your filenames in quotes and all the white space will become real; to loop over these files you have to call the value of the variable inside quotes, ie "$filename"
- $ means "take the value the variable is assuming at this moment"
- you can separate the different lines of the loop by a semicolon ;

[reduced, 1-line version] for thing in list_of_things; do operation using $thing; done

### Operations inside a loop

`echo`                    this prints on the screen

`cat file > smw.file`     this is used if you wanna write what is contained in file in smw.file inside a loop;
`>> smt.file`                     use this to append any string (echoed) to a file

### Already constructed loops to do simple things

Note: using echo before any other operation involving values of the variables but giving no output would give us the actual operation executed, since it reads the values of variables

### Make a copy of files of a given type

```bash
for filename in *.file
do
cp $filename original-$filename
done
```

---

## If statements and company

[If tutorial for Bash](https://ryanstutorials.net/bash-scripting-tutorial/bash-if-statements.php)

General syntax:

```
if [ <some test> ]
then
    commands
fi
```

Common tests:

- !EXPRESSION means expression is false
- n string means length of string is > 0
- z string means length of string is < 0
- d FILE means FILE exists and is directory
- e FILE means FILE exists
- s FILE exists and its size is > 0

### Boolean operators

- && means AND
- || means OR

### All the possible mechanisms

- else: if test is false then perform a different set of commands wrt if
- elif: if the previous test returned false then try this one

### Case mechanism

If you have a single variable that can match a series of patterns, you can do something like making a dictionary of those possible values and assign a different result to each.

```
case <variable> in
<pattern 1>)
    <commands>
;;
<pattern 2>)
    <other commands>
;;
esac

```