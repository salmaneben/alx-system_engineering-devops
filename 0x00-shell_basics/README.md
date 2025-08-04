# 0x00. Shell Basics

![Shell](https://img.shields.io/badge/Shell-Bash-green)
![Linux](https://img.shields.io/badge/OS-Linux-blue)

## 📋 Description

This project introduces the fundamentals of shell navigation and basic commands in a Unix-like environment. It covers essential file operations, directory navigation, and basic shell utilities that form the foundation of system administration.

## 🎯 Learning Objectives

By the end of this project, you should be able to explain:

- What is a shell and how it works
- Basic navigation in the filesystem
- File and directory operations
- Understanding file types and permissions
- Using wildcards and special characters
- Creating symbolic links
- File manipulation and organization

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-current_working_directory` | Script that prints the absolute path name of the current working directory |
| `1-listit` | Script that displays the contents list of your current directory |
| `2-bring_me_home` | Script that changes the working directory to the user's home directory |
| `3-listfiles` | Script that displays current directory contents in a long format |
| `4-listmorefiles` | Script that displays current directory contents, including hidden files |
| `5-listfilesdigitonly` | Script that displays current directory contents with user and group IDs displayed numerically |
| `6-firstdirectory` | Script that creates a directory named `my_first_directory` in the `/tmp/` directory |
| `7-movethatfile` | Script that moves the file `betty` from `/tmp/` to `/tmp/my_first_directory` |
| `8-firstdelete` | Script that deletes the file `betty` in `/tmp/my_first_directory` |
| `9-firstdirdeletion` | Script that deletes the directory `my_first_directory` in `/tmp` |
| `10-back` | Script that changes the working directory to the previous one |
| `11-lists` | Script that lists all files in the current directory and parent directory and the `/boot` directory |
| `12-file_type` | Script that prints the type of the file named `iamafile` |
| `13-symbolic_link` | Script that creates a symbolic link to `/bin/ls`, named `__ls__` |
| `14-copy_html` | Script that copies all HTML files from current directory to parent directory |
| `100-lets_move` | Script that moves all files beginning with an uppercase letter to `/tmp/u/` |
| `101-clean_emacs` | Script that deletes all files in current directory that end with `~` |
| `102-tree` | Script that creates directories `welcome/`, `welcome/to/` and `welcome/to/school` |
| `103-commas` | Script that lists all files and directories separated by commas |
| `school.mgc` | Magic file that can be used with the command `file` to detect School data files |

## 🚀 Usage

To run any script, make sure it's executable and run it:

```bash
# Make the script executable
chmod +x script_name

# Run the script
./script_name
```

### Examples

```bash
# Display current working directory
./0-current_working_directory

# List directory contents
./1-listit

# Navigate to home directory
./2-bring_me_home

# List files in long format
./3-listfiles
```

## ✅ Requirements

- All scripts tested on Ubuntu 20.04 LTS
- All scripts should be exactly two lines long (`wc -l file` should print 2)
- All files must end with a new line
- The first line of all files should be exactly `#!/bin/bash`
- All files must be executable
- No use of backticks, `&&`, `||` or `;`
- All files must pass Shellcheck

## 🔍 Key Concepts

### Basic Navigation
- `pwd` - Print working directory
- `cd` - Change directory
- `ls` - List directory contents

### File Operations
- `cp` - Copy files
- `mv` - Move/rename files
- `rm` - Remove files
- `mkdir` - Make directories
- `rmdir` - Remove directories

### File Information
- `file` - Determine file type
- `ln` - Create links
- Wildcards: `*`, `?`, `[]`

### Advanced Features
- Hidden files (starting with `.`)
- Symbolic links
- File globbing and pattern matching

## 🎓 Resources

- [What Is "The Shell"?](http://linuxcommand.org/lc3_lts0010.php)
- [Navigation](http://linuxcommand.org/lc3_lts0020.php)
- [Looking Around](http://linuxcommand.org/lc3_lts0030.php)
- [A Guided Tour](http://linuxcommand.org/lc3_lts0040.php)
- [Manipulating Files](http://linuxcommand.org/lc3_lts0050.php)
- [Working With Commands](http://linuxcommand.org/lc3_lts0060.php)
- [Reading Man pages](http://linuxcommand.org/lc3_man_pages/man1.html)
- [Keyboard shortcuts for Bash](https://www.howtogeek.com/181/keyboard-shortcuts-for-bash-command-shell-for-ubuntu-debian-suse-redhat-linux-etc/)
- [LTS](https://wiki.ubuntu.com/LTS)
- [Shebang](https://en.wikipedia.org/wiki/Shebang_%28Unix%29)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
