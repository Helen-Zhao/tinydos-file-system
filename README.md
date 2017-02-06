# tinydos-file-system

The tinydos "file system" is a program that simulates how real files systems work, using a text file as the hard drive. A "drive" of 128 blocks is created, where each block can either hold information or references to other blocks. A block can be assigned "directory" status or "file" status. A directory holds references (maximum of 6 entries) to other directories or files. The root directory is stored in block 0. Text can be appended to files once created. This program needs to be run on a Linux operating system.

#Commands
- format volumeName
 - Creates an ordinary file called volumeName and fills it in as a newly formatted TinyDOS volume. The real file will be 66944 bytes long. The volume is used for the next commands in the command file.
- reconnect volumeName
 - Reconnects the ordinary file called volumeName to be used as a TinyDOS volume for the next commands in the command file.
- ls fullDirectoryPathname
 - Lists the contents of the directory specified by fullDirectoryPathname. All pathnames of files and directories for TinyDOS will be fully qualified. You can make ls as pretty as you like, it must show the names, types and sizes of all files in the directory.
- mkfile fullFilePathname
 - Makes a file with the pathname fullFilePathname. Any directories in the path should already exist.
- mkdir fullDirectoryPathname
 - Makes a directory with the pathname fullDirectoryPathname. Any directories in the path should already exist.
- append fullFilePathname "data"
 - Writes all of the data between the double quotes to the end of the file called fullFilePathname. The file must already exist. Double quotes will not appear inside the data.
- print fullFilePathname
 - Prints all of the data from the file called fullFilePathname to the screen. The file must already exist.
- delfile fullFilePathname
 - Deletes the file called fullFilePathname. The file must already exist.
- deldir fullDirectoryPathname
 - Deletes the directory called fullDirectoryPathname. The directory must already exist and the directory must be empty.
- quit
 - The TinyDOS program quits.

Please note that Drive.py is not developed by me, but Robert Sheehan from the University of Auckland. 
