# 0x0D. Web Stack Debugging #0

![Shell](https://img.shields.io/badge/Shell-Bash-lightgrey)
![DevOps](https://img.shields.io/badge/DevOps-Web%20Stack%20Debugging-blue)
![Debugging](https://img.shields.io/badge/Debugging-Apache-orange)
![SysAdmin](https://img.shields.io/badge/SysAdmin-Scripting-green)

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
- [Testing](#testing)
- [Best Practices](#best-practices)
- [Resources](#resources)
- [Author](#author)

## 📝 Description

This is the first project in a series of web stack debugging challenges. The goal is to get Apache web server running properly on Ubuntu 14.04 LTS containers. This project focuses on identifying and fixing issues that prevent web services from functioning correctly.

**Key Focus Areas:**
- Container debugging
- Web server troubleshooting
- Service management
- Network connectivity
- Process monitoring
- Log analysis

## 🎯 Learning Objectives

By the end of this project, you will be able to:

- **Web Stack Debugging:** Understand the fundamentals of web stack debugging
- **Service Management:** Learn how to start, stop, and manage web services
- **Container Troubleshooting:** Debug issues within isolated container environments
- **Apache Configuration:** Understand basic Apache web server setup
- **Network Diagnostics:** Use tools to diagnose network connectivity issues
- **Log Analysis:** Read and interpret system and service logs
- **Automation:** Write scripts to automate debugging and fixing processes

## 🛠 Technologies Used

- **Operating System:** Ubuntu 14.04 LTS
- **Web Server:** Apache HTTP Server
- **Container:** Docker
- **Shell:** Bash
- **Tools:** curl, ps, netstat, systemctl/service

## 🌍 Environment

- **OS:** Ubuntu 14.04 LTS
- **Container Runtime:** Docker
- **Web Server:** Apache2
- **Shell:** `/bin/bash`

## ⚙️ Requirements

### General
- All files interpreted on Ubuntu 14.04 LTS
- All files end with a new line
- A `README.md` file at the root of the project folder is mandatory
- All Bash script files must be executable
- Scripts must pass Shellcheck without any error
- Scripts must run without error
- First line of all Bash scripts: `#!/usr/bin/env bash`
- Second line of all Bash scripts: comment explaining the script

### Docker Container Requirements
- Ubuntu 14.04 LTS container with Apache2 installed
- Container must be accessible via HTTP
- Apache service must be properly configured

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/salmaneben/alx-system_engineering-devops.git
cd alx-system_engineering-devops/0x0D-web_stack_debugging_0
```

2. **Make scripts executable:**
```bash
chmod +x 0-give_me_a_page
```

3. **Test in Docker container:**
```bash
docker run -p 8080:80 -d -it ubuntu:14.04
docker exec -it <container_id> /bin/bash
```

## 📋 Tasks

### 0. Give me a page!
**File:** `0-give_me_a_page`

**Objective:** Fix the Apache web server to respond to GET requests on port 80.

**Problem:** Apache is not running or configured properly in the container.

**Solution Approach:**
- Check if Apache is installed
- Start the Apache service
- Verify the service is running
- Test HTTP connectivity

**Expected Output:**
```bash
curl 0:8080
# Should return HTML content instead of connection refused
```

## 🔧 Usage Examples

### Running the Debug Script
```bash
# Make the script executable
chmod +x 0-give_me_a_page

# Run the script in the container
./0-give_me_a_page

# Test the web server
curl localhost:80
curl 0:8080  # If port forwarded
```

### Manual Debugging Steps
```bash
# Check if Apache is installed
dpkg -l | grep apache2

# Check Apache service status
service apache2 status

# Start Apache service
service apache2 start

# Verify Apache is listening on port 80
netstat -tlnp | grep :80

# Check for any error logs
tail -f /var/log/apache2/error.log
```

## 🔍 Debugging Methodology

### 1. **Identify the Problem**
```bash
# Test connectivity
curl localhost:80

# Check service status
ps aux | grep apache
service apache2 status
```

### 2. **Analyze Logs**
```bash
# Check error logs
tail -f /var/log/apache2/error.log
tail -f /var/log/apache2/access.log

# Check system logs
tail -f /var/log/syslog
```

### 3. **Check Configuration**
```bash
# Verify Apache configuration
apache2ctl configtest

# Check listening ports
netstat -tlnp
ss -tlnp
```

### 4. **Apply Fix**
```bash
# Start the service
service apache2 start

# Enable service for startup
update-rc.d apache2 enable
```

### 5. **Verify Solution**
```bash
# Test HTTP response
curl -I localhost:80

# Check service is running
service apache2 status
```

## ⚠️ Common Issues & Solutions

### Issue 1: Apache Not Installed
```bash
# Solution: Install Apache
apt-get update
apt-get install -y apache2
```

### Issue 2: Apache Service Not Running
```bash
# Solution: Start the service
service apache2 start
# or
systemctl start apache2
```

### Issue 3: Permission Issues
```bash
# Solution: Check and fix permissions
chown -R www-data:www-data /var/www/
chmod -R 755 /var/www/
```

### Issue 4: Port Already in Use
```bash
# Solution: Check what's using the port
netstat -tlnp | grep :80
# Kill the conflicting process or change port
```

### Issue 5: Configuration Errors
```bash
# Solution: Test and fix configuration
apache2ctl configtest
# Fix any syntax errors in config files
```

## 🧪 Testing

### Automated Testing
```bash
# Test script functionality
./0-give_me_a_page

# Verify HTTP response
response=$(curl -s -o /dev/null -w "%{http_code}" localhost:80)
if [ "$response" = "200" ]; then
    echo "✅ Apache is responding correctly"
else
    echo "❌ Apache is not responding (HTTP $response)"
fi
```

### Manual Testing
```bash
# Test with curl
curl localhost:80
curl -I localhost:80

# Test with browser (if GUI available)
# Open http://localhost:80

# Test from external container
curl container_ip:80
```

## 📚 Best Practices

### 1. **Systematic Debugging**
- Always check service status first
- Review logs for error messages
- Test connectivity step by step
- Document the debugging process

### 2. **Script Best Practices**
- Add error handling
- Include informative comments
- Test scripts thoroughly
- Make scripts idempotent

### 3. **Security Considerations**
- Keep Apache updated
- Remove unnecessary modules
- Configure proper access controls
- Monitor security logs

### 4. **Performance Optimization**
- Monitor resource usage
- Configure appropriate worker limits
- Enable compression when appropriate
- Use caching strategies

## 📖 Resources

### Official Documentation
- [Apache HTTP Server Documentation](https://httpd.apache.org/docs/)
- [Ubuntu Server Guide - Apache](https://ubuntu.com/server/docs/web-servers-apache)

### Debugging Tools
- [curl Documentation](https://curl.se/docs/)
- [netstat Manual](https://linux.die.net/man/8/netstat)
- [systemctl Manual](https://www.freedesktop.org/software/systemd/man/systemctl.html)

### Best Practices
- [Web Server Security](https://www.apache.org/security/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 👤 Author

**Salman Eben**
- GitHub: [@salmaneben](https://github.com/salmaneben)
- Project: ALX School System Engineering & DevOps

---

*This project is part of the ALX School curriculum on System Engineering and DevOps.*
