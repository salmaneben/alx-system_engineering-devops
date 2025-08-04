# 0x13. Firewall

![Firewall](https://img.shields.io/badge/Firewall-Network%20Security-red)
![UFW](https://img.shields.io/badge/UFW-Ubuntu%20Firewall-blue)
![Security](https://img.shields.io/badge/Security-Access%20Control-green)

## 📋 Description

This project focuses on network security through firewall configuration using UFW (Uncomplicated Firewall). You'll learn to secure servers by controlling incoming and outgoing network traffic, implementing port-based access control, and configuring advanced firewall rules including port forwarding and traffic redirection.

## 🎯 Learning Objectives

By the end of this project, you should be able to:

- Understand the role of firewalls in network security
- Configure UFW (Uncomplicated Firewall) on Ubuntu systems
- Implement security best practices for server protection
- Block and allow specific ports and protocols
- Configure port forwarding and traffic redirection
- Monitor and troubleshoot firewall rules
- Implement defense-in-depth security strategies
- Understand the difference between network and host-based firewalls

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-block_all_incoming_traffic_but` | Script that configures UFW to block all incoming traffic except essential ports |
| `100-port_forwarding` | UFW configuration file that redirects port 8080/TCP to port 80/TCP |

## 🔥 Firewall Fundamentals

### What is a Firewall?
A firewall is a network security system that monitors and controls incoming and outgoing network traffic based on predetermined security rules. It acts as a barrier between trusted internal networks and untrusted external networks.

### Types of Firewalls
- **Packet Filtering**: Examines packets at network layer
- **Stateful Inspection**: Tracks connection states
- **Application Layer**: Deep packet inspection
- **Next-Generation**: Advanced threat detection

### UFW (Uncomplicated Firewall)
UFW is a user-friendly front-end for managing iptables firewall rules on Ubuntu and Debian systems.

## 🛡️ Basic UFW Configuration

### Installation and Setup
```bash
# Install UFW (usually pre-installed on Ubuntu)
sudo apt update
sudo apt install ufw

# Check UFW status
sudo ufw status

# Enable UFW
sudo ufw enable

# Disable UFW
sudo ufw disable

# Reset UFW to defaults
sudo ufw --force reset
```

### Essential Firewall Rules
```bash
#!/usr/bin/env bash
# 0-block_all_incoming_traffic_but
# Configure firewall to block all incoming traffic except essential ports

# Reset UFW to default state
sudo ufw --force reset

# Set default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (port 22) - CRITICAL: Do this first to avoid lockout
sudo ufw allow 22/tcp

# Allow HTTP (port 80)
sudo ufw allow 80/tcp

# Allow HTTPS (port 443)
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw --force enable

# Display status
sudo ufw status verbose
```

### Default Policies
```bash
# Set default policies
sudo ufw default deny incoming    # Block all incoming traffic
sudo ufw default allow outgoing   # Allow all outgoing traffic
sudo ufw default deny forward     # Block forwarding
```

## 🔧 Advanced UFW Configuration

### Port-Specific Rules
```bash
# Allow specific ports
sudo ufw allow 22        # SSH
sudo ufw allow 80        # HTTP
sudo ufw allow 443       # HTTPS
sudo ufw allow 25        # SMTP
sudo ufw allow 53        # DNS
sudo ufw allow 110       # POP3
sudo ufw allow 143       # IMAP
sudo ufw allow 993       # IMAPS
sudo ufw allow 995       # POP3S

# Allow port ranges
sudo ufw allow 6000:6007/tcp
sudo ufw allow 6000:6007/udp

# Allow specific protocols
sudo ufw allow 53/udp    # DNS over UDP
sudo ufw allow 123/udp   # NTP
```

### IP-Based Rules
```bash
# Allow from specific IP
sudo ufw allow from 192.168.1.100

# Allow from IP range (subnet)
sudo ufw allow from 192.168.1.0/24

# Allow from specific IP to specific port
sudo ufw allow from 192.168.1.100 to any port 22

# Block specific IP
sudo ufw deny from 203.0.113.100

# Allow from specific IP on specific interface
sudo ufw allow in on eth0 from 192.168.1.100
```

### Application Profiles
```bash
# List available application profiles
sudo ufw app list

# Allow application profile
sudo ufw allow 'Nginx Full'
sudo ufw allow 'OpenSSH'
sudo ufw allow 'Apache'
sudo ufw allow 'Apache Secure'

# View application profile details
sudo ufw app info 'Nginx Full'
```

### Interface-Specific Rules
```bash
# Allow on specific interface
sudo ufw allow in on eth0 to any port 80
sudo ufw allow out on eth1

# Deny on specific interface
sudo ufw deny in on eth0 from 192.168.1.100
```

## 🔄 Port Forwarding Configuration

### UFW Port Forwarding Setup
```bash
# /etc/ufw/before.rules
# Add these lines to the *nat table section

*nat
:PREROUTING ACCEPT [0:0]

# Redirect port 8080 to port 80
-A PREROUTING -p tcp --dport 8080 -j REDIRECT --to-port 80

COMMIT
```

### Complete Port Forwarding Configuration
```bash
# Enable IP forwarding in kernel
echo 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Edit UFW configuration
sudo nano /etc/default/ufw
# Change: DEFAULT_FORWARD_POLICY="DROP" to DEFAULT_FORWARD_POLICY="ACCEPT"

# Configure NAT rules in /etc/ufw/before.rules
sudo nano /etc/ufw/before.rules
```

### Advanced Port Forwarding Examples
```bash
# Forward external port 8080 to internal port 80
*nat
:PREROUTING ACCEPT [0:0]
-A PREROUTING -p tcp --dport 8080 -j REDIRECT --to-port 80

# Forward to different host
-A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 192.168.1.100:80

# Forward with source IP restriction
-A PREROUTING -s 192.168.1.0/24 -p tcp --dport 8080 -j REDIRECT --to-port 80
COMMIT
```

## 📊 Monitoring and Management

### Checking Firewall Status
```bash
# Basic status
sudo ufw status

# Verbose status with rule numbers
sudo ufw status verbose

# Numbered status for rule management
sudo ufw status numbered
```

### Rule Management
```bash
# Delete rule by number
sudo ufw delete 3

# Delete rule by specification
sudo ufw delete allow 80/tcp

# Insert rule at specific position
sudo ufw insert 1 allow from 192.168.1.100

# Replace rule
sudo ufw delete 2
sudo ufw insert 2 allow from 192.168.1.100 to any port 22
```

### Logging Configuration
```bash
# Enable logging
sudo ufw logging on

# Set logging level
sudo ufw logging low     # Low level logging
sudo ufw logging medium  # Medium level logging
sudo ufw logging high    # High level logging

# View firewall logs
sudo tail -f /var/log/ufw.log
sudo journalctl -u ufw -f
```

## 🔍 Troubleshooting and Debugging

### Common Issues and Solutions

#### SSH Lockout Prevention
```bash
# Always allow SSH before enabling firewall
sudo ufw allow 22/tcp
sudo ufw enable

# Create emergency access rule
sudo ufw insert 1 allow from YOUR_IP_ADDRESS to any port 22
```

#### Connection Testing
```bash
# Test port connectivity
telnet server_ip 80
nc -zv server_ip 80

# Test from specific source
nc -zv -s source_ip server_ip 80

# Check listening ports
sudo netstat -tlnp
sudo ss -tlnp
```

#### Rule Verification
```bash
# Check iptables rules (underlying)
sudo iptables -L -n -v
sudo iptables -t nat -L -n -v

# Test UFW rule parsing
sudo ufw --dry-run delete allow 80/tcp
```

### Performance Monitoring
```bash
# Monitor firewall performance
sudo iptables -L -n -v --line-numbers

# Check connection tracking
cat /proc/net/nf_conntrack | wc -l
cat /proc/sys/net/netfilter/nf_conntrack_max

# Monitor dropped packets
sudo ufw status verbose | grep -i "packets"
```

## 🛠️ Advanced Security Configurations

### Rate Limiting
```bash
# Limit SSH connection attempts
sudo ufw limit ssh

# Custom rate limiting (using raw iptables)
sudo iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
```

### Geographic Blocking
```bash
# Install geoip module
sudo apt install xtables-addons-common

# Block by country (example: block China)
sudo iptables -A INPUT -m geoip --src-cc CN -j DROP
```

### DDoS Protection
```bash
# Protect against SYN flood attacks
sudo iptables -A INPUT -p tcp --syn -m limit --limit 1/s --limit-burst 3 -j ACCEPT
sudo iptables -A INPUT -p tcp --syn -j DROP

# Limit concurrent connections
sudo iptables -A INPUT -p tcp --dport 80 -m connlimit --connlimit-above 20 -j DROP
```

### Application-Specific Rules
```bash
# Web server protection
sudo ufw allow 'Nginx Full'
sudo ufw limit ssh

# Database server protection
sudo ufw allow from 192.168.1.0/24 to any port 3306  # MySQL
sudo ufw allow from 192.168.1.0/24 to any port 5432  # PostgreSQL

# Email server protection
sudo ufw allow 25   # SMTP
sudo ufw allow 587  # SMTP submission
sudo ufw allow 993  # IMAPS
sudo ufw allow 995  # POP3S
```

## 📋 Security Best Practices

### Defense in Depth
1. **Network Firewall**: Perimeter protection
2. **Host Firewall**: Individual server protection
3. **Application Firewall**: Application-level filtering
4. **Intrusion Detection**: Monitor for threats

### Firewall Rules Best Practices
```bash
# 1. Start with restrictive defaults
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 2. Allow only necessary services
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https

# 3. Use specific IP ranges when possible
sudo ufw allow from 192.168.1.0/24 to any port 22

# 4. Regular rule review and cleanup
sudo ufw status numbered
sudo ufw delete [rule_number]

# 5. Enable logging for monitoring
sudo ufw logging medium
```

### Configuration Management
```bash
# Backup UFW configuration
sudo cp -r /etc/ufw /etc/ufw.backup

# Version control firewall rules
cd /etc/ufw
sudo git init
sudo git add .
sudo git commit -m "Initial firewall configuration"

# Document rule purposes
sudo ufw comment "Web server access" allow 80/tcp
```

## 🔒 Compliance and Auditing

### Security Compliance
```bash
# PCI DSS compliance example
sudo ufw default deny incoming
sudo ufw allow from trusted_network to any port 22
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw logging high
```

### Audit and Reporting
```bash
# Generate firewall report
sudo ufw status verbose > firewall_report.txt

# Check for security violations
grep "BLOCKED" /var/log/ufw.log
grep "DENIED" /var/log/ufw.log

# Automated security check script
#!/bin/bash
echo "=== Firewall Security Audit ==="
echo "UFW Status: $(sudo ufw status | head -1)"
echo "Default Policies:"
sudo ufw status verbose | grep "Default:"
echo "Active Rules:"
sudo ufw status numbered
echo "Recent Blocks:"
sudo tail -20 /var/log/ufw.log | grep BLOCK
```

## ✅ Requirements

- Ubuntu 16.04 LTS or later
- Root or sudo privileges
- Basic understanding of networking concepts
- Understanding of TCP/IP protocols
- Knowledge of common network ports

## 🎓 Resources

- [UFW Documentation](https://help.ubuntu.com/community/UFW)
- [iptables Tutorial](https://www.netfilter.org/documentation/HOWTO/iptables-HOWTO.html)
- [Network Security Best Practices](https://www.sans.org/white-papers/1988/)
- [Firewall Configuration Guide](https://ubuntu.com/server/docs/security-firewall)
- [Linux Security Hardening](https://www.cisecurity.org/cis-benchmarks/)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
