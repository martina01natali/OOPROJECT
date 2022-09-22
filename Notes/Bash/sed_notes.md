# sed notes

Created: March 10, 2022 10:34 AM
Status: To review

# References

[Sed - An Introduction and Tutorial by Bruce Barnett](https://www.grymoire.com/Unix/Sed.html#toc_Sed_-_An_Introduction_and_Tutorial_by_Bruce_Barnett)

[]()

[]()

[https://www.notion.so](https://www.notion.so)

[https://www.notion.so](https://www.notion.so)

[https://www.notion.so](https://www.notion.so)

[https://www.notion.so](https://www.notion.so)

# A brief, very brief, very sad intro to `sed`

### What the actual flac this sintax is crazy

Yes. But *sed*ly it is very useful.

## s for substitution

This is the main task you want to complete with sed: substitute anything inside a file with millimetric precision. The basic sintax is

```
sed 's/substitute this/with this/' <from_old_file >to_new_file

```

With this sintax a) I am using no regular expressions; b) I will substitute the string "substitute this" inside any line of a file but just for the first time it appears; c) I am using / as the delimiter for sed but I could use any character, really, such as | or _

- matched string can be referred to using &, e.g.

```
echo "123 abc" | sed 's/[0-9]*/& &/'
123 123 abc

```

- "all lower letters" or "all numbers" can be referred to using **ranges** in square brackets, e.g. [a-z], [0-9], [A-Z]
- all kinds of regular expressions are welcome, sed is an inclusive environment
- extended regular expressions are welcome but need **r** as an option of sed to be undestood correctly, e.g. [0-9]* is equal to saying [0-9]+ but the latter is an extended regular expression
- keep parts of the pattern: you can store/remember up to 9 patterns with sed, recalling them with \1, \2, etc... To keep part of a pattern and delete the rest, you have to use **escaped parentheses** \\( and \\), e.g.

```
echo abcd123 | sed 's/\\([a-z]*\\).*/\\1/'
abcd

```

- /g is global replacement and will act on the whole line any number of times