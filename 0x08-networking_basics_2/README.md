# 0x08. Networking Basics #2

![Networking](https://img.shields.io/badge/Advanced-Networking-blue)
![Configuration](https://img.shields.io/badge/Network-Configuration-green)
![Administration](https://img.shields.io/badge/System-Administration-orange)

## 📋 Description

This project builds upon networking fundamentals by focusing on practical network configuration, host management, and advanced networking concepts. You'll learn to configure localhost, manage host files, display network information, and work with ports and network interfaces.

## 🎯 Learning Objectives

By the end of this project, you should be able to explain:

- What is localhost/127.0.0.1
- What is 0.0.0.0
- What is `/etc/hosts` file and how to modify it
- How to display your machine's active network interfaces
- How to configure network interfaces
- What is netstat and how to use it
- What are port numbers and how they work
- How to listen on specific ports

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-change_your_home_IP` | Bash script that configures Ubuntu server to change localhost and facebook.com resolution |
| `1-show_attached_IPs` | Bash script that displays all active IPv4 IPs on the machine |
| `100-port_listening_on_localhost` | Bash script that listens on port 98 on localhost |

## 🚀 Usage

Make scripts executable and run them:

```bash
# Make executable
chmod +x script_name

# Configure IP resolution
sudo ./0-change_your_home_IP

# Show active IPs
./1-show_attached_IPs

# Listen on port 98
./100-port_listening_on_localhost
```

### Examples

```bash
# Change localhost resolution
sudo ./0-change_your_home_IP
# Changes localhost to resolve to 127.0.0.2
# Changes facebook.com to resolve to 8.8.8.8

# Display active IPs
./1-show_attached_IPs
# Output: List of all active IPv4 addresses

# Start listening on port 98
./100-port_listening_on_localhost &
# Starts listening on localhost:98
```

## 🌐 Network Configuration Concepts

### Localhost (127.0.0.1)
- **Purpose**: Loopback address for local testing
- **Range**: 127.0.0.0/8 (127.0.0.1 to 127.255.255.255)
- **Usage**: Testing network applications locally
- **Benefits**: No network hardware required, always available

### 0.0.0.0 Address
- **Server Context**: Bind to all available network interfaces
- **Client Context**: Default route (any address)
- **Usage Examples**:
  - Web server listening on 0.0.0.0:80 (all interfaces)
  - Default gateway 0.0.0.0 (route to anywhere)

### /etc/hosts File
- **Purpose**: Local DNS resolution before DNS queries
- **Format**: `IP_ADDRESS hostname [aliases]`
- **Examples**:
  ```
  127.0.0.1    localhost
  127.0.1.1    mycomputer
  192.168.1.10 server.local server
  ```
- **Use Cases**:
  - Block websites (redirect to localhost)
  - Local development environments
  - Network testing and debugging

## 🔍 Network Information Commands

### Display Network Interfaces
```bash
# Show all network interfaces
ifconfig                    # Traditional command
ip addr show               # Modern Linux command
ip a                       # Short form

# Show only active interfaces
ifconfig -a                # All interfaces
ip link show up           # Only UP interfaces
```

### Network Interface Information
```bash
# Interface details
ifconfig eth0              # Specific interface
ip addr show eth0         # Specific interface with ip

# Interface statistics
cat /proc/net/dev          # Network statistics
netstat -i                 # Interface statistics
```

### Active Network Connections
```bash
# Show all connections
netstat -tuln              # TCP/UDP listening ports
netstat -an                # All connections
ss -tuln                   # Modern replacement for netstat

# Show processes using ports
netstat -tulnp             # With process names
ss -tulnp                  # With process names
lsof -i                    # List open files (network)
```

## 🔌 Port Management

### Understanding Ports
- **Port Range**: 0-65535
- **Well-known**: 0-1023 (system services)
- **Registered**: 1024-49151 (user applications)
- **Dynamic**: 49152-65535 (temporary)

### Listening on Ports
```bash
# Using netcat (nc)
nc -l 98                   # Listen on port 98
nc -l -p 98               # Alternative syntax

# Using Python
python3 -m http.server 98  # HTTP server on port 98

# Using socat
socat TCP-LISTEN:98,fork /dev/null
```

### Port Testing
```bash
# Test if port is open
nc -zv localhost 98        # Test port 98
telnet localhost 98        # Interactive test
nmap localhost -p 98       # Port scan

# Check what's using a port
lsof -i :98               # Process using port 98
netstat -tulnp | grep :98 # Find process on port 98
```

## 🛠 Script Implementation Details

### Host Resolution Configuration
```bash
#!/usr/bin/env bash
# Configure localhost and facebook.com resolution

# Backup original hosts file
cp /etc/hosts ~/hosts.backup

# Update hosts file
echo "127.0.0.2    localhost" > /tmp/hosts.new
echo "8.8.8.8      facebook.com" >> /tmp/hosts.new

# Replace hosts file
cp /tmp/hosts.new /etc/hosts
```

### Display Active IPs
```bash
#!/usr/bin/env bash
# Display all active IPv4 IPs

# Method 1: Using ifconfig
ifconfig | grep "inet " | awk '{print $2}' | cut -d: -f2

# Method 2: Using ip command
ip addr show | grep "inet " | awk '{print $2}' | cut -d/ -f1

# Method 3: Using hostname
hostname -I
```

### Port Listening
```bash
#!/usr/bin/env bash
# Listen on port 98 on localhost

# Using netcat
nc -l localhost 98

# Alternative with socat
socat TCP-LISTEN:98,bind=127.0.0.1,reuseaddr,fork /dev/null
```

## 🔧 Network Troubleshooting

### Common Issues and Solutions

#### DNS Resolution Problems
```bash
# Check DNS configuration
cat /etc/resolv.conf

# Test DNS resolution
nslookup google.com
dig google.com

# Flush DNS cache (if applicable)
sudo systemd-resolve --flush-caches
```

#### Interface Configuration Issues
```bash
# Bring interface up/down
sudo ifconfig eth0 up
sudo ifconfig eth0 down

# Or using ip command
sudo ip link set eth0 up
sudo ip link set eth0 down

# Check interface status
ip link show eth0
```

#### Port Binding Issues
```bash
# Check if port is already in use
netstat -tulnp | grep :80
lsof -i :80

# Kill process using port
sudo kill -9 $(lsof -t -i:80)

# Find available ports
ss -tuln | grep -v LISTEN
```

## 📊 Network Monitoring

### Real-time Monitoring
```bash
# Monitor network traffic
iftop                      # Interface top
nethogs                    # Network hogs
vnstat                     # Network statistics

# Monitor connections
watch -n 1 'netstat -tuln' # Watch connections
watch -n 1 'ss -tuln'     # Modern alternative
```

### Network Performance
```bash
# Test network speed
speedtest-cli              # Internet speed test
iperf3 -s                 # Network performance server
iperf3 -c server_ip       # Network performance client

# Check latency
ping -c 10 8.8.8.8        # Ping test
mtr google.com            # Network route analysis
```

## 🔒 Security Considerations

### Host File Security
- Regular backup of `/etc/hosts`
- Monitor for unauthorized changes
- Use proper permissions (644)
- Validate entries for security

### Port Security
- Close unnecessary listening ports
- Use firewall rules to restrict access
- Monitor for unexpected port usage
- Regular port scans for security audits

## ✅ Requirements

- All scripts tested on Ubuntu 20.04 LTS
- All scripts should be exactly 3 lines long
- All files must end with a new line
- The first line of all files should be exactly `#!/usr/bin/env bash`
- The second line should be a comment explaining the script
- All files must be executable
- Scripts should not use `awk`

## 🎓 Resources

- [What is localhost](https://en.wikipedia.org/wiki/Localhost)
- [What is 0.0.0.0](https://en.wikipedia.org/wiki/0.0.0.0)
- [Netstat command](https://www.tutorialspoint.com/unix_commands/netstat.htm)
- [Hosts file](https://en.wikipedia.org/wiki/Hosts_%28file%29)
- [ifconfig command](https://www.tutorialspoint.com/unix_commands/ifconfig.htm)
- [IP command examples](https://www.cyberciti.biz/faq/linux-ip-command-examples-usage-syntax/)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
