# 1 - Files and dirs

Created: March 10, 2022 10:34 AM
Status: Completed

# References

[]()

[]()

# Navigating Files and Directories

`pwd` = print working directory
`cd` = change directory
`cd -`= "the previous directory I was in"

Note: if you have spaces in names of directories/files, surround them with ""

`man`	= show "man" = manual of command "command"; you can navigate the manual using arrows down and up, spacebar to skip up and down by a full page; you can search inside the manual by using / followed by what you're looking for: move between results with N (forward) or Shift+N (backwards)

`ls` = list (files)

**Options** (also called switches or flags)
You can also combine different options by simply adding letters together one after another (ex. -F -a = -Fa)
--help
-a 	show all
-F 	list details
/       tells you that is directory
@     tells you that is link
*       tells you that is executable
-s	display size
-S	sort by size
-h 	size in human readable form
-t	order by last time of change
-r	list in reverse order
-R	do it recursively

**Arguments**
Can be passed to an option and tell the option what to operate on

ls	-F	namedir

ll		alias ll='ls -alF' list all objects even hidden with details

The root directory is expressed as "/".

---

# Working with files and directories

touch       create file
mkdir	create directory
-p 		create directory with subdirectories in one command
mv		move something somewhere

something	somewhere

-i	or --interactive, means requires confirmation before overwriting

cp		copy something somewhere: something can also be a list of file names

-r 	recursively copy all files inside your working dir

rm		remove something

-i 	requires confirmation

-r 	removes all files recursively and so the whole directory

---

# The text editor: nano

Create a new file to write with nano:

`nano draft.txt`

Note: you can also use notepad the same as nano.

Write you file. Then, to save it use Ctrl+O.