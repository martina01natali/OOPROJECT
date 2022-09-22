# 5 - Shell scripts

Created: March 10, 2022 10:34 AM
Status: Completed

# References

[]()

[]()

## Shell scripts

A script can be created with nano or an external text editor/IDE. Scripts in Bash are .sh files.
To create a new script with nano, simply
`nano newscr.sh`

To run a script in bash, simply
`bash newscr.sh`

The script can contain **arguments** (just like a function), that can be passed by **writing them after the call to the bash command**.

Parameters in the script can be given with

- $number where number = 1,2,3,... and means "the n-th argument on the command line"
- $@ special character, means "all of the command-line arguments to the shell script". Tip: $@ represents an actual list of files/arguments, so you can put it in a loop by using `for file in $@`

To run it correctly,
bash [newscr.sh](http://newscr.sh/) namefile.type (if using $@ you can add as many namefiles as you want)

Note: if there are any spaces in the filename, we need to surround the pointer to your argument, "$n", with double quotes *inside* the script.

<aside>
💡 ***Pro tip: when building a complicated script, try to run one command at a time and in the end piping the portion of history you're interested in in a script. This will save you time, swears, mistakes and ultimately white hair.***

</aside>

example
`history | tail -n 5 > redo-history.sh`
will put the last 5 lines you prompted in the redo-history script.