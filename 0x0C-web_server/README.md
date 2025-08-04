# 0x0C. Web Server

![Web Server](https://img.shields.io/badge/Web-Server-blue)
![Nginx](https://img.shields.io/badge/Nginx-HTTP%20Server-green)
![HTTP](https://img.shields.io/badge/HTTP-Protocol-orange)
![DevOps](https://img.shields.io/badge/DevOps-Automation-red)

## 📋 Description

This project focuses on web server configuration and management using Nginx. You'll learn to install, configure, and optimize web servers, handle HTTP requests, implement redirects, set up custom error pages, and automate server configuration using scripts. This forms the foundation for understanding web infrastructure and server administration.

## 🎯 Learning Objectives

By the end of this project, you should be able to:

- Understand the role of web servers in the internet infrastructure
- Install and configure Nginx web server
- Manage HTTP requests and responses
- Configure virtual hosts and domain handling
- Implement HTTP redirects and URL rewriting
- Set up custom error pages (404, etc.)
- Understand child processes and process management
- Automate web server configuration with scripts
- Monitor web server performance and logs
- Implement basic security measures for web servers

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-transfer_file` | Script that transfers a file from client to server using scp |
| `1-install_nginx_web_server` | Script that installs and configures Nginx web server |
| `2-setup_a_domain_name` | Domain name setup documentation and configuration |
| `3-redirection` | Script that configures Nginx redirect rules |
| `4-not_found_page_404` | Script that configures a custom 404 error page |
| `7-puppet_install_nginx_web_server.pp` | Puppet manifest for automated Nginx installation |

## 🌐 Web Server Fundamentals

### What is a Web Server?

A web server is software that serves web content to clients over HTTP/HTTPS. It:
- **Handles HTTP Requests**: Processes GET, POST, PUT, DELETE requests
- **Serves Static Content**: HTML, CSS, JavaScript, images, files
- **Manages Virtual Hosts**: Multiple websites on one server
- **Provides Security**: SSL/TLS, access control, authentication
- **Enables Scalability**: Load balancing, caching, compression

### HTTP Protocol Basics
```
HTTP Request Flow:
Client → DNS Resolution → TCP Connection → HTTP Request → Web Server
Web Server → Process Request → Generate Response → Send Response → Client
```

### Common HTTP Status Codes
- **200 OK**: Request successful
- **301 Moved Permanently**: Permanent redirect
- **302 Found**: Temporary redirect
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error
- **503 Service Unavailable**: Server overloaded

## 🔧 Nginx Web Server Setup

### Installing Nginx
```bash
#!/usr/bin/env bash
# 1-install_nginx_web_server - Install and configure Nginx

# Update package repository
sudo apt-get update

# Install Nginx
sudo apt-get install -y nginx

# Allow Nginx through firewall
sudo ufw allow 'Nginx Full'

# Create custom index page
echo "Hello World!" | sudo tee /var/www/html/index.html

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Check if Nginx is running and responding
if curl -s http://localhost | grep -q "Hello World!"; then
    echo "Nginx installed and configured successfully"
else
    echo "Error: Nginx installation failed"
    exit 1
fi
```

### Basic Nginx Configuration
```nginx
# /etc/nginx/sites-available/default
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    
    server_name _;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    # Custom error pages
    error_page 404 /custom_404.html;
    location = /custom_404.html {
        root /var/www/html;
        internal;
    }
    
    # Access and error logs
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
}
```

## 📂 File Transfer and Management

### SCP File Transfer
```bash
#!/usr/bin/env bash
# 0-transfer_file - Transfer file from client to server using scp

# Check if correct number of parameters
if [ $# -lt 4 ]; then
    echo "Usage: $0 PATH_TO_FILE IP USERNAME PATH_TO_SSH_KEY"
    exit 1
fi

# Assign parameters to variables
FILE_PATH=$1
SERVER_IP=$2
USERNAME=$3
SSH_KEY=$4

# Transfer file using scp
scp -o StrictHostKeyChecking=no -i "$SSH_KEY" "$FILE_PATH" "$USERNAME@$SERVER_IP":~/

# Check if transfer was successful
if [ $? -eq 0 ]; then
    echo "File transferred successfully to $USERNAME@$SERVER_IP"
else
    echo "Error: File transfer failed"
    exit 1
fi
```

### Advanced File Transfer Options
```bash
# Transfer with compression
scp -C -i ~/.ssh/key file.txt user@server:~/

# Transfer directory recursively
scp -r -i ~/.ssh/key directory/ user@server:~/

# Transfer with progress indicator
scp -v -i ~/.ssh/key file.txt user@server:~/

# Transfer multiple files
scp -i ~/.ssh/key file1.txt file2.txt user@server:~/

# Rsync for efficient transfers
rsync -avz -e "ssh -i ~/.ssh/key" file.txt user@server:~/
```

## 🌍 Domain Name Configuration

### Domain Setup Process
```bash
# 2-setup_a_domain_name
# Domain configuration guide

# 1. Register domain with domain registrar
# 2. Configure DNS records
# 3. Point domain to server IP

# DNS Record Types:
# A Record: domain.com → IP Address
# CNAME: www.domain.com → domain.com
# MX: Email server configuration
# TXT: Domain verification, SPF records
```

### DNS Configuration Example
```bash
# DNS Records Configuration
# Type    Name    Value               TTL
# A       @       your_server_ip      300
# A       www     your_server_ip      300
# CNAME   blog    domain.com          300
# MX      @       mail.domain.com     300

# Verify DNS propagation
dig domain.com
nslookup domain.com
host domain.com

# Check if domain points to server
ping domain.com
curl -I http://domain.com
```

## ↩️ HTTP Redirects Configuration

### Implementing Redirects
```bash
#!/usr/bin/env bash
# 3-redirection - Configure Nginx redirect

# Install Nginx if not present
sudo apt-get update
sudo apt-get install -y nginx

# Configure redirect in Nginx
sudo tee /etc/nginx/sites-available/default > /dev/null <<EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    root /var/www/html;
    index index.html index.htm;
    
    server_name _;
    
    # Redirect /redirect_me to another URL
    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }
    
    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF

# Test configuration and reload
sudo nginx -t
sudo systemctl reload nginx

echo "Redirect configured: /redirect_me → YouTube"
```

### Advanced Redirect Patterns
```nginx
server {
    listen 80;
    server_name old-domain.com;
    
    # Permanent redirect entire domain
    return 301 https://new-domain.com$request_uri;
}

server {
    listen 80;
    server_name example.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name example.com;
    
    # Conditional redirects
    location /old-path {
        return 301 /new-path;
    }
    
    # Regex redirects
    location ~ ^/product/(\d+) {
        return 301 /item/$1;
    }
    
    # Temporary redirect
    location /maintenance {
        return 302 /under-construction.html;
    }
}
```

## 🚫 Custom Error Pages

### 404 Error Page Configuration
```bash
#!/usr/bin/env bash
# 4-not_found_page_404 - Configure custom 404 error page

# Install Nginx
sudo apt-get update
sudo apt-get install -y nginx

# Create custom 404 page
sudo tee /var/www/html/custom_404.html > /dev/null <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>404 - Page Not Found</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 100px; }
        h1 { color: #e74c3c; font-size: 3em; }
        p { font-size: 1.2em; color: #666; }
        a { color: #3498db; text-decoration: none; }
    </style>
</head>
<body>
    <h1>Ceci n'est pas une page</h1>
    <p>The page you are looking for could not be found.</p>
    <a href="/">Return to Home</a>
</body>
</html>
EOF

# Configure Nginx to use custom 404 page
sudo tee /etc/nginx/sites-available/default > /dev/null <<EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    root /var/www/html;
    index index.html index.htm;
    
    server_name _;
    
    # Custom 404 error page
    error_page 404 /custom_404.html;
    location = /custom_404.html {
        root /var/www/html;
        internal;
    }
    
    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF

# Test and reload Nginx
sudo nginx -t
sudo systemctl reload nginx

echo "Custom 404 page configured successfully"
```

### Multiple Error Pages
```nginx
server {
    listen 80;
    root /var/www/html;
    
    # Multiple error page configurations
    error_page 404 /errors/404.html;
    error_page 403 /errors/403.html;
    error_page 500 502 503 504 /errors/50x.html;
    
    location ^~ /errors/ {
        internal;
        root /var/www/html;
    }
    
    # Custom error page with variables
    error_page 404 = @fallback;
    
    location @fallback {
        proxy_pass http://backend;
        proxy_set_header Host $host;
    }
}
```

## 🤖 Puppet Automation

### Automated Nginx Installation
```puppet
# 7-puppet_install_nginx_web_server.pp
# Install and configure Nginx using Puppet

# Ensure Nginx package is installed
package { 'nginx':
  ensure => installed,
}

# Create custom index page
file { '/var/www/html/index.html':
  ensure  => file,
  content => 'Hello World!',
  owner   => 'www-data',
  group   => 'www-data',
  mode    => '0644',
  require => Package['nginx'],
}

# Configure Nginx default site
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => template('nginx/default.erb'),
  notify  => Service['nginx'],
  require => Package['nginx'],
}

# Ensure Nginx service is running
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => Package['nginx'],
}

# Configure redirect
file_line { 'nginx_redirect':
  path    => '/etc/nginx/sites-available/default',
  line    => '    location /redirect_me { return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4; }',
  match   => '^\s*location / {',
  require => File['/etc/nginx/sites-available/default'],
  notify  => Service['nginx'],
}
```

## 📊 Web Server Monitoring

### Nginx Status Monitoring
```nginx
# Enable Nginx status module
server {
    listen 8080;
    server_name localhost;
    
    location /nginx_status {
        stub_status on;
        access_log off;
        allow 127.0.0.1;
        deny all;
    }
}
```

### Log Analysis
```bash
# Real-time log monitoring
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Analyze access patterns
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr

# Check response codes
awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c | sort -nr

# Monitor bandwidth usage
awk '{sum += $10} END {print sum/1024/1024 " MB"}' /var/log/nginx/access.log
```

### Performance Monitoring Script
```bash
#!/bin/bash
# nginx_monitor.sh - Monitor Nginx performance

echo "=== Nginx Performance Monitor ==="
echo "Time: $(date)"
echo ""

# Check if Nginx is running
if systemctl is-active --quiet nginx; then
    echo "✓ Nginx Status: Running"
else
    echo "✗ Nginx Status: Not Running"
    exit 1
fi

# Check connections
echo "Active Connections:"
curl -s http://localhost:8080/nginx_status | grep "Active connections"

# Check server load
echo "Server Load:"
uptime

# Check memory usage
echo "Memory Usage:"
free -h | grep Mem

# Check recent errors
echo "Recent Errors (last 10):"
tail -10 /var/log/nginx/error.log

# Check disk usage for logs
echo "Log Directory Usage:"
du -sh /var/log/nginx/
```

## 🔐 Web Server Security

### Basic Security Configuration
```nginx
server {
    listen 80;
    server_name example.com;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # Hide server version
    server_tokens off;
    
    # Deny access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # Deny access to sensitive files
    location ~* \.(htaccess|htpasswd|ini|log|sh|sql|conf)$ {
        deny all;
    }
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;
    location /api/ {
        limit_req zone=one burst=5;
    }
}
```

### SSL/HTTPS Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # SSL Configuration
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;
    
    location / {
        root /var/www/html;
        index index.html;
    }
}
```

## ✅ Requirements

- Ubuntu 16.04 LTS or later
- Nginx 1.10 or later
- Understanding of HTTP protocol
- Basic knowledge of DNS and networking
- Familiarity with Linux command line
- SSH access to server

## 🎓 Resources

- [Nginx Documentation](https://nginx.org/en/docs/)
- [HTTP Protocol Specification](https://tools.ietf.org/html/rfc7231)
- [Web Server Security Guide](https://www.nginx.com/blog/nginx-security-best-practices/)
- [DNS Configuration Guide](https://www.cloudflare.com/learning/dns/what-is-dns/)
- [SSL/TLS Best Practices](https://wiki.mozilla.org/Security/Server_Side_TLS)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
- [Nginx](https://en.wikipedia.org/wiki/Nginx)
- [How to Configure Nginx](https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-server-blocks-virtual-hosts-on-ubuntu-16-04)
- [Root and sub domain](https://landingi.com/help/domains-vs-subdomains/)
- [HTTP requests](https://www.tutorialspoint.com/http/http_methods.htm)
- [HTTP redirection](https://moz.com/learn/seo/redirection)
- [Not found HTTP response code](https://en.wikipedia.org/wiki/HTTP_404)
- [Logs files on Linux](https://www.cyberciti.biz/faq/ubuntu-linux-gnome-system-log-viewer/)
- [RFC 7231 (HTTP/1.1)](https://datatracker.ietf.org/doc/html/rfc7231)
- [RFC 7540 (HTTP/2)](https://datatracker.ietf.org/doc/html/rfc7540)

## Tasks

<details>
<summary><a href="./0-transfer_file">0. Transfer a file to your server</a></summary><br>
<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/j2P4SmgY/image.png' border='0' alt='image'/></a>
</details>

<details>
<summary><a href="./1-install_nginx_web_server">1. Install nginx web server</a></summary><br>
<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/QMbf1FrY/image.png' border='0' alt='image'/></a>
<a href='https://postimg.cc/621fsx68' target='_blank'><img src='https://i.postimg.cc/vTGqVGpt/image.png' border='0' alt='image'/></a>
</details>

<details>
<summary><a href="./2-setup_a_domain_name">2. Setup a domain name</a></summary><br>
<a href='https://postimg.cc/svdGgYqp' target='_blank'><img src='https://i.postimg.cc/L6htvvV0/image.png' border='0' alt='image'/></a>
</details>

<details>
<summary><a href="./3-redirection">3. Redirection</a></summary><br>
<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/tTmZ8GqZ/image.png' border='0' alt='image'/></a>
</details>

<details>
<summary><a href="./4-not_found_page_404">4. Not found page 404</a></summary><br>
<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/zvhdBrG6/image.png' border='0' alt='image'/></a>
</details>

<details>
<summary><a href="./7-puppet_install_nginx_web_server.pp">5. Install Nginx web server (w/ Puppet)</a></summary><br>
<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/Vs2dxb0D/image.png' border='0' alt='image'/></a>
</details>
