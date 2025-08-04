# 0x1B. Web Stack Debugging #4

![Debugging](https://img.shields.io/badge/Debugging-Advanced-red)
![Performance](https://img.shields.io/badge/Performance-Optimization-blue)
![Nginx](https://img.shields.io/badge/Nginx-Tuning-green)
![Load Testing](https://img.shields.io/badge/Load-Testing-orange)

## 📋 Description

This advanced web stack debugging project focuses on performance optimization and high-load scenarios. You'll learn to diagnose and fix performance bottlenecks, optimize server configurations for high traffic, implement load testing strategies, and ensure web applications can handle thousands of concurrent requests efficiently.

## 🎯 Learning Objectives

By the end of this project, you should be able to:

- Diagnose performance bottlenecks in web applications
- Optimize Nginx configuration for high-traffic scenarios
- Implement effective load testing strategies
- Handle file descriptor limits and system resource constraints
- Configure web servers for optimal performance under load
- Monitor and analyze system performance metrics
- Implement caching strategies for improved performance
- Debug memory and CPU usage issues
- Optimize database connections and queries
- Implement horizontal and vertical scaling strategies

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-the_sky_is_the_limit_not.pp` | Puppet manifest that fixes Nginx configuration to handle high load |
| `1-user_limit.pp` | Puppet manifest that optimizes system limits for the holberton user |

## 🚀 Performance Debugging Fundamentals

### Understanding Web Performance Bottlenecks

#### Common Performance Issues
- **High Response Times**: Slow server processing
- **Connection Timeouts**: Server unable to handle connections
- **Memory Leaks**: Applications consuming excessive memory
- **CPU Saturation**: Processor overutilization
- **I/O Bottlenecks**: Disk or network limitations
- **Database Slowdowns**: Inefficient queries or connections

#### Performance Metrics to Monitor
```bash
# CPU Usage
top -bn1 | grep "Cpu(s)"
vmstat 1 5

# Memory Usage
free -h
cat /proc/meminfo

# Network Connections
netstat -an | grep :80 | wc -l
ss -tuln

# Disk I/O
iotop -ao1
iostat -x 1
```

## 🔧 Nginx Performance Optimization

### Basic Nginx Performance Configuration
```nginx
# /etc/nginx/nginx.conf
user nginx;
worker_processes auto;
worker_cpu_affinity auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}

http {
    # Basic optimizations
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 1000;
    
    # Buffer sizes
    client_body_buffer_size 128k;
    client_max_body_size 10m;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 4k;
    output_buffers 1 32k;
    postpone_output 1460;
    
    # Timeouts
    client_header_timeout 3m;
    client_body_timeout 3m;
    send_timeout 3m;
    
    # Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/x-javascript
        application/javascript
        application/xml+rss
        application/json;
}
```

### Advanced Nginx Tuning
```nginx
# Advanced performance configuration
http {
    # Connection optimization
    upstream backend {
        least_conn;
        server 127.0.0.1:8080 max_fails=3 fail_timeout=30s;
        server 127.0.0.1:8081 max_fails=3 fail_timeout=30s;
        keepalive 32;
    }
    
    # Caching configuration
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m 
                     max_size=10g inactive=60m use_temp_path=off;
    
    server {
        listen 80;
        
        # Static file caching
        location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
            access_log off;
        }
        
        # Dynamic content caching
        location / {
            proxy_pass http://backend;
            proxy_cache my_cache;
            proxy_cache_valid 200 302 10m;
            proxy_cache_valid 404 1m;
            proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
            proxy_cache_lock on;
            
            # Headers
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

## 🛠️ Puppet Automation for Performance Fixes

### Nginx Performance Optimization Manifest
```puppet
# 0-the_sky_is_the_limit_not.pp
# Optimize Nginx configuration for high load

# Increase file descriptor limits
file { '/etc/security/limits.conf':
  ensure  => file,
  content => "
* soft nofile 65536
* hard nofile 65536
nginx soft nofile 65536
nginx hard nofile 65536
root soft nofile 65536
root hard nofile 65536
",
}

# Optimize Nginx configuration
file { '/etc/nginx/nginx.conf':
  ensure  => file,
  content => template('nginx/nginx_optimized.conf.erb'),
  notify  => Service['nginx'],
}

# Increase worker_rlimit_nofile in default config
file_line { 'nginx_worker_rlimit_nofile':
  path  => '/etc/nginx/nginx.conf',
  line  => 'worker_rlimit_nofile 65535;',
  match => '^worker_rlimit_nofile',
  notify => Service['nginx'],
}

# Optimize worker_connections
file_line { 'nginx_worker_connections':
  path  => '/etc/nginx/nginx.conf',
  line  => '    worker_connections 4096;',
  match => '^\s*worker_connections',
  notify => Service['nginx'],
}

# Ensure nginx service is running
service { 'nginx':
  ensure => running,
  enable => true,
}

# Restart nginx to apply changes
exec { 'restart-nginx':
  command     => '/usr/sbin/service nginx restart',
  refreshonly => true,
  subscribe   => File['/etc/nginx/nginx.conf'],
}
```

### System Limits Optimization Manifest
```puppet
# 1-user_limit.pp
# Optimize system limits for holberton user

# Increase file descriptor limits for holberton user
file_line { 'holberton_soft_nofile':
  path => '/etc/security/limits.conf',
  line => 'holberton soft nofile 65536',
}

file_line { 'holberton_hard_nofile':
  path => '/etc/security/limits.conf',
  line => 'holberton hard nofile 65536',
}

# Increase process limits
file_line { 'holberton_soft_nproc':
  path => '/etc/security/limits.conf',
  line => 'holberton soft nproc 8192',
}

file_line { 'holberton_hard_nproc':
  path => '/etc/security/limits.conf',
  line => 'holberton hard nproc 8192',
}

# System-wide file descriptor limit
file_line { 'fs_file_max':
  path => '/etc/sysctl.conf',
  line => 'fs.file-max = 2097152',
}

# Apply sysctl changes
exec { 'apply_sysctl':
  command     => '/sbin/sysctl -p',
  refreshonly => true,
  subscribe   => File_line['fs_file_max'],
}
```

## 📊 Load Testing and Performance Analysis

### Apache Bench (ab) Testing
```bash
# Basic load testing
ab -n 1000 -c 10 http://localhost/

# Advanced load testing with keep-alive
ab -n 10000 -c 100 -k -H "Accept-Encoding: gzip,deflate" http://localhost/

# Test with POST data
ab -n 1000 -c 50 -p data.txt -T application/x-www-form-urlencoded http://localhost/api/

# Analyze results:
# - Requests per second
# - Time per request
# - Connection Times (min/mean/max)
# - Failed requests
```

### Advanced Load Testing with wrk
```bash
# Install wrk
sudo apt install wrk

# Basic load test
wrk -t12 -c400 -d30s http://localhost/

# Custom script testing
wrk -t12 -c400 -d30s -s script.lua http://localhost/

# Example Lua script (script.lua)
cat << 'EOF' > script.lua
wrk.method = "POST"
wrk.body   = "key=value&foo=bar"
wrk.headers["Content-Type"] = "application/x-www-form-urlencoded"

function response(status, headers, body)
    if status ~= 200 then
        print("Error: " .. status)
    end
end
EOF
```

### Monitoring During Load Tests
```bash
# Real-time monitoring script
#!/bin/bash
# monitor_load_test.sh

echo "Starting load test monitoring..."
echo "Timestamp,CPU%,Memory%,Connections,LoadAvg" > load_test_metrics.csv

while true; do
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    cpu=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | sed 's/%us,//')
    memory=$(free | grep Mem | awk '{printf "%.2f", $3/$2 * 100.0}')
    connections=$(netstat -an | grep :80 | grep ESTABLISHED | wc -l)
    loadavg=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
    
    echo "$timestamp,$cpu,$memory,$connections,$loadavg" >> load_test_metrics.csv
    sleep 1
done
```

## 🔍 System Resource Optimization

### File Descriptor Limits
```bash
# Check current limits
ulimit -n
cat /proc/sys/fs/file-max

# Check per-process limits
cat /proc/$(pgrep nginx)/limits

# System-wide configuration
echo "fs.file-max = 2097152" >> /etc/sysctl.conf
sysctl -p

# Per-user limits (/etc/security/limits.conf)
nginx soft nofile 65536
nginx hard nofile 65536
* soft nofile 65536
* hard nofile 65536
```

### Memory Optimization
```bash
# Check memory usage patterns
free -h
cat /proc/meminfo | grep -E "MemTotal|MemFree|MemAvailable|Buffers|Cached"

# Monitor memory allocation
vmstat 1 10
watch -n 1 'cat /proc/meminfo | grep -E "MemFree|Buffers|Cached"'

# Optimize swap usage
echo "vm.swappiness = 10" >> /etc/sysctl.conf
echo "vm.vfs_cache_pressure = 50" >> /etc/sysctl.conf
sysctl -p
```

### Network Optimization
```bash
# TCP optimization
echo "net.core.somaxconn = 65535" >> /etc/sysctl.conf
echo "net.core.netdev_max_backlog = 5000" >> /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog = 65535" >> /etc/sysctl.conf
echo "net.ipv4.tcp_fin_timeout = 10" >> /etc/sysctl.conf
echo "net.ipv4.tcp_keepalive_time = 600" >> /etc/sysctl.conf
echo "net.ipv4.tcp_keepalive_intvl = 60" >> /etc/sysctl.conf
echo "net.ipv4.tcp_keepalive_probes = 3" >> /etc/sysctl.conf

sysctl -p
```

## 📈 Application Performance Monitoring

### Real-time Performance Dashboard
```bash
#!/bin/bash
# performance_dashboard.sh

clear
while true; do
    clear
    echo "=== Web Server Performance Dashboard ==="
    echo "Time: $(date)"
    echo ""
    
    # System Load
    echo "=== System Load ==="
    uptime
    echo ""
    
    # CPU Usage
    echo "=== CPU Usage ==="
    top -bn1 | grep "Cpu(s)"
    echo ""
    
    # Memory Usage
    echo "=== Memory Usage ==="
    free -h
    echo ""
    
    # Network Connections
    echo "=== Network Connections ==="
    echo "Total connections: $(netstat -an | grep :80 | wc -l)"
    echo "Established: $(netstat -an | grep :80 | grep ESTABLISHED | wc -l)"
    echo "Time_Wait: $(netstat -an | grep :80 | grep TIME_WAIT | wc -l)"
    echo ""
    
    # Nginx Status
    echo "=== Nginx Status ==="
    if systemctl is-active --quiet nginx; then
        echo "Status: Running"
        echo "Workers: $(ps aux | grep 'nginx: worker' | grep -v grep | wc -l)"
    else
        echo "Status: Not Running"
    fi
    echo ""
    
    # Recent Errors
    echo "=== Recent Errors (last 5 minutes) ==="
    journalctl -u nginx --since "5 minutes ago" | grep -i error | tail -3
    
    sleep 5
done
```

### Automated Performance Alerts
```bash
#!/bin/bash
# performance_alerts.sh

ALERT_EMAIL="admin@example.com"
CPU_THRESHOLD=80
MEMORY_THRESHOLD=85
CONNECTION_THRESHOLD=1000

check_cpu() {
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | sed 's/%us,//' | cut -d'%' -f1)
    if (( $(echo "$cpu_usage > $CPU_THRESHOLD" | bc -l) )); then
        echo "HIGH CPU ALERT: $cpu_usage%" | mail -s "CPU Alert" $ALERT_EMAIL
    fi
}

check_memory() {
    memory_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
    if [ "$memory_usage" -gt "$MEMORY_THRESHOLD" ]; then
        echo "HIGH MEMORY ALERT: $memory_usage%" | mail -s "Memory Alert" $ALERT_EMAIL
    fi
}

check_connections() {
    connections=$(netstat -an | grep :80 | grep ESTABLISHED | wc -l)
    if [ "$connections" -gt "$CONNECTION_THRESHOLD" ]; then
        echo "HIGH CONNECTION COUNT: $connections" | mail -s "Connection Alert" $ALERT_EMAIL
    fi
}

# Main monitoring loop
while true; do
    check_cpu
    check_memory
    check_connections
    sleep 60
done
```

## 🔧 Database Performance Optimization

### MySQL Optimization for High Load
```sql
-- MySQL configuration optimization
SET GLOBAL innodb_buffer_pool_size = 2147483648; -- 2GB
SET GLOBAL max_connections = 500;
SET GLOBAL thread_cache_size = 50;
SET GLOBAL table_open_cache = 4000;
SET GLOBAL query_cache_size = 268435456; -- 256MB

-- Connection pooling configuration
SET GLOBAL wait_timeout = 600;
SET GLOBAL interactive_timeout = 600;
```

### Redis Caching Implementation
```bash
# Install and configure Redis
sudo apt install redis-server

# Redis configuration optimization
sudo nano /etc/redis/redis.conf
# Set: maxmemory 1gb
# Set: maxmemory-policy allkeys-lru

# Example PHP implementation
cat << 'EOF' > cache_example.php
<?php
$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

function get_cached_data($key) {
    global $redis;
    $data = $redis->get($key);
    
    if ($data === false) {
        // Data not in cache, fetch from database
        $data = fetch_from_database();
        $redis->setex($key, 3600, serialize($data)); // Cache for 1 hour
    } else {
        $data = unserialize($data);
    }
    
    return $data;
}
?>
EOF
```

## ✅ Requirements

- Ubuntu 14.04/16.04/18.04 LTS
- Nginx 1.10 or later
- Understanding of system performance concepts
- Puppet 3.4 or later
- Basic knowledge of load testing
- Understanding of Linux system limits

## 🎓 Resources

- [Nginx Performance Tuning](https://nginx.org/en/docs/beginners_guide.html)
- [Linux Performance Analysis](https://www.brendangregg.com/linuxperf.html)
- [Load Testing Best Practices](https://www.nginx.com/blog/load-testing/)
- [System Limits Configuration](https://linux.die.net/man/5/limits.conf)
- [Puppet Resource Reference](https://puppet.com/docs/puppet/latest/type.html)
- [Web Performance Optimization](https://developers.google.com/web/fundamentals/performance)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
