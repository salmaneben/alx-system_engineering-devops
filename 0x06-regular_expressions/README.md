# 0x06. Regular Expressions

![Regex](https://img.shields.io/badge/Regular-Expressions-red)
![Pattern](https://img.shields.io/badge/Pattern-Matching-blue)
![Ruby](https://img.shields.io/badge/Ruby-Oniguruma-orange)

## 📋 Description

This project focuses on regular expressions (regex) using Ruby's Oniguruma regex library. You'll learn to create patterns that match specific text, validate input, and extract information from strings using powerful pattern matching techniques.

## 🎯 Learning Objectives

By the end of this project, you should be able to explain:

- What regular expressions are and how they work
- The difference between different regex engines
- How to build regex patterns for various matching scenarios
- Character classes, quantifiers, and anchors
- Grouping and capturing in regex
- Common regex patterns for validation and extraction

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-simply_match_school.rb` | Ruby script that matches the word "School" |
| `1-repetition_token_0.rb` | Ruby script that matches patterns with specific repetitions |
| `2-repetition_token_1.rb` | Ruby script that matches patterns with optional characters |
| `3-repetition_token_2.rb` | Ruby script that matches patterns with one or more repetitions |
| `4-repetition_token_3.rb` | Ruby script that matches patterns with zero or more repetitions |
| `5-beginning_and_end.rb` | Ruby script that matches strings starting with 'h' and ending with 'n' |
| `6-phone_number.rb` | Ruby script that matches 10-digit phone numbers |
| `7-OMG_WHY_ARE_YOU_SHOUTING.rb` | Ruby script that matches only capital letters |
| `100-textme.rb` | Ruby script that extracts sender, receiver, and flags from TextMe app logs |

## 🚀 Usage

Run Ruby scripts with regex patterns:

```bash
# Basic pattern matching
echo "School" | ruby 0-simply_match_school.rb

# Phone number validation
echo "4155049898" | ruby 6-phone_number.rb

# Extract capital letters
echo "HELLO WORLD" | ruby 7-OMG_WHY_ARE_YOU_SHOUTING.rb

# Parse log files
ruby 100-textme.rb textme.log
```

## 🔍 Regular Expression Basics

### Basic Metacharacters
```regex
.       # Matches any character except newline
^       # Start of string
$       # End of string
*       # Zero or more of preceding element
+       # One or more of preceding element
?       # Zero or one of preceding element
```

### Character Classes
```regex
[abc]       # Matches a, b, or c
[a-z]       # Matches any lowercase letter
[A-Z]       # Matches any uppercase letter
[0-9]       # Matches any digit
[^abc]      # Matches anything except a, b, or c
```

### Predefined Character Classes
```regex
\d      # Digit [0-9]
\D      # Non-digit [^0-9]
\w      # Word character [a-zA-Z0-9_]
\W      # Non-word character [^a-zA-Z0-9_]
\s      # Whitespace [ \t\n\r\f]
\S      # Non-whitespace [^ \t\n\r\f]
```

### Quantifiers
```regex
{n}     # Exactly n times
{n,}    # n or more times
{n,m}   # Between n and m times
*       # Zero or more times {0,}
+       # One or more times {1,}
?       # Zero or one time {0,1}
```

## 🔧 Common Patterns

### Phone Numbers
```regex
\d{10}              # 10 digits
\d{3}-\d{3}-\d{4}   # XXX-XXX-XXXX format
\(\d{3}\) \d{3}-\d{4}  # (XXX) XXX-XXXX format
```

### Email Addresses
```regex
\w+@\w+\.\w+                    # Basic email
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}  # More comprehensive
```

### Text Validation
```regex
^[A-Z]+$            # Only uppercase letters
^[a-z]+$            # Only lowercase letters
^[A-Za-z\s]+$       # Letters and spaces only
^\d+$               # Numbers only
```

## 🎯 Ruby Regex Syntax

### Basic Matching
```ruby
# Using =~ operator
puts "School" =~ /School/

# Using match method
result = "School".match(/School/)
puts result[0] if result

# Using scan method
text = "School is great"
matches = text.scan(/\w+/)
puts matches
```

### Substitution
```ruby
# Replace with gsub
text = "Hello World"
new_text = text.gsub(/World/, "Ruby")
puts new_text  # "Hello Ruby"
```

### Capture Groups
```ruby
# Extract parts with parentheses
phone = "123-456-7890"
match = phone.match(/(\d{3})-(\d{3})-(\d{4})/)
puts match[1]  # "123"
puts match[2]  # "456"
puts match[3]  # "7890"
```

## 📊 TextMe Log Format

For the advanced task, TextMe logs have this format:
```
[SENDER],[RECEIVER],[FLAGS]
```

Example log entries:
```
+14155552345,+14155552346,0
+14155552347,+14155552348,1
```

Extraction pattern:
```ruby
/\[from:(\+?\d{10,15})\] \[to:(\+?\d{10,15})\] \[flags:([^\]]*)\]/
```

## 🔄 Regex Engines

### Different Engines
- **PCRE** (Perl Compatible): Used in PHP, Apache
- **POSIX**: Standard Unix regex
- **Oniguruma**: Used in Ruby
- **RE2**: Used in Google products
- **JavaScript**: ECMAScript regex

### Ruby's Oniguruma Features
- Unicode support
- Named captures
- Atomic grouping
- Possessive quantifiers
- Lookbehind assertions

## 🧪 Testing Regex

### Online Tools
- Regex101.com
- RegExr.com
- RegexPal.com

### Ruby Testing
```ruby
# Test in irb
irb
> "test string".match(/pattern/)
> "test string" =~ /pattern/
> "test string".scan(/pattern/)
```

## 📈 Regex Best Practices

### Performance Tips
- Use specific patterns over general ones
- Avoid excessive backtracking
- Use non-capturing groups when you don't need the match
- Anchor patterns when possible

### Readability
- Use comments in complex patterns
- Break complex patterns into parts
- Test patterns thoroughly
- Document expected input format

## ✅ Requirements

- All scripts tested on Ubuntu 20.04 LTS
- Ruby scripts must use the Oniguruma regex library
- All files must end with a new line
- All files must be executable
- First line of Ruby files should be `#!/usr/bin/env ruby`
- All regex must work with the provided test strings

## 🎓 Resources

- [Regular Expressions Info](https://www.regular-expressions.info/)
- [Ruby Regex Documentation](https://ruby-doc.org/core/Regexp.html)
- [Oniguruma Documentation](https://github.com/kkos/oniguruma)
- [Regex Tutorial](https://regexone.com/)
- [Regex Cheat Sheet](https://www.rexegg.com/regex-quickstart.html)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
