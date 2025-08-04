# 0x0B. SSH

![SSH](https://img.shields.io/badge/SSH-Secure%20Shell-blue)
![Security](https://img.shields.io/badge/Security-Authentication-green)
![Remote Access](https://img.shields.io/badge/Remote-Access-orange)

## 📋 Description

This project focuses on SSH (Secure Shell), a cryptographic network protocol for secure remote access and command execution. You'll learn to configure SSH clients and servers, manage SSH keys, implement security best practices, and automate remote server management using SSH.

## 🎯 Learning Objectives

By the end of this project, you should be able to:

- Understand what SSH is and how it works
- Create and manage SSH key pairs
- Connect to remote servers using SSH
- Configure SSH client and server settings
- Implement SSH security best practices
- Use SSH for file transfer and port forwarding
- Automate SSH connections and commands
- Troubleshoot SSH connection issues
- Configure SSH agent for key management
- Set up SSH tunneling and proxying

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-use_a_private_key` | Bash script that connects to a server using SSH with a private key |
| `1-create_ssh_key_pair` | Bash script that creates an RSA key pair for SSH authentication |
| `2-ssh_config` | SSH client configuration file with optimized settings |

## 🔑 SSH Fundamentals

### What is SSH?

SSH (Secure Shell) is a cryptographic network protocol that provides:
- **Secure remote access** to servers and devices
- **Encrypted communication** over insecure networks
- **Authentication mechanisms** using passwords or keys
- **Secure file transfer** capabilities
- **Port forwarding** and tunneling features

### SSH Protocol Features
- **Encryption**: All data is encrypted during transmission
- **Authentication**: Multiple authentication methods available
- **Integrity**: Data integrity verification
- **Compression**: Optional data compression
- **Port Forwarding**: Secure tunneling of network connections

## 🔧 SSH Key Management

### Creating SSH Key Pairs

#### Basic RSA Key Generation
```bash
#!/usr/bin/env bash
# 1-create_ssh_key_pair - Create an RSA key pair

# Generate RSA key pair with 4096-bit key size
ssh-keygen -t rsa -b 4096 -f ~/.ssh/school -N "betty"

echo "SSH key pair created:"
echo "Private key: ~/.ssh/school"
echo "Public key: ~/.ssh/school.pub"
```

#### Advanced Key Generation Options
```bash
# Generate different key types
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -C "user@example.com"
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -C "user@example.com"
ssh-keygen -t ecdsa -b 521 -f ~/.ssh/id_ecdsa -C "user@example.com"

# Generate key with custom settings
ssh-keygen -t rsa -b 4096 -f ~/.ssh/server_key -N "passphrase" -C "server access key"
```

### SSH Key Best Practices
```bash
# Set proper permissions for SSH keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 644 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/config

# Backup important keys
cp ~/.ssh/id_rsa ~/.ssh/id_rsa.backup
cp ~/.ssh/id_rsa.pub ~/.ssh/id_rsa.pub.backup
```

## 🌐 SSH Client Configuration

### Basic SSH Connection
```bash
#!/usr/bin/env bash
# 0-use_a_private_key - Connect using SSH with private key

# Connect to server using specific private key
ssh -i ~/.ssh/school ubuntu@server_ip

# Alternative with explicit options
ssh -i ~/.ssh/school -o PasswordAuthentication=no ubuntu@server_ip
```

### SSH Config File
```bash
# 2-ssh_config - SSH client configuration file
# Location: ~/.ssh/config

Host *
    # Security settings
    PasswordAuthentication no
    PubkeyAuthentication yes
    HostKeyAlgorithms ssh-ed25519,rsa-sha2-512,rsa-sha2-256
    KexAlgorithms curve25519-sha256,diffie-hellman-group16-sha512
    Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
    MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha2-256,hmac-sha2-512
    
    # Connection settings
    ServerAliveInterval 60
    ServerAliveCountMax 3
    ConnectTimeout 30
    
    # Performance settings
    Compression yes
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h:%p
    ControlPersist 10m

# Specific host configuration
Host school-server
    HostName 54.210.47.199
    User ubuntu
    IdentityFile ~/.ssh/school
    Port 22

Host production-server
    HostName prod.example.com
    User admin
    IdentityFile ~/.ssh/prod_key
    Port 2222
    LocalForward 3306 localhost:3306
```

### Advanced SSH Configuration
```bash
# ~/.ssh/config - Advanced configuration
Host jump-server
    HostName jump.example.com
    User jumpuser
    IdentityFile ~/.ssh/jump_key
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h:%p
    ControlPersist 10m

Host target-server
    HostName 192.168.1.100
    User targetuser
    IdentityFile ~/.ssh/target_key
    ProxyJump jump-server
    
Host dev-*
    User developer
    IdentityFile ~/.ssh/dev_key
    Port 2222
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null

Host *.internal
    ProxyCommand ssh -W %h:%p jump-server
    User internal-user
    IdentityFile ~/.ssh/internal_key
```

## 🔒 SSH Server Configuration

### Basic SSH Server Setup
```bash
# Install SSH server
sudo apt update
sudo apt install openssh-server

# Start and enable SSH service
sudo systemctl start ssh
sudo systemctl enable ssh

# Check SSH service status
sudo systemctl status ssh
```

### SSH Server Configuration
```bash
# /etc/ssh/sshd_config - Secure SSH server configuration

# Basic settings
Port 2222
Protocol 2
ListenAddress 0.0.0.0

# Authentication settings
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
ChallengeResponseAuthentication no
UsePAM yes

# Security settings
AllowUsers ubuntu developer admin
DenyUsers guest nobody
MaxAuthTries 3
MaxSessions 10
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2

# Disable dangerous features
PermitEmptyPasswords no
PermitUserEnvironment no
AllowTcpForwarding yes
AllowAgentForwarding yes
GatewayPorts no
X11Forwarding no

# Logging
SyslogFacility AUTH
LogLevel INFO

# Crypto settings
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha2-256,hmac-sha2-512
KexAlgorithms curve25519-sha256,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512
```

### Apply SSH Configuration
```bash
# Test SSH configuration
sudo sshd -t

# Restart SSH service
sudo systemctl restart ssh

# Monitor SSH logs
sudo tail -f /var/log/auth.log | grep ssh
```

## 🔐 SSH Key Authentication Setup

### Server-Side Key Setup
```bash
# Create .ssh directory
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add public key to authorized_keys
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Alternative: copy public key from client
ssh-copy-id -i ~/.ssh/school.pub ubuntu@server_ip
```

### Client-Side Key Management
```bash
# Add key to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
ssh-add ~/.ssh/school

# List loaded keys
ssh-add -l

# Remove all keys from agent
ssh-add -D

# Remove specific key
ssh-add -d ~/.ssh/school
```

### SSH Agent Configuration
```bash
# ~/.bashrc - Auto-start SSH agent
if ! pgrep -u "$USER" ssh-agent > /dev/null; then
    ssh-agent > ~/.ssh-agent-thing
fi
if [[ "$SSH_AGENT_PID" == "" ]]; then
    eval "$(<~/.ssh-agent-thing)"
fi

# Auto-add keys on login
ssh-add -l >/dev/null || alias ssh='ssh-add -l >/dev/null || ssh-add && unalias ssh; ssh'
```

## 🌐 SSH Advanced Features

### Port Forwarding (Tunneling)

#### Local Port Forwarding
```bash
# Forward local port to remote service
ssh -L 8080:localhost:80 user@server

# Forward local port to different remote host
ssh -L 3306:database.internal:3306 user@jumpserver

# Background forwarding
ssh -fN -L 8080:localhost:80 user@server
```

#### Remote Port Forwarding
```bash
# Forward remote port to local service
ssh -R 8080:localhost:80 user@server

# Allow remote connections to forwarded port
ssh -R 0.0.0.0:8080:localhost:80 user@server
```

#### Dynamic Port Forwarding (SOCKS Proxy)
```bash
# Create SOCKS proxy
ssh -D 1080 user@server

# Use with applications
curl --socks5 localhost:1080 http://example.com
```

### SSH File Transfer

#### SCP (Secure Copy)
```bash
# Copy file to remote server
scp file.txt user@server:/path/to/destination/

# Copy file from remote server
scp user@server:/path/to/file.txt ./

# Copy directory recursively
scp -r directory/ user@server:/path/to/destination/

# Copy with specific SSH key
scp -i ~/.ssh/key file.txt user@server:/path/
```

#### SFTP (SSH File Transfer Protocol)
```bash
# Interactive SFTP session
sftp user@server

# SFTP commands
sftp> put file.txt
sftp> get remote_file.txt
sftp> ls
sftp> cd /path/to/directory
sftp> mkdir new_directory
sftp> bye

# Batch SFTP operations
echo "put file.txt" | sftp user@server
```

#### rsync over SSH
```bash
# Sync files using rsync over SSH
rsync -avz -e ssh source/ user@server:/destination/

# Sync with progress and compression
rsync -avz --progress -e "ssh -i ~/.ssh/key" source/ user@server:/dest/

# Exclude files
rsync -avz --exclude='*.log' source/ user@server:/dest/
```

## 🔍 SSH Troubleshooting

### Connection Debugging
```bash
# Verbose SSH connection
ssh -v user@server
ssh -vv user@server  # More verbose
ssh -vvv user@server # Maximum verbosity

# Test SSH key authentication
ssh -T git@github.com

# Check SSH client configuration
ssh -G hostname

# Test SSH server connectivity
nc -zv server_ip 22
telnet server_ip 22
```

### Common SSH Issues and Solutions

#### Permission Issues
```bash
# Fix SSH directory permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 600 ~/.ssh/config
chmod 644 ~/.ssh/authorized_keys

# Fix server permissions
sudo chown -R user:user ~/.ssh
sudo restorecon -R ~/.ssh  # SELinux systems
```

#### Host Key Issues
```bash
# Remove old host key
ssh-keygen -R hostname

# Add new host key
ssh-keyscan hostname >> ~/.ssh/known_hosts

# Skip host key checking (not recommended for production)
ssh -o StrictHostKeyChecking=no user@server
```

#### Authentication Issues
```bash
# Check SSH agent
ssh-add -l

# Test key authentication
ssh -i ~/.ssh/key -o PasswordAuthentication=no user@server

# Check server logs
sudo tail -f /var/log/auth.log
sudo journalctl -u ssh -f
```

## 🛡️ SSH Security Best Practices

### Key Management Security
```bash
# Use strong passphrases
ssh-keygen -t ed25519 -f ~/.ssh/secure_key -C "secure@example.com"

# Rotate keys regularly
ssh-keygen -t ed25519 -f ~/.ssh/new_key
# Update authorized_keys on servers
# Remove old keys

# Use different keys for different purposes
ssh-keygen -t ed25519 -f ~/.ssh/github_key -C "github access"
ssh-keygen -t ed25519 -f ~/.ssh/server_key -C "server access"
```

### Server Hardening
```bash
# Change default SSH port
sudo sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config

# Disable root login
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Limit user access
echo "AllowUsers ubuntu admin" | sudo tee -a /etc/ssh/sshd_config

# Configure fail2ban for SSH protection
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Network Security
```bash
# Configure firewall for SSH
sudo ufw allow 2222/tcp
sudo ufw deny 22/tcp
sudo ufw enable

# Restrict SSH access by IP
sudo ufw allow from 192.168.1.0/24 to any port 2222
```

## 📊 SSH Monitoring and Logging

### SSH Activity Monitoring
```bash
# Monitor SSH connections
sudo tail -f /var/log/auth.log | grep ssh

# Show current SSH sessions
who
w
last

# Check SSH process information
sudo netstat -tlnp | grep :22
sudo ss -tlnp | grep :22
```

### SSH Log Analysis
```bash
# Analyze SSH login attempts
grep "Failed password" /var/log/auth.log
grep "Accepted password" /var/log/auth.log
grep "ssh" /var/log/auth.log | grep "Invalid user"

# SSH connection statistics
awk '/ssh.*Accepted/ {print $1, $2, $3, $9, $11}' /var/log/auth.log

# Failed login attempts by IP
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -nr
```

### Automated SSH Security Monitoring
```bash
#!/bin/bash
# ssh_monitor.sh - Monitor SSH security

LOG_FILE="/var/log/auth.log"
ALERT_EMAIL="admin@example.com"
FAILED_LOGIN_THRESHOLD=5

# Check for failed login attempts
failed_logins=$(grep "Failed password" "$LOG_FILE" | grep "$(date '+%b %d')" | wc -l)

if [ "$failed_logins" -gt "$FAILED_LOGIN_THRESHOLD" ]; then
    echo "WARNING: $failed_logins failed SSH login attempts today" | \
    mail -s "SSH Security Alert" "$ALERT_EMAIL"
fi

# Check for successful root logins
root_logins=$(grep "Accepted.*root" "$LOG_FILE" | grep "$(date '+%b %d')" | wc -l)

if [ "$root_logins" -gt 0 ]; then
    echo "WARNING: $root_logins root login attempts today" | \
    mail -s "Root Login Alert" "$ALERT_EMAIL"
fi
```

## ✅ Requirements

- Ubuntu 16.04 LTS or later
- OpenSSH client and server
- Understanding of public key cryptography
- Basic networking knowledge
- Text editor for configuration files

## 🎓 Resources

- [OpenSSH Documentation](https://www.openssh.com/manual.html)
- [SSH Protocol Specification](https://tools.ietf.org/html/rfc4253)
- [SSH Security Best Practices](https://infosec.mozilla.org/guidelines/openssh)
- [SSH Hardening Guide](https://www.ssh.com/academy/ssh/sshd_config)
- [Public Key Cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*

* **2. Client configuration file**
  * [2-ssh_config](./2-ssh_config): SSH configuration file configured to use the private key
`~/.ssh/holberton` and to refuse authentication using a password.
0x0B-ssh
