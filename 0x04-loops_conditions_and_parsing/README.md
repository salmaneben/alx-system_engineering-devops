# 0x04. Loops, Conditions and Parsing

![Bash](https://img.shields.io/badge/Bash-Scripting-green)
![Loops](https://img.shields.io/badge/Control-Structures-blue)
![Logic](https://img.shields.io/badge/Programming-Logic-orange)

## 📋 Description

This project introduces advanced Bash scripting concepts including loops, conditional statements, and text parsing. You'll learn to create more sophisticated scripts that can make decisions, repeat actions, and process data dynamically.

## 🎯 Learning Objectives

By the end of this project, you should be able to explain:

- How to create SSH keys
- What is the advantage of using `#!/usr/bin/env bash` over `#!/bin/bash`
- How to use `while`, `until` and `for` loops
- How to use `if`, `else`, `elif` and `case` condition statements
- How to use the `cut` command
- What are files and other comparison operators, and how to use them

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-RSA_public_key.pub` | RSA public key for SSH authentication |
| `1-for_best_school` | Script that displays "Best School" 10 times using a for loop |
| `2-while_best_school` | Script that displays "Best School" 10 times using a while loop |
| `3-until_best_school` | Script that displays "Best School" 10 times using an until loop |
| `4-if_9_say_hi` | Script that displays "Best School" 10 times, but for the 9th iteration, displays "Hi" on a new line |
| `5-4_bad_luck_8_is_your_chance` | Script that loops from 1 to 10 and displays "bad luck" for 4th iteration, "good luck" for 8th iteration |
| `6-superstitious_numbers` | Script that displays numbers from 1 to 20 with special messages for certain numbers |
| `7-clock` | Script that displays the time for 12 hours and 59 minutes |
| `8-for_ls` | Script that displays the content of the current directory in a list format where only the part of the name after the first dash is displayed |
| `9-to_file_or_not_to_file` | Script that gives information about the school file |
| `10-fizzbuzz` | Script that displays numbers from 1 to 100 (Fizz-Buzz implementation) |
| `100-read_and_cut` | Script that displays the content of the file /etc/passwd with specific formatting |
| `101-tell_the_story_of_passwd` | Script that displays the content of the file /etc/passwd in a story format |
| `102-lets_parse_apache_logs` | Script that parses Apache log files and displays visitor IP and HTTP status code |
| `103-dig_the-data` | Script that groups visitors by IP and HTTP status code, and displays data in descending order |

## 🚀 Usage

First, make sure you have the RSA key for authentication:

```bash
# Generate SSH key if needed
ssh-keygen -t rsa -b 4096

# Make scripts executable
chmod +x script_name

# Run scripts
./script_name
```

### Examples

```bash
# Display using for loop
./1-for_best_school

# Display with conditions
./4-if_9_say_hi

# Classic FizzBuzz
./10-fizzbuzz

# Parse log files
./102-lets_parse_apache_logs < apache_access.log
```

## 🔄 Loop Structures

### For Loop
```bash
# C-style for loop
for ((i=1; i<=10; i++)); do
    echo $i
done

# List iteration
for item in list1 list2 list3; do
    echo $item
done

# Range iteration
for i in {1..10}; do
    echo $i
done
```

### While Loop
```bash
counter=1
while [ $counter -le 10 ]; do
    echo $counter
    ((counter++))
done
```

### Until Loop
```bash
counter=1
until [ $counter -gt 10 ]; do
    echo $counter
    ((counter++))
done
```

## 🔀 Conditional Statements

### If Statement
```bash
if [ condition ]; then
    # commands
elif [ condition2 ]; then
    # commands
else
    # commands
fi
```

### Case Statement
```bash
case $variable in
    pattern1)
        # commands
        ;;
    pattern2)
        # commands
        ;;
    *)
        # default commands
        ;;
esac
```

## 🔍 Comparison Operators

### Numeric Comparisons
```bash
-eq    # Equal to
-ne    # Not equal to
-lt    # Less than
-le    # Less than or equal to
-gt    # Greater than
-ge    # Greater than or equal to
```

### String Comparisons
```bash
=      # Equal to
!=     # Not equal to
-z     # Empty string
-n     # Non-empty string
```

### File Tests
```bash
-e     # File exists
-f     # Regular file
-d     # Directory
-r     # Readable
-w     # Writable
-x     # Executable
-s     # File has size > 0
```

## ✂️ Text Processing

### Cut Command
```bash
cut -d: -f1 /etc/passwd        # Extract first field (username)
cut -c1-5 file                 # Extract characters 1-5
cut -d' ' -f2,4 file          # Extract fields 2 and 4
```

### Other Useful Commands
```bash
awk '{print $1}'               # Print first field
sed 's/old/new/g'             # Replace text
grep "pattern" file            # Find pattern
sort file                      # Sort lines
uniq file                      # Remove duplicates
```

## 🎮 Classic Programming Problems

### FizzBuzz Implementation
The classic programming problem where you:
- Print numbers 1-100
- Replace multiples of 3 with "Fizz"
- Replace multiples of 5 with "Buzz"
- Replace multiples of both with "FizzBuzz"

### Log File Parsing
Common system administration task:
- Parse Apache/Nginx logs
- Extract IP addresses and status codes
- Group and count occurrences
- Sort by frequency

## 🔑 SSH Key Management

### Generating SSH Keys
```bash
# Generate RSA key pair
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Generate with specific filename
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_alx

# View public key
cat ~/.ssh/id_rsa.pub
```

### Using SSH Keys
- Public key goes on the server (authorized_keys)
- Private key stays on your local machine
- Enables passwordless authentication

## ✅ Requirements

- All scripts tested on Ubuntu 20.04 LTS
- All files must end with a new line
- All Bash scripts must be executable
- First line should be `#!/usr/bin/env bash`
- Second line should be a comment explaining the script
- No use of `awk`
- Must pass Shellcheck (version 0.3.7)

## 🎓 Resources

- [Loops](https://tldp.org/LDP/Bash-Beginners-Guide/html/sect_09_01.html)
- [Conditionals](https://tldp.org/LDP/Bash-Beginners-Guide/html/sect_07_01.html)
- [Parsing](https://tldp.org/LDP/abs/html/textproc.html)
- [SSH Key Generation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [Shellcheck](https://github.com/koalaman/shellcheck)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*