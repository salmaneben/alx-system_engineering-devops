# 0x05. Processes and Signals

![Process](https://img.shields.io/badge/Process-Management-green)
![Signals](https://img.shields.io/badge/Signal-Handling-blue)
![System](https://img.shields.io/badge/System-Administration-orange)

## 📋 Description

This project covers process management and signal handling in Unix-like systems. You'll learn how to create, monitor, and control processes, handle signals gracefully, and implement daemon-like behavior in your scripts.

## 🎯 Learning Objectives

By the end of this project, you should be able to explain:

- What is a PID
- What is a process
- How to find a process' PID
- How to kill a process
- What is a signal
- What are the 2 signals that cannot be ignored
- How to create infinite loops
- How to handle signals in scripts

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-what-is-my-pid` | Script that displays its own PID |
| `1-list_your_processes` | Script that displays a list of currently running processes |
| `2-show_your_bash_pid` | Script that displays lines containing the bash word |
| `3-show_your_bash_pid_made_easy` | Script that displays the PID and process name of processes containing "bash" |
| `4-to_infinity_and_beyond` | Script that displays "To infinity and beyond" indefinitely |
| `5-dont_stop_me_now` | Script that stops the 4-to_infinity_and_beyond process |
| `6-stop_me_if_you_can` | Script that stops the 4-to_infinity_and_beyond process without using kill or killall |
| `7-highlander` | Script that displays "To infinity and beyond" indefinitely with signal handling |
| `8-beheaded_process` | Script that kills the 7-highlander process |
| `100-process_and_pid_file` | Script that creates a PID file, displays messages, and handles signals |
| `101-manage_my_process` | Init script that manages the manage_my_process daemon |
| `102-zombie.c` | C program that creates 5 zombie processes |
| `manage_my_process` | Script that indefinitely writes to a file (daemon-like behavior) |

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
# Show current process ID
./0-what-is-my-pid

# List all processes
./1-list_your_processes

# Create infinite loop
./4-to_infinity_and_beyond &

# Stop process gracefully
./5-dont_stop_me_now

# Manage daemon process
sudo ./101-manage_my_process start
```

## 🔄 Process Management

### What is a Process?
A process is a running instance of a program with its own:
- Process ID (PID)
- Memory space
- File descriptors
- Environment variables
- Current working directory

### Process States
- **Running**: Currently executing
- **Sleeping**: Waiting for an event
- **Stopped**: Suspended
- **Zombie**: Completed but parent hasn't read exit status

### Process Hierarchy
- Every process has a parent (except init)
- Parent Process ID (PPID)
- Child processes inherit from parent

## 📊 Process Commands

### Viewing Processes
```bash
ps                      # Show current user's processes
ps aux                  # Show all processes with details
ps -ef                  # Show all processes in full format
pstree                  # Show process tree
top                     # Real-time process monitor
htop                    # Enhanced process monitor
```

### Process Information
```bash
echo $$                 # Current shell's PID
pgrep process_name      # Find PID by name
pidof process_name      # Find PID by name
ps -p PID               # Show specific process
cat /proc/PID/status    # Detailed process info
```

### Managing Processes
```bash
kill PID                # Terminate process
kill -9 PID            # Force kill process
killall process_name    # Kill all processes by name
pkill process_name      # Kill processes by name
jobs                    # Show background jobs
fg                      # Bring job to foreground
bg                      # Send job to background
nohup command &         # Run command immune to hangups
```

## 📡 Signal Handling

### Common Signals
| Signal | Number | Description | Can be caught? |
|--------|--------|-------------|----------------|
| SIGHUP | 1 | Hangup | Yes |
| SIGINT | 2 | Interrupt (Ctrl+C) | Yes |
| SIGQUIT | 3 | Quit (Ctrl+\) | Yes |
| SIGKILL | 9 | Kill | **No** |
| SIGTERM | 15 | Terminate | Yes |
| SIGSTOP | 19 | Stop | **No** |
| SIGCONT | 18 | Continue | Yes |

### Signal Commands
```bash
kill -l                 # List all signals
kill -TERM PID         # Send SIGTERM
kill -9 PID           # Send SIGKILL
kill -STOP PID        # Send SIGSTOP
kill -CONT PID        # Send SIGCONT
```

### Signal Handling in Scripts
```bash
#!/bin/bash
# Signal handler function
cleanup() {
    echo "Received signal, cleaning up..."
    exit 0
}

# Trap signals
trap cleanup SIGTERM SIGINT

# Main script
while true; do
    echo "Running..."
    sleep 1
done
```

## 🔧 Daemon Management

### Creating a Daemon
A daemon is a background process that:
- Runs continuously
- Has no controlling terminal
- Usually started at boot
- Managed by init system

### Init Script Structure
```bash
#!/bin/bash
case "$1" in
    start)
        # Start the daemon
        ;;
    stop)
        # Stop the daemon
        ;;
    restart)
        # Restart the daemon
        ;;
    status)
        # Check daemon status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
```

### PID File Management
- Store daemon PID in `/var/run/name.pid`
- Check PID file before starting
- Remove PID file when stopping
- Use PID file for status checks

## 👻 Zombie Processes

### What are Zombies?
- Processes that have completed execution
- Still have an entry in process table
- Parent hasn't read the exit status
- Show as `<defunct>` or `Z` in ps output

### Preventing Zombies
```c
#include <signal.h>
#include <sys/wait.h>

void sigchld_handler(int sig) {
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

int main() {
    signal(SIGCHLD, sigchld_handler);
    // ... rest of program
}
```

## 🔄 Background Processes

### Running in Background
```bash
command &               # Run in background
nohup command &         # Run immune to hangups
screen command          # Run in screen session
tmux new-session command # Run in tmux session
```

### Job Control
```bash
jobs                    # List background jobs
fg %1                   # Bring job 1 to foreground
bg %1                   # Send job 1 to background
disown %1              # Remove job from shell's job table
```

## ✅ Requirements

- All scripts tested on Ubuntu 20.04 LTS
- All files must end with a new line
- All Bash scripts must be executable
- First line should be `#!/usr/bin/env bash`
- Second line should be a comment explaining the script
- Must pass Shellcheck
- Cannot use `kill` command in scripts 5 and 6

## 🎓 Resources

- [Linux Process Management](https://www.tutorialspoint.com/unix/unix-processes.htm)
- [Signal Handling](https://www.gnu.org/software/libc/manual/html_node/Signal-Handling.html)
- [Process Control](https://tldp.org/LDP/abs/html/x9644.html)
- [Daemon Programming](https://www.netzmafia.de/skripten/unix/linux-daemon-howto.html)
- [Init Scripts](https://bash.cyberciti.biz/guide/Writing_your_first_shell_script)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*