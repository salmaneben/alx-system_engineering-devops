# 0x03. Shell Variables and Expansions

![Shell](https://img.shields.io/badge/Shell-Bash-green)
![Variables](https://img.shields.io/badge/Variables-Environment-blue)
![Expansion](https://img.shields.io/badge/Expansion-Parameter-orange)

## 📋 Description

This project covers shell variables, environment variables, expansions, and arithmetic operations in Bash. You'll learn how to create, manipulate, and use variables effectively, understand the difference between local and global variables, and master various expansion techniques.

## 🎯 Learning Objectives

By the end of this project, you should be able to explain:

- What happens when you type `$ ls -l *.txt`
- What are the `/etc/profile` file and the `/etc/environment` file
- What is the difference between a local and a global variable
- What is a reserved variable
- How to create, update and delete shell variables
- What are the roles of special parameters
- What is expansion and how to use it
- What is the difference between single and double quotes
- How to do command substitution with `$()` and backticks

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-alias` | Script that creates an alias with name `ls` and value `rm *` |
| `1-hello_you` | Script that prints `hello user`, where user is the current Linux user |
| `2-path` | Script that adds `/action` to the `PATH` |
| `3-paths` | Script that counts the number of directories in the `PATH` |
| `4-global_variables` | Script that lists environment variables |
| `5-local_variables` | Script that lists all local variables and environment variables, and functions |
| `6-create_local_variable` | Script that creates a new local variable with name `BEST` and value `School` |
| `7-create_global_variable` | Script that creates a new global variable with name `BEST` and value `School` |
| `8-true_knowledge` | Script that prints the result of the addition of 128 with the value stored in `TRUEKNOWLEDGE` |
| `9-divide_and_rule` | Script that prints the result of `POWER` divided by `DIVIDE` |
| `10-love_exponent_breath` | Script that displays the result of `BREATH` to the power `LOVE` |
| `11-binary_to_decimal` | Script that converts a number from base 2 to base 10 |
| `12-combinations` | Script that prints all possible combinations of two letters, except `oo` |
| `13-print_float` | Script that prints a number with two decimal places |
| `100-decimal_to_hexadecimal` | Script that converts a number from base 10 to base 16 |
| `101-rot13` | Script that encodes and decodes text using the rot13 encryption |
| `102-odd` | Script that prints every other line from the input, starting with the first line |
| `103-water_and_stir` | Script that adds the two numbers stored in environment variables and prints the result |

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
# Create alias
./0-alias

# Show current user
./1-hello_you

# List environment variables
./4-global_variables

# Perform arithmetic
TRUEKNOWLEDGE=89 ./8-true_knowledge
```

## 🔧 Variable Types

### Local Variables
- Exist only in current shell session
- Not inherited by child processes
- Created with simple assignment: `VAR=value`

### Environment Variables
- Available to all child processes
- Created with `export`: `export VAR=value`
- Examples: `PATH`, `HOME`, `USER`, `PWD`

### Special Variables
- `$0` - Script name
- `$1, $2, ...` - Positional parameters
- `$#` - Number of parameters
- `$@` - All parameters
- `$?` - Exit status of last command
- `$$` - Process ID
- `$!` - Process ID of last background command

## 🔄 Expansions

### Parameter Expansion
```bash
${VAR}              # Basic expansion
${VAR:-default}     # Use default if VAR is unset
${VAR:=default}     # Assign default if VAR is unset
${VAR:+alternate}   # Use alternate if VAR is set
${VAR:?error}       # Error if VAR is unset
```

### Command Substitution
```bash
$(command)          # Modern syntax
`command`           # Legacy syntax (backticks)
```

### Arithmetic Expansion
```bash
$((expression))     # Arithmetic evaluation
$(( 5 + 3 ))       # Results in 8
$(( VAR * 2 ))     # Use variables in arithmetic
```

### Brace Expansion
```bash
{a,b,c}            # Expands to: a b c
{1..5}             # Expands to: 1 2 3 4 5
{a..z}             # Expands to: a b c ... z
```

## 🔢 Arithmetic Operations

### Basic Operators
```bash
+    # Addition
-    # Subtraction
*    # Multiplication
/    # Division
%    # Modulus
**   # Exponentiation
```

### Examples
```bash
result=$((5 + 3))          # Addition
result=$((10 / 2))         # Division
result=$((2 ** 3))         # Power (2^3 = 8)
result=$(($VAR1 + $VAR2))  # Variables
```

## 🔤 Base Conversion

### Number Base Systems
```bash
# Base 2 (Binary) to Base 10 (Decimal)
echo $((2#1010))           # 10 in decimal

# Base 10 to Base 16 (Hexadecimal)
printf "%x\n" 255          # ff in hexadecimal

# Base 16 to Base 10
echo $((16#ff))            # 255 in decimal
```

## 💬 Quoting

### Single Quotes
- Preserve literal value of all characters
- No variable expansion
- Example: `echo '$USER'` prints `$USER`

### Double Quotes
- Allow variable expansion
- Preserve spaces
- Example: `echo "$USER"` prints the username

### No Quotes
- Variable expansion occurs
- Word splitting on spaces
- Glob expansion occurs

## ✅ Requirements

- All scripts tested on Ubuntu 20.04 LTS
- All scripts should be exactly two lines long
- All files must end with a new line
- The first line of all files should be exactly `#!/bin/bash`
- All files must be executable
- No use of backticks, `&&`, `||` or `;`

## 🎓 Resources

- [Expansions](http://linuxcommand.org/lc3_lts0080.php)
- [Shell Variables](https://www.gnu.org/software/bash/manual/html_node/Shell-Variables.html)
- [Environment Variables](https://www.digitalocean.com/community/tutorials/how-to-read-and-set-environmental-and-shell-variables-on-a-linux-vps)
- [Shell Parameter Expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html)
- [Shell Arithmetic](https://www.gnu.org/software/bash/manual/html_node/Shell-Arithmetic.html)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
