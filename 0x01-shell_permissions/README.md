# 0x01. Shell Permissions

![Shell](https://img.shields.io/badge/Shell-Bash-green)
![Permissions](https://img.shields.io/badge/Permissions-Linux-blue)
![Security](https://img.shields.io/badge/Security-Access-red)

## 📋 Description

This project focuses on understanding and managing file permissions, ownership, and user identification in Unix-like systems. You'll learn how to control access to files and directories, manage user roles, and implement security through proper permission settings.

## 🎯 Learning Objectives

By the end of this project, you should be able to explain:

- What do the commands `chmod`, `sudo`, `su`, `chown`, `chgrp` do
- Linux file permissions representation (r, w, x for user, group, other)
- How to represent each of the three sets of permissions as a single digit
- How to change permissions, owner and group of a file
- Why can't a normal user `chown` a file
- How to run a command with root privileges
- How to change user ID or become another user

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-iam_betty` | Script that switches the current user to the user `betty` |
| `1-who_am_i` | Script that prints the effective username of the current user |
| `2-groups` | Script that prints all the groups the current user is part of |
| `3-new_owner` | Script that changes the owner of the file `hello` to the user `betty` |
| `4-empty` | Script that creates an empty file called `hello` |
| `5-execute` | Script that adds execute permission to the owner of the file `hello` |
| `6-multiple_permissions` | Script that adds execute permission to the owner and the group owner, and read permission to other users, to the file `hello` |
| `7-everybody` | Script that adds execution permission to the owner, the group owner and the other users, to the file `hello` |
| `8-James_Bond` | Script that sets the permission to the file `hello` as follows: Owner: no permission at all, Group: no permission at all, Other users: all the permissions |
| `9-John_Doe` | Script that sets the mode of the file `hello` to `-rwxr-x-wx` |
| `10-mirror_permissions` | Script that sets the mode of the file `hello` the same as `olleh`'s mode |
| `11-directories_permissions` | Script that adds execute permission to all subdirectories of the current directory for the owner, the group owner and all other users |
| `12-directory_permissions` | Script that creates a directory called `my_dir` with permissions 751 in the working directory |
| `13-change_group` | Script that changes the group owner to `school` for the file `hello` |
| `100-change_owner_and_group` | Script that changes the owner to `vincent` and the group owner to `staff` for all the files and directories in the working directory |
| `101-symbolic_link_permissions` | Script that changes the owner and the group owner of `_hello` to `vincent` and `staff` respectively |
| `102-if_only` | Script that changes the owner of the file `hello` to `betty` only if it is owned by the user `guillaume` |
| `103-Star_Wars` | Script that will play the StarWars IV episode in the terminal |

## 🚀 Usage

Make scripts executable and run them:

```bash
# Make executable
chmod +x script_name

# Run script
./script_name
```

### Examples

```bash
# Check current user
./1-who_am_i

# See user groups
./2-groups

# Change file owner
sudo ./3-new_owner

# Set specific permissions
./8-James_Bond
```

## 🔐 Permission System

### Permission Types
- **r (read)**: Permission to read the file (4)
- **w (write)**: Permission to modify the file (2)
- **x (execute)**: Permission to execute the file (1)

### Permission Classes
- **Owner (u)**: The user who owns the file
- **Group (g)**: The group that owns the file
- **Other (o)**: All other users

### Numeric Representation
Permissions are represented by three digits (e.g., 755):
- First digit: Owner permissions
- Second digit: Group permissions
- Third digit: Other permissions

```
7 = rwx = 4+2+1 (read, write, execute)
6 = rw- = 4+2   (read, write)
5 = r-x = 4+1   (read, execute)
4 = r-- = 4     (read only)
3 = -wx = 2+1   (write, execute)
2 = -w- = 2     (write only)
1 = --x = 1     (execute only)
0 = --- = 0     (no permissions)
```

### Common Permission Examples
- `755`: Owner can read/write/execute, others can read/execute
- `644`: Owner can read/write, others can read only
- `600`: Owner can read/write, no access for others
- `777`: Everyone can read/write/execute (dangerous!)

## 🛠 Key Commands

### User Management
```bash
su username          # Switch user
sudo command         # Run command as root
whoami              # Show current user
groups              # Show user groups
id                  # Show user and group IDs
```

### Permission Management
```bash
chmod 755 file      # Set numeric permissions
chmod u+x file      # Add execute permission for owner
chmod g-w file      # Remove write permission for group
chmod o=r file      # Set read-only for others
```

### Ownership Management
```bash
chown user file         # Change file owner
chown user:group file   # Change owner and group
chgrp group file        # Change group only
```

## ✅ Requirements

- All scripts tested on Ubuntu 20.04 LTS
- All scripts should be exactly two lines long
- All files must end with a new line
- The first line of all files should be exactly `#!/bin/bash`
- All files must be executable
- No use of backticks, `&&`, `||` or `;`

## 🎓 Resources

- [Permissions](http://linuxcommand.org/lc3_lts0090.php)
- [File permissions in Linux/Unix](https://www.guru99.com/file-permissions.html)
- [Linux File Permission Tutorial](https://www.tutorialspoint.com/unix/unix-file-permission.htm)
- [Understanding Linux File Permissions](https://www.linux.com/training-tutorials/understanding-linux-file-permissions/)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
