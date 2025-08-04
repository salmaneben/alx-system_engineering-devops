# 0x02. Shell I/O Redirections and Filters

![Shell](https://img.shields.io/badge/Shell-Bash-green)
![I/O](https://img.shields.io/badge/I%2FO-Redirection-blue)
![Filters](https://img.shields.io/badge/Text-Processing-orange)

## 📋 Description

This project explores input/output redirection and text processing in the shell. You'll learn how to manipulate data streams, use filters to process text, and combine commands using pipes to create powerful data processing pipelines.

## 🎯 Learning Objectives

By the end of this project, you should be able to explain:

- What are shell redirections
- How to redirect standard output to a file
- How to get standard input from a file instead of the keyboard
- How to send the output from one program to the input of another program
- How to combine commands and filters with redirections
- What are special characters and how to use them
- How to display lines of a file
- How to duplicate the last line of a file
- How to find lines containing specific patterns

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-hello_world` | Script that prints "Hello, World", followed by a new line to the standard output |
| `1-confused_smiley` | Script that displays a confused smiley `"(Ôo)'` |
| `2-hellofile` | Script that displays the content of the `/etc/passwd` file |
| `3-twofiles` | Script that displays the content of `/etc/passwd` and `/etc/hosts` |
| `4-lastlines` | Script that displays the last 10 lines of `/etc/passwd` |
| `5-firstlines` | Script that displays the first 10 lines of `/etc/passwd` |
| `6-third_line` | Script that displays the third line of the file `iacta` |
| `7-file` | Script that creates a file with a very special name containing special characters |
| `8-cwd_state` | Script that writes the result of `ls -la` into the file `ls_cwd_content` |
| `9-duplicate_last_line` | Script that duplicates the last line of the file `iacta` |
| `10-no_more_js` | Script that deletes all the regular files with a `.js` extension in current and subfolders |
| `11-directories` | Script that counts the number of directories and sub-directories in the current directory |
| `12-newest_files` | Script that displays the 10 newest files in the current directory |
| `13-unique` | Script that takes a list of words as input and prints only words that appear exactly once |
| `14-findthatword` | Script that displays lines containing the pattern "root" from the file `/etc/passwd` |
| `15-countthatword` | Script that displays the number of lines that contain the pattern "bin" in the file `/etc/passwd` |
| `16-whatsnext` | Script that displays lines containing "root" and the 3 lines after them in `/etc/passwd` |
| `17-hidethisword` | Script that displays all lines in `/etc/passwd` that do not contain the pattern "bin" |
| `18-letteronly` | Script that displays all lines of `/etc/ssh/sshd_config` starting with a letter |
| `19-AZ` | Script that replaces all characters A and c from input to Z and e respectively |
| `20-hiago` | Script that removes all letters c and C from input |
| `21-reverse` | Script that reverses its input |
| `22-users_and_homes` | Script that displays all users and their home directories, sorted by users |
| `100-empty_casks` | Script that finds all empty files and directories in current directory and all sub-directories |
| `101-gifs` | Script that lists all files with a `.gif` extension in current and sub-directories |
| `102-acrostic` | Script that decodes acrostics that use the first letter of each line |
| `103-the_biggest_fan` | Script that parses web server logs in TSV format and displays the 11 hosts or IP addresses which did the most requests |

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
# Display file content
./2-hellofile

# Get last 10 lines
./4-lastlines

# Count directories
./11-directories

# Find pattern in file
./14-findthatword
```

## 🔄 I/O Redirection Concepts

### Standard Streams
- **stdin (0)**: Standard input (usually keyboard)
- **stdout (1)**: Standard output (usually terminal)
- **stderr (2)**: Standard error (usually terminal)

### Redirection Operators
```bash
>    # Redirect stdout to file (overwrite)
>>   # Redirect stdout to file (append)
<    # Redirect stdin from file
2>   # Redirect stderr to file
&>   # Redirect both stdout and stderr
|    # Pipe stdout to another command
```

### Examples
```bash
ls > file.txt           # Save ls output to file
cat < input.txt         # Read from input.txt
echo "text" >> file.txt # Append to file
ls 2> errors.txt        # Save errors to file
command1 | command2     # Pipe output to command2
```

## 🔍 Text Processing Filters

### Common Filters
```bash
cat     # Display file contents
head    # Show first lines
tail    # Show last lines
grep    # Search for patterns
sort    # Sort lines
uniq    # Remove duplicates
cut     # Extract columns
tr      # Translate characters
wc      # Count lines, words, characters
```

### Advanced Text Processing
```bash
grep "pattern" file      # Find lines with pattern
grep -v "pattern" file   # Find lines without pattern
sort file | uniq         # Sort and remove duplicates
cut -d: -f1 /etc/passwd  # Extract first field
tr 'a-z' 'A-Z'          # Convert to uppercase
```

## 📊 Special Characters

| Character | Description |
|-----------|-------------|
| `*` | Wildcard (matches any characters) |
| `?` | Single character wildcard |
| `[]` | Character class |
| `|` | Pipe (connect commands) |
| `;` | Command separator |
| `&` | Background process |
| `$` | Variable prefix |
| `"` | Weak quotes |
| `'` | Strong quotes |
| `\` | Escape character |

## ✅ Requirements

- All scripts tested on Ubuntu 20.04 LTS
- All scripts should be exactly two lines long
- All files must end with a new line
- The first line of all files should be exactly `#!/bin/bash`
- All files must be executable
- No use of backticks, `&&`, `||` or `;`

## 🎓 Resources

- [Shell, I/O Redirection](http://linuxcommand.org/lc3_lts0070.php)
- [Special Characters](http://mywiki.wooledge.org/BashGuide/SpecialCharacters)
- [Pipelines](https://www.gnu.org/software/bash/manual/html_node/Pipelines.html)
- [Redirections](https://www.gnu.org/software/bash/manual/html_node/Redirections.html)
- [Text Processing Commands](https://www.tldp.org/LDP/abs/html/textproc.html)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
