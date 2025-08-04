# 0x12. Web Stack Debugging #2

![Debugging](https://img.shields.io/badge/Debugging-Web%20Stack-red)
![Security](https://img.shields.io/badge/Security-User%20Management-blue)
![Nginx](https://img.shields.io/badge/Nginx-Configuration-green)

## 📋 Description

This project focuses on web stack debugging with an emphasis on security and user management. You'll learn to troubleshoot permission issues, configure services to run as non-root users, and implement secure web server configurations. This is essential for maintaining secure and properly configured production environments.

## 🎯 Learning Objectives

By the end of this project, you should be able to:

- Run processes as different users for security
- Configure web servers to run as non-privileged users
- Debug permission-related issues in web stacks
- Understand the principle of least privilege
- Troubleshoot user and group permission problems
- Configure Nginx to run securely on non-standard ports
- Implement security best practices for web services

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-iamsomeonelese` | Script that runs the `whoami` command as another user |
| `1-run_nginx_as_nginx` | Script that configures Nginx to run as the nginx user on port 8080 |
| `100-fix_in_7_lines_or_less` | Optimized version of task 1 in 7 lines or less |

## 🔧 User Management and Security

### Running Commands as Different Users

#### Using `su` Command
```bash
#!/usr/bin/env bash
# 0-iamsomeonelese - Run whoami as another user

if [ $# -eq 0 ]; then
    echo "Usage: $0 <username>"
    exit 1
fi

su - "$1" -c "whoami"
```

#### Alternative Methods
```bash
# Using sudo
sudo -u username whoami

# Using runuser (Red Hat/CentOS)
runuser -l username -c 'whoami'

# Using su without login shell
su username -c "whoami"
```

### Security Best Practices

#### Principle of Least Privilege
- **Run services as dedicated users**: Each service should have its own user
- **Minimal permissions**: Grant only necessary permissions
- **No root privileges**: Avoid running services as root when possible
- **Separate environments**: Isolate different applications

#### User Creation for Services
```bash
# Create system user for web service
sudo useradd --system --no-create-home --shell /bin/false webuser

# Create user with specific home directory
sudo useradd --create-home --shell /bin/bash --home /opt/myapp appuser

# Add user to specific group
sudo usermod -a -G www-data webuser
```

## 🌐 Nginx Security Configuration

### Running Nginx as Non-Root User

#### Problem Analysis
Common issues when running Nginx as non-root:
- **Port permissions**: Ports < 1024 require root privileges
- **File permissions**: Log files and configuration access
- **Process ownership**: Worker processes must run as intended user

#### Solution Implementation
```bash
#!/usr/bin/env bash
# 1-run_nginx_as_nginx - Configure Nginx to run as nginx user on port 8080

# Stop nginx if running
sudo pkill nginx

# Modify nginx configuration
sudo sed -i 's/80;/8080;/g' /etc/nginx/sites-available/default
sudo sed -i 's/#user www-data/user nginx/g' /etc/nginx/nginx.conf

# Ensure nginx user exists
if ! id "nginx" &>/dev/null; then
    sudo useradd --system --no-create-home --shell /bin/false nginx
fi

# Set proper permissions
sudo chown -R nginx:nginx /var/log/nginx
sudo chown -R nginx:nginx /var/lib/nginx

# Start nginx as nginx user
sudo -u nginx /usr/sbin/nginx
```

### Advanced Nginx Security Configuration

#### Complete Security Setup
```nginx
# /etc/nginx/nginx.conf
user nginx;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Hide nginx version
    server_tokens off;
    
    # File upload limits
    client_max_body_size 100M;
    client_body_timeout 60s;
    client_header_timeout 60s;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=login:10m rate=10r/m;
    
    include /etc/nginx/sites-enabled/*;
}
```

#### Site-Specific Configuration
```nginx
# /etc/nginx/sites-available/default
server {
    listen 8080;
    listen [::]:8080;
    
    server_name _;
    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    
    # Security configurations
    location / {
        try_files $uri $uri/ =404;
        
        # Rate limiting for login pages
        location /login {
            limit_req zone=login burst=20 nodelay;
            try_files $uri $uri/ =404;
        }
    }
    
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
    
    # Optimize static file serving
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 🔍 Debugging Techniques

### Permission Debugging

#### Check File Permissions
```bash
# Check file ownership and permissions
ls -la /etc/nginx/nginx.conf
ls -ld /var/log/nginx/
ls -ld /var/lib/nginx/

# Check user and group information
id nginx
groups nginx
getent passwd nginx
```

#### Process Debugging
```bash
# Check running processes
ps aux | grep nginx
pstree -p nginx

# Check which user is running nginx
ps -eo pid,user,cmd | grep nginx

# Check listening ports
sudo netstat -tlnp | grep nginx
sudo ss -tlnp | grep nginx
```

#### System Resource Debugging
```bash
# Check system limits
ulimit -a

# Check for specific user limits
sudo -u nginx sh -c 'ulimit -a'

# Check SELinux status (if applicable)
sestatus
getsebool -a | grep nginx
```

### Log Analysis

#### Nginx Log Analysis
```bash
# Check error logs
sudo tail -f /var/log/nginx/error.log

# Check access logs
sudo tail -f /var/log/nginx/access.log

# Check system logs
sudo journalctl -u nginx -f
sudo tail -f /var/log/syslog | grep nginx
```

#### Common Error Patterns
```bash
# Permission denied errors
grep "Permission denied" /var/log/nginx/error.log

# Port binding issues
grep "bind() to" /var/log/nginx/error.log

# Configuration syntax errors
nginx -t
```

## 🛠️ Troubleshooting Common Issues

### Port Permission Issues

#### Problem: Cannot bind to port 80
```bash
# Error: nginx: [emerg] bind() to 0.0.0.0:80 failed (13: Permission denied)

# Solutions:
# 1. Use port > 1024
sudo sed -i 's/listen 80/listen 8080/g' /etc/nginx/sites-available/default

# 2. Use capabilities (advanced)
sudo setcap 'cap_net_bind_service=+ep' /usr/sbin/nginx

# 3. Use authbind
sudo apt install authbind
sudo touch /etc/authbind/byport/80
sudo chmod 500 /etc/authbind/byport/80
sudo chown nginx /etc/authbind/byport/80
```

### File Permission Issues

#### Problem: Cannot access log files
```bash
# Create proper directory structure
sudo mkdir -p /var/log/nginx
sudo chown -R nginx:nginx /var/log/nginx
sudo chmod 755 /var/log/nginx

# Ensure log rotation works
sudo logrotate -d /etc/logrotate.d/nginx
```

#### Problem: Cannot access web files
```bash
# Set proper web directory permissions
sudo chown -R nginx:nginx /var/www/html
sudo chmod -R 644 /var/www/html
sudo find /var/www/html -type d -exec chmod 755 {} \;
```

### Configuration Issues

#### Nginx Configuration Testing
```bash
# Test configuration syntax
sudo nginx -t

# Test configuration with specific file
sudo nginx -t -c /etc/nginx/nginx.conf

# Check configuration file inclusion
sudo nginx -T | grep -E "include|server"
```

## 📊 Monitoring and Maintenance

### System Monitoring
```bash
# Monitor nginx processes
watch -n 1 'ps aux | grep nginx'

# Monitor port usage
watch -n 1 'sudo netstat -tlnp | grep :8080'

# Monitor log files in real-time
sudo multitail /var/log/nginx/access.log /var/log/nginx/error.log
```

### Automated Health Checks
```bash
#!/usr/bin/env bash
# nginx-health-check.sh

NGINX_PID=$(pgrep nginx)
NGINX_PORT=8080

if [ -z "$NGINX_PID" ]; then
    echo "ERROR: Nginx is not running"
    exit 1
fi

if ! sudo netstat -tlnp | grep -q ":$NGINX_PORT "; then
    echo "ERROR: Nginx is not listening on port $NGINX_PORT"
    exit 1
fi

if ! curl -s -o /dev/null -w "%{http_code}" http://localhost:$NGINX_PORT | grep -q "200"; then
    echo "ERROR: Nginx is not responding correctly"
    exit 1
fi

echo "SUCCESS: Nginx is running correctly on port $NGINX_PORT"
```

## 🔒 Security Hardening

### System-Level Security
```bash
# Disable unnecessary services
sudo systemctl disable apache2
sudo systemctl stop apache2

# Configure firewall
sudo ufw allow 8080/tcp
sudo ufw enable

# Set up fail2ban for nginx
sudo apt install fail2ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
```

### Application-Level Security
```nginx
# Rate limiting configuration
http {
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;
    
    server {
        location /api/ {
            limit_req zone=one burst=5;
        }
    }
}
```

### File System Security
```bash
# Set proper umask for nginx user
echo "umask 022" >> /home/nginx/.profile

# Secure configuration files
sudo chmod 640 /etc/nginx/nginx.conf
sudo chown root:nginx /etc/nginx/nginx.conf
```

## ✅ Requirements

- Ubuntu 16.04 LTS or later
- Nginx installed and configured
- Understanding of Linux user management
- Basic knowledge of file permissions
- Familiarity with systemd services

## 🎓 Resources

- [Nginx Security Guide](https://nginx.org/en/docs/security.html)
- [Linux User Management](https://www.linux.com/training-tutorials/how-manage-users-groups-linux/)
- [File Permissions Guide](https://www.linux.com/training-tutorials/understanding-linux-file-permissions/)
- [Systemd Service Management](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [Web Server Security Best Practices](https://owasp.org/www-project-secure-headers/)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
  * [100-fix_in_7_lines_or_less](./100-fix_in_7_lines_or_less): Bash script
  that fixes a web server to run Nginx listening on port `8080` as the `nginx`
  user.
  * 7 lines long.
