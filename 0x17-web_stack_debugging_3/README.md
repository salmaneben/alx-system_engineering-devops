# 0x17. Web Stack Debugging #3

![Debugging](https://img.shields.io/badge/Debugging-Web%20Stack-red)
![Apache](https://img.shields.io/badge/Apache-Configuration-blue)
![Puppet](https://img.shields.io/badge/Puppet-Automation-orange)
![WordPress](https://img.shields.io/badge/WordPress-LAMP-green)

## 📋 Description

This project focuses on advanced web stack debugging with emphasis on Apache configuration, WordPress troubleshooting, and automation using Puppet. You'll learn to diagnose and fix complex web server issues, optimize Apache performance, and automate fixes using configuration management tools.

## 🎯 Learning Objectives

By the end of this project, you should be able to:

- Debug Apache web server configuration issues
- Troubleshoot WordPress installation problems
- Use strace and other debugging tools effectively
- Automate fixes using Puppet manifests
- Optimize Apache performance and security
- Implement monitoring and logging for web stacks
- Handle PHP-FPM and Apache integration issues
- Diagnose database connectivity problems
- Use systematic debugging approaches

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-strace_is_your_friend.pp` | Puppet manifest that fixes Apache 500 errors by correcting file permissions |

## 🔧 Web Stack Debugging Fundamentals

### Common Web Stack Issues
- **500 Internal Server Error**: Server configuration problems
- **403 Forbidden**: Permission or access control issues
- **404 Not Found**: Missing files or incorrect paths
- **502 Bad Gateway**: Backend service communication problems
- **503 Service Unavailable**: Overloaded or maintenance mode

### LAMP Stack Components
```
Linux (Operating System)
├── Apache (Web Server)
├── MySQL/MariaDB (Database)
└── PHP (Server-side scripting)
```

## 🔍 Debugging Tools and Techniques

### System Debugging Tools

#### strace - System Call Tracer
```bash
# Trace system calls for Apache process
sudo strace -p $(pgrep apache2) -f -e trace=file

# Trace specific file operations
sudo strace -e trace=open,openat,stat apache2ctl restart

# Trace and follow child processes
sudo strace -f -o /tmp/apache_trace.log apache2ctl configtest

# Common strace options
strace -e trace=file,process,network program
strace -c program  # Count system calls
strace -r program  # Show relative timestamps
```

#### lsof - List Open Files
```bash
# Check what files Apache is using
sudo lsof -p $(pgrep apache2)

# Check specific port usage
sudo lsof -i :80
sudo lsof -i :443

# Check file locks
sudo lsof +L1
```

#### Apache Debugging Commands
```bash
# Test Apache configuration
sudo apache2ctl configtest
sudo apache2ctl -S  # Show virtual host configuration

# Check Apache modules
apache2ctl -M

# Verbose configuration check
apache2 -t -D DUMP_VHOSTS -D DUMP_MODULES

# Check Apache status
sudo systemctl status apache2
sudo apache2ctl status
```

### Log Analysis

#### Apache Error Logs
```bash
# Monitor Apache error logs in real-time
sudo tail -f /var/log/apache2/error.log

# Search for specific errors
grep "Internal Server Error" /var/log/apache2/error.log
grep "Permission denied" /var/log/apache2/error.log

# Check access logs for patterns
tail -f /var/log/apache2/access.log | grep "500"
```

#### PHP Error Debugging
```bash
# Enable PHP error logging
sudo nano /etc/php/7.4/apache2/php.ini
# Set: log_errors = On
# Set: error_log = /var/log/php_errors.log

# Check PHP-FPM status
sudo systemctl status php7.4-fpm

# PHP-FPM error logs
sudo tail -f /var/log/php7.4-fpm.log
```

## 🛠️ Puppet Automation for Web Stack Fixes

### Basic Puppet Manifest Structure
```puppet
# 0-strace_is_your_friend.pp
# Fix Apache 500 error by correcting file permissions

# Ensure proper ownership of web directory
file { '/var/www/html':
  ensure  => directory,
  owner   => 'www-data',
  group   => 'www-data',
  mode    => '0755',
  recurse => true,
}

# Fix specific file that causes 500 error
file { '/var/www/html/wp-settings.php':
  ensure => file,
  owner  => 'www-data',
  group  => 'www-data',
  mode   => '0644',
}

# Ensure Apache service is running
service { 'apache2':
  ensure => running,
  enable => true,
}

# Restart Apache after configuration changes
exec { 'restart-apache':
  command     => '/usr/sbin/service apache2 restart',
  refreshonly => true,
  subscribe   => File['/var/www/html/wp-settings.php'],
}
```

### Advanced Puppet Configuration Management
```puppet
# Advanced web stack configuration
class webstack {
  # Package management
  package { ['apache2', 'php', 'php-mysql', 'mysql-server']:
    ensure => installed,
  }

  # Apache configuration
  file { '/etc/apache2/sites-available/000-default.conf':
    ensure  => file,
    content => template('webstack/default-vhost.erb'),
    notify  => Service['apache2'],
  }

  # PHP configuration optimization
  file { '/etc/php/7.4/apache2/php.ini':
    ensure => file,
    source => 'puppet:///modules/webstack/php.ini',
    notify => Service['apache2'],
  }

  # Enable required Apache modules
  exec { 'enable-rewrite':
    command => '/usr/sbin/a2enmod rewrite',
    unless  => '/usr/sbin/apache2ctl -M | grep rewrite',
    notify  => Service['apache2'],
  }

  # Service management
  service { 'apache2':
    ensure  => running,
    enable  => true,
    require => Package['apache2'],
  }
}
```

## 🌐 Apache Configuration Debugging

### Virtual Host Configuration
```apache
# /etc/apache2/sites-available/wordpress.conf
<VirtualHost *:80>
    ServerName example.com
    ServerAlias www.example.com
    DocumentRoot /var/www/html/wordpress
    
    # Directory permissions
    <Directory /var/www/html/wordpress>
        AllowOverride All
        Require all granted
        Options -Indexes +FollowSymLinks
    </Directory>
    
    # Error and access logs
    ErrorLog ${APACHE_LOG_DIR}/wordpress_error.log
    CustomLog ${APACHE_LOG_DIR}/wordpress_access.log combined
    
    # Security headers
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
    Header always set X-XSS-Protection "1; mode=block"
</VirtualHost>
```

### Common Apache Configuration Issues
```bash
# Check for syntax errors
sudo apache2ctl configtest

# Common configuration problems:
# 1. Missing DocumentRoot
# 2. Incorrect file permissions
# 3. Missing directory directives
# 4. Conflicting virtual hosts
# 5. Missing required modules

# Fix permission issues
sudo chown -R www-data:www-data /var/www/html
sudo find /var/www/html -type d -exec chmod 755 {} \;
sudo find /var/www/html -type f -exec chmod 644 {} \;
```

### Apache Module Management
```bash
# List enabled modules
apache2ctl -M

# Enable modules
sudo a2enmod rewrite
sudo a2enmod ssl
sudo a2enmod headers

# Disable modules
sudo a2dismod autoindex
sudo a2dismod status

# Check module configuration
sudo apache2ctl -t -D DUMP_MODULES
```

## 🗄️ Database Connectivity Debugging

### MySQL Connection Issues
```bash
# Test MySQL connectivity
mysql -u username -p -h localhost

# Check MySQL service status
sudo systemctl status mysql

# MySQL error logs
sudo tail -f /var/log/mysql/error.log

# Check MySQL processes
sudo mysqladmin -u root -p processlist

# Test database connection from PHP
cat << 'EOF' > /tmp/test_db.php
<?php
$connection = mysqli_connect('localhost', 'username', 'password', 'database');
if (!$connection) {
    die('Connection failed: ' . mysqli_connect_error());
}
echo 'Connected successfully';
mysqli_close($connection);
?>
EOF

php /tmp/test_db.php
```

### WordPress Database Configuration
```php
// wp-config.php debugging
define('DB_NAME', 'database_name');
define('DB_USER', 'username');
define('DB_PASSWORD', 'password');
define('DB_HOST', 'localhost');

// Enable WordPress debugging
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);

// Check WordPress debug log
tail -f /var/www/html/wp-content/debug.log
```

## 📊 Performance Monitoring and Optimization

### Apache Performance Tuning
```apache
# /etc/apache2/mods-available/mpm_prefork.conf
<IfModule mpm_prefork_module>
    StartServers          8
    MinSpareServers       5
    MaxSpareServers      20
    ServerLimit         256
    MaxRequestWorkers   256
    MaxRequestsPerChild 4000
</IfModule>

# Enable compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>
```

### System Resource Monitoring
```bash
# Monitor Apache processes
watch -n 1 'ps aux | grep apache2 | grep -v grep | wc -l'

# Check memory usage
free -h
top -p $(pgrep apache2 | tr '\n' ',' | sed 's/,$//')

# Monitor disk I/O
iotop -a -o -d 1

# Check file descriptor usage
lsof | grep apache2 | wc -l
```

## 🔒 Security and Hardening

### Apache Security Configuration
```apache
# Security headers
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options DENY
Header always set X-XSS-Protection "1; mode=block"
Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"

# Hide Apache version
ServerTokens Prod
ServerSignature Off

# Disable dangerous HTTP methods
<LimitExcept GET POST HEAD>
    deny from all
</LimitExcept>

# Prevent access to sensitive files
<FilesMatch "\.(htaccess|htpasswd|ini|log|sh|inc|bak)$">
    Require all denied
</FilesMatch>
```

### File Permission Security
```bash
# Secure WordPress installation
sudo chown -R www-data:www-data /var/www/html/
sudo find /var/www/html/ -type d -exec chmod 750 {} \;
sudo find /var/www/html/ -type f -exec chmod 640 {} \;

# Specific WordPress permissions
sudo chmod 600 /var/www/html/wp-config.php
sudo chmod -R 755 /var/www/html/wp-content/uploads/
```

## 🚨 Automated Monitoring and Alerting

### Log Monitoring Script
```bash
#!/bin/bash
# monitor_apache.sh - Monitor Apache for issues

LOG_FILE="/var/log/apache2/error.log"
ALERT_EMAIL="admin@example.com"
CHECK_INTERVAL=60

monitor_errors() {
    local error_count=$(tail -n 100 "$LOG_FILE" | grep -c "Internal Server Error")
    
    if [ "$error_count" -gt 5 ]; then
        echo "High error rate detected: $error_count errors in last 100 lines" | \
        mail -s "Apache Error Alert" "$ALERT_EMAIL"
    fi
}

check_apache_status() {
    if ! systemctl is-active --quiet apache2; then
        echo "Apache service is down, attempting restart" | \
        mail -s "Apache Service Down" "$ALERT_EMAIL"
        
        systemctl restart apache2
    fi
}

# Main monitoring loop
while true; do
    monitor_errors
    check_apache_status
    sleep "$CHECK_INTERVAL"
done
```

### Puppet Monitoring Manifest
```puppet
# monitoring.pp
class apache_monitoring {
  # Install monitoring tools
  package { ['htop', 'iotop', 'strace']:
    ensure => installed,
  }

  # Create monitoring script
  file { '/usr/local/bin/monitor_apache.sh':
    ensure  => file,
    mode    => '0755',
    content => template('monitoring/apache_monitor.sh.erb'),
  }

  # Setup cron job for monitoring
  cron { 'apache_monitoring':
    command => '/usr/local/bin/monitor_apache.sh',
    user    => 'root',
    minute  => '*/5',
  }

  # Logrotate for Apache logs
  file { '/etc/logrotate.d/apache_custom':
    ensure  => file,
    content => template('monitoring/apache_logrotate.erb'),
  }
}
```

## ✅ Requirements

- Ubuntu 14.04/16.04 LTS
- Apache 2.4 or later
- PHP 5.6 or later
- MySQL 5.7 or later
- Puppet 3.4 or later
- Understanding of LAMP stack architecture
- Basic knowledge of system administration

## 🎓 Resources

- [Apache HTTP Server Documentation](https://httpd.apache.org/docs/)
- [Puppet Documentation](https://puppet.com/docs/)
- [WordPress Debugging](https://wordpress.org/support/article/debugging-in-wordpress/)
- [Linux System Debugging](https://www.brendangregg.com/linuxperf.html)
- [strace Tutorial](https://strace.io/)
- [Apache Performance Tuning](https://httpd.apache.org/docs/2.4/misc/perf-tuning.html)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
