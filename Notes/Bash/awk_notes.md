# awk notes

Created: March 10, 2022 10:34 AM
Status: To review

# References

[](https://likegeeks.com/awk-command/)

[]()

[https://www.notion.so](https://www.notion.so)

[https://www.notion.so](https://www.notion.so)

[https://www.notion.so](https://www.notion.so)

[https://www.notion.so](https://www.notion.so)

# An `awk`ward introduction to `awk`

## References
awk manual: run `man awk` on cmd line

## Basics

Basic shell sintax:
`awk options program file`

Options:

- `F$` means specify a file separator (substitute $ with your separator)
- `f` file means specify a file that contains an awk script
- `v` var=value means declare a variable

Define an awk script: you need to surround your commands with '{ }', what's on the inside will be executed.

Awk assigns a number to each data field found wrt given separator (given with -F option) and you can use these variables inside your script '{...}':

- $0 is whole line
- ...
- $n is n-th field of each line

Don't forget that you can reassign this variables whenever you want.

*example*

```
$ cat example.txt
This is
a test

$ awk '{print $1}' example.txt
This
a

```