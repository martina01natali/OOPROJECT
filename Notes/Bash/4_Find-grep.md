# 4 - Find and grep

Created: March 10, 2022 10:34 AM
Status: Completed

# References

[]()

[]()

## Finding things

The main characters of this section are the command `grep` and `find`
which is a contraction of "global/regular expression/print" and **finds and print lines in files that match a pattern**.
Notes:

- grep is case-sensitive.
- grep and find have a problem with regular expressions: e.g. if you leave *.txt when running grep string *.txt it will expand the wildcard * first (selecting only the .txt files in the directory you're working (no sub-directories)): to avoid this, enclose in double quotes

The sintax of `grep` is the following (more with man grep):
Comm Options

```
grep        print **lines** matching a given string and PATTERN
        Pattern matching
        -w      consider given string as word with boundaries
        -n      numbers the lines that match
        -i      make grep case-insensitive
        -v      invert sense of matching
        -e      followed by PATTERN can be used to use explicitly PATTERN as the pattern even if it begins with -
        Output control
        -r      search recursively in the whole directory and subdirectories
            string          string to look for, can contain spaces when surrounded by double quotes
                    file.type       in this file

```

The sintax of `find` is the following (more with man find or find --help):

### Comm Options

```
find        prints **name of files** matching a given cryterion and a given PATTERN
        PATTERN     can be given using regular expressions
            -type   d       directories
                    f       files
            -name       the name of the files match a given string, that will be given after this option
                    string_for_name.type
```

One can pass the output of find to another command by putting the command line containing find inside the brackets of $()
e.g. `grep string $(find here -name "*.type")`

### Using find and grep together

- Suppose we want to scan **all the lines** of selected files, then we should provide the command find inside round brackets and pass the output to grep
e.g. grep -opt "string" $(find somewhere -opt something)
- Suppose we want to scan just the **names** of selected files: then we have to pipe find and grep
e.g. find somewhere -opt "string" | grep -opt string

### Regular expressions introduction

def regular expressions = pattern that matches sets of related character strings

Note: when using regular expressions with grep, make sure you use the -E option and enclose the expression in double quotes

### Standard Wildcards

Symbol  Effect
?       replace 1 character

*       replace any number of characters

.*      replace from 0 to any number of characters
[]      specifies a range, gives all matching elements like a logical OR
[!]     logical NOT, "tranne"
{}      ensemble of patterns separated by commas, spaces not allowed!
|       logical OR, e.g. "a|b" matches strings containing a or b or both
\       escape to look for literal expressions

### Regular Expressions (will omit standard wildcards)

Symbol  Effect
.       match any single character, equivalent to ?
^       "the beginning of the line" (additions to the pattern must follow, not precede, the symbol)
$       "the end of the line"

### Categories of characters

[:upper:] uppercase letters
[:lower:] lowercase letters
[:alpha:] alphabetic (letters) meaning upper+lower (both uppercase and lowercase letters)
[:digit:] numbers in decimal, 0 to 9
[:alnum:] alphanumeric meaning alpha+digits (any uppercase or lowercase letters or any decimal digits)
[:space:] whitespace meaning spaces, tabs, newlines and similar
[:graph:] graphically printable characters excluding space
[:print:] printable characters including space
[:punct:] punctuation characters meaning graphical characters minus alpha and digits
[:cntrl:] control characters meaning non-printable characters
[:xdigit:] characters that are hexadecimal digits