# ssh and course notes

Created: March 10, 2022 10:45 AM
Status: To review

OOP 05/10/2021

Access the remote machine
ssh [magister01@axpfe2.fe.infn.it](mailto:magister01@axpfe2.fe.infn.it)
Username: magister01
Pssw: **** (see magister01 key in KeePass)

Directory prove: cartella condivisa su ssh
cd /home/oop_shared/

List all files with ls
Change to folder prove
To read file:
file nomefile (tells type of file)
cat nomefile (reads what's in the file)
wc nomefile (counts words/characters/lines) (???)
less nomefile (open vim and exit with q)

Copiare una directory intera da locale a ssh:
open two bash
one in ssh
one local --> cd to directory that you want to copy
scp gets you from local to remote
scp -r	(esegui ricorsivamente (-r) la copia dei file)

To copy directory shell-lesson-data in [magister01@axpfe2.fe.infn.it](mailto:magister01@axpfe2.fe.infn.it)
scp -r shell-lesson-data/ [magister01@axpfe2.fe.infn.it](mailto:magister01@axpfe2.fe.infn.it):

Compress/decompress file
tar
man tar	(open manual of command tar)

## ssh management

### Permessi Linux

When listing files, the first column gives you the permissions you have:
ex. -rwxr--r--

- `can be - if file or d if directory`

rw-		(tripletta of user) user can read and write
rwx		user can read and write and execute
r--		(tripletta of group) group of users can just read
r--		(tripletta of everyone else) others out of group can just read

Users/groups
When listing files, user, group are listed along with the files. The column# is an indication of what is in the directory (it is default 1 forfiles).

permissions	#	owner	owner's group	size	date	nameFile

### secure copy: from and to remote server

The fundamental command you need is `scp`, with its options. Basic sintax to:

- copy a file from local to remote: scp /file/to/send scp username@remote:/where/to/put
- copy a file from remote to local: scp username@remote:/file/to/send /where/to/put [WARNING: you must run this command while being on your local to make it work properly]

Options

- P Specifies the remote host ssh port.
- p Preserves files modification and access times.
- q Use this option if you want to suppress the progress meter and nonerror messages.
- C This option forces scp to compresses the data as it is sent to thedestination machine.
- r This option tells scp to copy directories recursively.