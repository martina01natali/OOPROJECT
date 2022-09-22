# 0 - Introduction

Created: February 24, 2022 3:53 PM
Status: Completed

# References

[Shell novice tutorial](https://swcarpentry.github.io/shell-novice/)
[GreyCat's guide](http://mywiki.wooledge.org/BashGuide)

[How to Create Command Shortcuts with Aliases in Linux](https://www.tomshardware.com/how-to/create-command-shortcuts-with-linux-aliases)

[]()

[https://www.notion.so](https://www.notion.so)

[https://www.notion.so](https://www.notion.so)

[https://www.notion.so](https://www.notion.so)

[https://www.notion.so](https://www.notion.so)

# Unix shell tutorial

### Upgrading and updating ubuntu

Commands to update and upgrade:
`sudo apt update && sudo apt upgrade`

Commands to clean up the system of useless packages:
`sudo apt autoclean && sudo apt autoremove`

## Introducing the Shell

The Unix shell is both a command-line interface (CLI) and a scripting language.
The most popular Unix shell is Bash (the Bourne Again SHell — so-called because it’s derived from a shell written by Stephen Bourne). Bash is the default shell on most modern implementations of Unix and in most packages that provide Unix-like tools for Windows.

When the shell is first opened, you are presented with a prompt, indicating that the shell is waiting for input.

$

When you have to finish writing a command, the prompt will be

\>

Want to clear the terminal? `clear`

Use up and down arrows to move along the lines of the terminal or scroll with mouse

Want all the commands you gave? `history`

After this, to replicate a command, use (no need to repeat history) `! numberline`

Other history commands:

- Ctrl+R history search mode reverse-i-search that finds the most recent command in your history that matches the text you enter next; press again for earlier matches; use left and right arrow keys to choose that line, then you can edit it and then Enter to run the command
- !$ retrieves the *last word of the last command* (this is useful ;) )
You can also put pieces of history inside a script, by piping a section (i.e. head, tail commands) into a script
history | tail -n 1 > [lastcomm.sh](http://lastcomm.sh/)

To move along your command line, use
Ctrl+A = move to the start of the line
Ctrl+E = move to the end of the line

### Tab completion

Useful to complete the name of something (directory, file, etc.) when enough elements are already provided to identify univocally that object: use Tab, or, if it does nothing, press Tab twice to bring up a list of all the files.

### ASCII characters

You have to activate the "tastierino numerico" by

`Fn+Scorr (=Block num)`

Then if you have an ASCII character numbered XXX,

`Alt+XXX`

### Useful ASCII characters

`               is given by `Alt+96`: `command` restitutes the value of command (else you can use $(command) )
~		Alt+126

### Customary commands

[Guide on aliases](https://www.tomshardware.com/how-to/create-command-shortcuts-with-linux-aliases)

alias new_command='series of commands'