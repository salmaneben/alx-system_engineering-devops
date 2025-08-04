# 0x0E. Web Stack Debugging #1

![Shell](https://img.shields.io/badge/Shell-Bash-lightgrey)
![DevOps](https://img.shields.io/badge/DevOps-Web%20Stack%20Debugging-blue)
![Nginx](https://img.shields.io/badge/Web%20Server-Nginx-green)
![SysAdmin](https://img.shields.io/badge/SysAdmin-Debugging-orange)

## 📋 Table of Contents
- [Description](#description)
- [Learning Objectives](#learning-objectives)
- [Technologies Used](#technologies-used)
- [Environment](#environment)
- [Requirements](#requirements)
- [Installation](#installation)
- [Tasks](#tasks)
- [Usage Examples](#usage-examples)
- [Debugging Methodology](#debugging-methodology)
- [Common Issues & Solutions](#common-issues--solutions)
- [Nginx Configuration](#nginx-configuration)
- [Testing & Validation](#testing--validation)
- [Performance Optimization](#performance-optimization)
- [Security Best Practices](#security-best-practices)
- [Resources](#resources)
- [Author](#author)

## 📝 Description

This is the second project in the web stack debugging series, focusing specifically on **Nginx web server** troubleshooting and configuration. The project involves identifying and fixing issues that prevent Nginx from properly listening on port 80 and serving web content.

**Key Focus Areas:**
- Nginx service management
- Port configuration and binding
- Network interface configuration
- Service optimization
- Process management
- Configuration validation

## 🎯 Learning Objectives

By the end of this project, you will be able to:

- **Nginx Debugging:** Master the fundamentals of Nginx troubleshooting
- **Port Management:** Configure Nginx to listen on specific ports and interfaces
- **Service Configuration:** Understand Nginx configuration files and directives
- **Process Optimization:** Write efficient scripts for service management
- **Network Diagnostics:** Diagnose and resolve network binding issues
- **Configuration Testing:** Validate Nginx configurations before deployment
- **Performance Tuning:** Optimize Nginx for better performance

## 🛠 Technologies Used

- **Operating System:** Ubuntu 20.04 LTS
- **Web Server:** Nginx
- **Shell:** Bash
- **Tools:** curl, netstat, ss, nginx -t, systemctl
- **Configuration:** Nginx conf files

## 🌍 Environment

- **OS:** Ubuntu 20.04 LTS
- **Web Server:** Nginx 1.18+
- **Shell:** `/bin/bash`
- **Network:** IPv4/IPv6 support
- **Ports:** 80 (HTTP), 443 (HTTPS)

## ⚙️ Requirements

### General
- All files interpreted on Ubuntu 20.04 LTS
- All files end with a new line
- A `README.md` file at the root of the project folder is mandatory
- All Bash script files must be executable
- Scripts must pass Shellcheck without any error
- Scripts must run without error
- First line of all Bash scripts: `#!/usr/bin/env bash`
- Second line of all Bash scripts: comment explaining the script

### Nginx Requirements
- Nginx must be running and enabled
- Nginx must listen on port 80 of all server's active IPv4 IPs
- Configuration must be syntactically correct
- Service must start automatically on boot

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/salmaneben/alx-system_engineering-devops.git
cd alx-system_engineering-devops/0x0E-web_stack_debugging_1
```

2. **Make scripts executable:**
```bash
chmod +x 0-nginx_likes_port_80
chmod +x 1-debugging_made_short
```

3. **Install Nginx (if not already installed):**
```bash
sudo apt update
sudo apt install nginx -y
```

## 📋 Tasks

### 0. Nginx likes port 80
**File:** `0-nginx_likes_port_80`

**Objective:** Configure Nginx to run and listen on port 80 of all server's active IPv4 addresses.

**Problem:** Nginx is not listening on port 80 or not configured properly.

**Requirements:**
- Nginx must be running
- Nginx must be listening on port 80 of all active IPv4 IPs
- Service must be accessible via HTTP

### 1. Make it sweet and short
**File:** `1-debugging_made_short`

**Objective:** Create a short and efficient script (5 lines or less) that configures Nginx to listen on port 80.

**Requirements:**
- Script must be 5 lines or less
- Nginx must be listening on port 80
- No unnecessary commands
- Script must be efficient and concise

## 🔧 Usage Examples

### Task 0: Full Configuration Script
```bash
# Run the configuration script
sudo ./0-nginx_likes_port_80

# Verify Nginx is running
sudo systemctl status nginx

# Test HTTP connectivity
curl -I localhost:80
curl -I 0.0.0.0:80
```

### Task 1: Short Configuration Script
```bash
# Run the optimized script
sudo ./1-debugging_made_short

# Quick verification
curl localhost:80
```

### Manual Debugging Commands
```bash
# Check Nginx status
sudo systemctl status nginx

# Test Nginx configuration
sudo nginx -t

# View listening ports
sudo netstat -tlnp | grep nginx
sudo ss -tlnp | grep nginx

# Check Nginx processes
ps aux | grep nginx
```

## 🔍 Debugging Methodology

### 1. **Initial Assessment**
```bash
# Check if Nginx is installed
nginx -v

# Check service status
sudo systemctl status nginx

# Test basic connectivity
curl localhost:80
```

### 2. **Configuration Analysis**
```bash
# Test configuration syntax
sudo nginx -t

# View main configuration
sudo cat /etc/nginx/nginx.conf

# Check sites configuration
sudo cat /etc/nginx/sites-enabled/default
```

### 3. **Network Diagnostics**
```bash
# Check listening ports
sudo netstat -tlnp | grep :80
sudo ss -tlnp sport = :80

# Check all listening addresses
sudo netstat -tlnp | grep nginx
```

### 4. **Service Management**
```bash
# Start Nginx
sudo systemctl start nginx

# Enable for startup
sudo systemctl enable nginx

# Reload configuration
sudo systemctl reload nginx
```

### 5. **Validation**
```bash
# Test HTTP response
curl -I localhost:80

# Check from external IP
curl -I your_server_ip:80

# Verify listening on all interfaces
sudo netstat -tlnp | grep :80
```

## ⚠️ Common Issues & Solutions

### Issue 1: Nginx Not Listening on Port 80
```bash
# Check what's using port 80
sudo netstat -tlnp | grep :80

# If Apache is running, stop it
sudo systemctl stop apache2
sudo systemctl disable apache2

# Start Nginx
sudo systemctl start nginx
```

### Issue 2: Permission Denied on Port 80
```bash
# Ensure running as root/sudo
sudo systemctl start nginx

# Check if another service is using port 80
sudo lsof -i :80
```

### Issue 3: Configuration Errors
```bash
# Test configuration
sudo nginx -t

# Common fix - check syntax in default site
sudo nano /etc/nginx/sites-enabled/default

# Reload after fixing
sudo nginx -s reload
```

### Issue 4: Service Not Starting
```bash
# Check detailed status
sudo systemctl status nginx -l

# Check logs
sudo journalctl -u nginx -f
sudo tail -f /var/log/nginx/error.log
```

### Issue 5: Not Listening on All Interfaces
```bash
# Edit default site configuration
sudo nano /etc/nginx/sites-enabled/default

# Ensure listen directive is:
# listen 80 default_server;
# listen [::]:80 default_server;
```

## ⚙️ Nginx Configuration

### Basic Server Block
```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    server_name _;
    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Multiple Interface Configuration
```nginx
server {
    listen 0.0.0.0:80;
    listen [::]:80;
    server_name example.com;
    # Additional configuration...
}
```

### Configuration Testing
```bash
# Test syntax
sudo nginx -t

# Test and show configuration details
sudo nginx -T

# Reload configuration
sudo nginx -s reload
```

## 🧪 Testing & Validation

### Automated Testing Script
```bash
#!/bin/bash
# Test Nginx configuration

echo "Testing Nginx configuration..."

# Test 1: Check if Nginx is running
if systemctl is-active --quiet nginx; then
    echo "✅ Nginx is running"
else
    echo "❌ Nginx is not running"
    exit 1
fi

# Test 2: Check if listening on port 80
if netstat -tlnp | grep -q ":80.*nginx"; then
    echo "✅ Nginx is listening on port 80"
else
    echo "❌ Nginx is not listening on port 80"
    exit 1
fi

# Test 3: Test HTTP response
if curl -s -o /dev/null -w "%{http_code}" localhost:80 | grep -q "200"; then
    echo "✅ HTTP response successful"
else
    echo "❌ HTTP response failed"
    exit 1
fi

echo "🎉 All tests passed!"
```

### Manual Testing
```bash
# Test various endpoints
curl localhost:80
curl 127.0.0.1:80
curl 0.0.0.0:80

# Test with verbose output
curl -v localhost:80

# Test headers only
curl -I localhost:80
```

## 🚀 Performance Optimization

### Worker Process Configuration
```nginx
# /etc/nginx/nginx.conf
worker_processes auto;
worker_connections 1024;

events {
    use epoll;
    worker_connections 1024;
    multi_accept on;
}
```

### Monitoring Commands
```bash
# Monitor Nginx processes
ps aux | grep nginx

# Check memory usage
sudo systemctl status nginx

# Monitor connections
sudo netstat -an | grep :80 | wc -l
```

## 🔒 Security Best Practices

### Basic Security Configuration
```nginx
# Hide Nginx version
server_tokens off;

# Add security headers
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
```

### Firewall Configuration
```bash
# Allow HTTP traffic
sudo ufw allow 'Nginx HTTP'

# Check firewall status
sudo ufw status
```

## 📖 Resources

### Official Documentation
- [Nginx Documentation](http://nginx.org/en/docs/)
- [Nginx Configuration Guide](http://nginx.org/en/docs/beginners_guide.html)

### Debugging Tools
- [Nginx Testing Tool](http://nginx.org/en/docs/debugging_log.html)
- [systemctl Manual](https://www.freedesktop.org/software/systemd/man/systemctl.html)

### Best Practices
- [Nginx Performance Tuning](https://www.nginx.com/blog/tuning-nginx/)
- [Nginx Security Guide](https://www.nginx.com/blog/nginx-security-best-practices/)

## 👤 Author

**Salman Eben**
- GitHub: [@salmaneben](https://github.com/salmaneben)
- Project: ALX School System Engineering & DevOps

---

*This project is part of the ALX School curriculum on System Engineering and DevOps.*
