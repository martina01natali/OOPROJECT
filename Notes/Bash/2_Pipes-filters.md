# 2 - Pipes and filters

Created: March 10, 2022 10:34 AM
Status: Completed

# References

[]()

[]()

## Pipes and Filters

Note: "|" is called pipe

wc	counts lines, words and characters
-l	# lines per file
-m 	# characters
-w 	# words

### Capturing output from commands

Since wc gives you an actual output, you can make it write its output on an external file

wc file.file > writehere.txt

`cat` sends content of a file to the screen: if more than a file is provided, it concatenates the output of all the files

`cut` cut out certain sections of a file that is formatted in a table-like style; predefined format is tab-delimited file. Important: both delimiter and field to cut must be specified and separated by a comma, e.g. cut -d, -f 2 file.txt cuts out and prints the 2nd column of a comma delimited (-d) file, file.txt

-d 	we have a .csv, comma-delimited file
-f 	= cut out and print the fields separated as previously specified
number1,number2,...		index of the fields to cut out

`less` prints only a screenful of the file: go forward with spacebar, backward with b and exit with 

`sort` sort lines of a file by alphabetical (predefined) order

-n 	sort by numerical order
-r  reverse order

`head` show first line
-n	number		gives the number-th line of the file

`tail`

-f	show file permanently and show changes made to the file in real time (useful for logs or files opened and worked on by many users)

`echo something`	prints the text that follows, i.e. "something"

>	file	add text to a file
>>	file	append text to a file
$filename	restitutes the value of the file

`uniq`	filters out adjacent matching lines in a file: if you want to remove equal elements, you should sort the file beforehand

-c  counts times a line occurs in the input

awk		[https://www.geeksforgeeks.org/awk-command-unixlinux-examples/](https://www.geeksforgeeks.org/awk-command-unixlinux-examples/)

sed		[https://www.geeksforgeeks.org/sed-command-in-linux-unix-with-examples/](https://www.geeksforgeeks.org/sed-command-in-linux-unix-with-examples/)

tr      [https://www.geeksforgeeks.org/tr-command-in-unix-linux-with-examples/](https://www.geeksforgeeks.org/tr-command-in-unix-linux-with-examples/)

## Passing Output to another command (piping)

To combine more than one command together, use a pipe | between two commands: this tells the shell to use the output of the command on the left as the input to the command on the right
history | grep cd	(this looks for all the "cd" that it can find in the list of commands given, that is given by history)

## Tools designed to work together

This idea of linking programs together is why Unix has been so successful. Instead of creating enormous programs that try to do many different things, Unix programmers focus on creating lots of simple tools that each do one job well, and that work well with each other. This programming model is called ‘pipes and filters’. We’ve already seen pipes; a filter is a program like wc or sort that transforms a stream of input into a stream of output. Almost all of the standard Unix tools can work this way: unless told to do otherwise, they read from standard input, do something with what they’ve read, and write to standard output.

The key is that any program that reads lines of text from standard input and writes lines of text to standard output can be combined with every other program that behaves this way as well. You **can** and **should** write your programs this way so that you and other people can put those programs into pipes to multiply their power.