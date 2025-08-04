# 0x0F. Load Balancer

![Load Balancer](https://img.shields.io/badge/Load-Balancer-blue)
![HAProxy](https://img.shields.io/badge/HAProxy-High%20Availability-green)
![Nginx](https://img.shields.io/badge/Nginx-Load%20Balancing-orange)
![Scaling](https://img.shields.io/badge/Scaling-Horizontal-red)

## 📋 Description

This project focuses on implementing load balancing solutions to distribute traffic across multiple servers, ensuring high availability and improved performance. You'll learn to configure HAProxy and Nginx as load balancers, implement different balancing algorithms, handle server failures gracefully, and design scalable web infrastructure.

## 🎯 Learning Objectives

By the end of this project, you should be able to:

- Understand the concept and importance of load balancing
- Configure HAProxy for load balancing and high availability
- Implement different load balancing algorithms
- Set up health checks and failover mechanisms
- Configure SSL termination at the load balancer level
- Monitor load balancer performance and traffic distribution
- Implement session persistence and sticky sessions
- Design horizontally scalable web architectures
- Handle server maintenance without service interruption
- Optimize load balancer configuration for performance

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-custom_http_response_header` | Bash script that configures Nginx to add custom HTTP response header |
| `1-install_load_balancer` | Bash script that installs and configures HAProxy load balancer |
| `2-puppet_custom_http_response_header.pp` | Puppet manifest for custom HTTP header configuration |

## ⚖️ Load Balancing Fundamentals

### What is Load Balancing?

Load balancing is the process of distributing incoming network traffic across multiple servers to ensure:
- **High Availability**: Service continues even if servers fail
- **Scalability**: Handle increased traffic by adding more servers
- **Performance**: Distribute load to prevent server overload
- **Reliability**: Reduce single points of failure

### Load Balancing Algorithms

#### Round Robin
```
Request 1 → Server A
Request 2 → Server B  
Request 3 → Server C
Request 4 → Server A (cycle repeats)
```

#### Weighted Round Robin
```
Server A (weight: 3) → Gets 3 requests
Server B (weight: 2) → Gets 2 requests  
Server C (weight: 1) → Gets 1 request
```

#### Least Connections
```
Server A: 5 active connections
Server B: 3 active connections ← Next request goes here
Server C: 7 active connections
```

#### IP Hash
```
hash(client_ip) % server_count = target_server
Ensures same client always goes to same server
```

## 🔧 Nginx Load Balancer Configuration

### Basic Nginx Load Balancing
```nginx
# /etc/nginx/sites-available/load_balancer
upstream backend_servers {
    server 10.0.1.4:80;
    server 10.0.1.5:80;
    server 10.0.1.6:80;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Advanced Nginx Configuration
```nginx
# Advanced load balancing with health checks
upstream backend_servers {
    least_conn;  # Use least connections algorithm
    
    server 10.0.1.4:80 weight=3 max_fails=3 fail_timeout=30s;
    server 10.0.1.5:80 weight=2 max_fails=3 fail_timeout=30s;
    server 10.0.1.6:80 weight=1 max_fails=3 fail_timeout=30s backup;
    
    keepalive 32;  # Connection pooling
}

server {
    listen 80;
    server_name example.com;
    
    # Custom response header
    add_header X-Served-By $hostname;
    
    location / {
        proxy_pass http://backend_servers;
        
        # Proxy settings
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Connection settings
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # Buffer settings
        proxy_buffering on;
        proxy_buffer_size 128k;
        proxy_buffers 4 256k;
        proxy_busy_buffers_size 256k;
    }
    
    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

### Custom HTTP Response Header Script
```bash
#!/usr/bin/env bash
# 0-custom_http_response_header
# Configure Nginx to add custom HTTP response header

# Update package list
sudo apt-get update

# Install Nginx if not already installed
sudo apt-get install -y nginx

# Get hostname for header value
hostname=$(hostname)

# Configure custom header in default site
sudo tee /etc/nginx/sites-available/default > /dev/null <<EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    
    server_name _;
    
    # Add custom header
    add_header X-Served-By $hostname;
    
    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF

# Test Nginx configuration
sudo nginx -t

# Restart Nginx to apply changes
sudo systemctl restart nginx

# Enable Nginx to start on boot
sudo systemctl enable nginx

echo "Nginx configured with custom header X-Served-By: $hostname"
```

## ⚡ HAProxy Load Balancer Configuration

### Basic HAProxy Setup
```bash
#!/usr/bin/env bash
# 1-install_load_balancer
# Install and configure HAProxy load balancer

# Update package list
sudo apt-get update

# Install HAProxy
sudo apt-get install -y haproxy

# Enable HAProxy service
sudo systemctl enable haproxy

# Configure HAProxy
sudo tee /etc/haproxy/haproxy.cfg > /dev/null <<EOF
global
    daemon
    maxconn 2048

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms
    option httplog
    option dontlognull

frontend web_frontend
    bind *:80
    default_backend web_servers

backend web_servers
    balance roundrobin
    option httpchk GET /
    server web-01 10.0.1.4:80 check
    server web-02 10.0.1.5:80 check
EOF

# Test HAProxy configuration
sudo haproxy -c -f /etc/haproxy/haproxy.cfg

# Start HAProxy service
sudo systemctl restart haproxy

echo "HAProxy load balancer configured and started"
```

### Advanced HAProxy Configuration
```bash
# /etc/haproxy/haproxy.cfg
global
    daemon
    maxconn 4096
    log stdout local0
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy

defaults
    mode http
    log global
    option httplog
    option dontlognull
    option log-health-checks
    option forwardfor
    option http-server-close
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms
    errorfile 400 /etc/haproxy/errors/400.http
    errorfile 403 /etc/haproxy/errors/403.http
    errorfile 408 /etc/haproxy/errors/408.http
    errorfile 500 /etc/haproxy/errors/500.http
    errorfile 502 /etc/haproxy/errors/502.http
    errorfile 503 /etc/haproxy/errors/503.http
    errorfile 504 /etc/haproxy/errors/504.http

# Statistics interface
frontend stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 30s
    stats admin if TRUE

# Main frontend
frontend web_frontend
    bind *:80
    bind *:443 ssl crt /etc/ssl/certs/example.com.pem
    
    # Redirect HTTP to HTTPS
    redirect scheme https if !{ ssl_fc }
    
    # Custom headers
    http-response set-header X-Served-By %[env(HOSTNAME)]
    
    default_backend web_servers

# Backend servers
backend web_servers
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200
    
    # Cookie-based session persistence
    cookie SERVERID insert indirect nocache
    
    server web-01 10.0.1.4:80 check cookie web-01 maxconn 100
    server web-02 10.0.1.5:80 check cookie web-02 maxconn 100
    server web-03 10.0.1.6:80 check cookie web-03 maxconn 100 backup
```

## 🔧 Puppet Automation

### Puppet Manifest for Custom Headers
```puppet
# 2-puppet_custom_http_response_header.pp
# Configure Nginx with custom HTTP response header using Puppet

# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Configure Nginx with custom header
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => "
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    
    server_name _;
    
    # Add custom header with hostname
    add_header X-Served-By \$hostname;
    
    location / {
        try_files \$uri \$uri/ =404;
    }
}
",
  notify  => Service['nginx'],
  require => Package['nginx'],
}

# Ensure Nginx service is running
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => Package['nginx'],
}

# Restart Nginx when configuration changes
exec { 'nginx-reload':
  command     => '/usr/sbin/service nginx reload',
  refreshonly => true,
  subscribe   => File['/etc/nginx/sites-available/default'],
}
```

### Advanced Puppet Load Balancer Configuration
```puppet
# Advanced HAProxy configuration with Puppet
class loadbalancer {
  # Install HAProxy
  package { 'haproxy':
    ensure => installed,
  }

  # Configure HAProxy
  file { '/etc/haproxy/haproxy.cfg':
    ensure  => file,
    content => template('loadbalancer/haproxy.cfg.erb'),
    notify  => Service['haproxy'],
    require => Package['haproxy'],
  }

  # Enable HAProxy service
  service { 'haproxy':
    ensure  => running,
    enable  => true,
    require => Package['haproxy'],
  }

  # Configure firewall for load balancer
  firewall { '100 allow http':
    dport  => 80,
    proto  => tcp,
    action => accept,
  }

  firewall { '101 allow https':
    dport  => 443,
    proto  => tcp,
    action => accept,
  }

  firewall { '102 allow stats':
    dport  => 8404,
    proto  => tcp,
    action => accept,
  }
}
```

## 📊 Load Balancer Monitoring and Health Checks

### Health Check Implementation
```bash
#!/bin/bash
# health_check.sh - Monitor backend server health

SERVERS=("10.0.1.4" "10.0.1.5" "10.0.1.6")
LOG_FILE="/var/log/health_check.log"

check_server_health() {
    local server=$1
    local response_code=$(curl -s -o /dev/null -w "%{http_code}" "http://$server/health" --connect-timeout 5)
    
    if [ "$response_code" = "200" ]; then
        echo "$(date): Server $server is healthy" >> $LOG_FILE
        return 0
    else
        echo "$(date): Server $server is unhealthy (HTTP $response_code)" >> $LOG_FILE
        return 1
    fi
}

# Check all servers
for server in "${SERVERS[@]}"; do
    if check_server_health "$server"; then
        echo "✓ $server is healthy"
    else
        echo "✗ $server is unhealthy"
        # Send alert (email, Slack, etc.)
        # Remove from load balancer if needed
    fi
done
```

### HAProxy Statistics and Monitoring
```bash
# HAProxy stats API usage
# Get stats in CSV format
curl "http://localhost:8404/stats;csv"

# Get specific server stats
curl "http://localhost:8404/stats;csv" | grep "web-01"

# Enable/disable server via stats interface
# Disable server: PUT http://localhost:8404/stats with "s=web-01&action=disable"
# Enable server: PUT http://localhost:8404/stats with "s=web-01&action=enable"

# Monitor HAProxy logs
tail -f /var/log/haproxy.log

# Check HAProxy status
systemctl status haproxy
```

### Load Balancer Performance Monitoring
```bash
#!/bin/bash
# monitor_load_balancer.sh

echo "Load Balancer Performance Monitor"
echo "================================="

while true; do
    clear
    echo "Time: $(date)"
    echo ""
    
    # HAProxy process status
    echo "HAProxy Status:"
    systemctl is-active haproxy
    echo ""
    
    # Connection statistics
    echo "Connection Statistics:"
    netstat -an | grep :80 | awk '{print $6}' | sort | uniq -c
    echo ""
    
    # Backend server response times
    echo "Backend Server Response Times:"
    for server in 10.0.1.4 10.0.1.5 10.0.1.6; do
        response_time=$(curl -o /dev/null -s -w "%{time_total}" "http://$server/health")
        echo "Server $server: ${response_time}s"
    done
    echo ""
    
    # Current load distribution (from HAProxy stats)
    echo "Load Distribution:"
    curl -s "http://localhost:8404/stats;csv" | grep "web-" | \
    awk -F',' '{print $2 ": " $9 " sessions, " $8 " total"}'
    
    sleep 5
done
```

## 🔒 SSL Termination and Security

### SSL Configuration at Load Balancer
```bash
# Generate SSL certificate (Let's Encrypt example)
sudo certbot certonly --standalone -d example.com

# Combine certificate for HAProxy
sudo cat /etc/letsencrypt/live/example.com/fullchain.pem \
         /etc/letsencrypt/live/example.com/privkey.pem > \
         /etc/ssl/certs/example.com.pem

# HAProxy SSL configuration
frontend web_frontend
    bind *:80
    bind *:443 ssl crt /etc/ssl/certs/example.com.pem
    
    # Security headers
    http-response set-header Strict-Transport-Security "max-age=31536000; includeSubDomains"
    http-response set-header X-Frame-Options "DENY"
    http-response set-header X-Content-Type-Options "nosniff"
    
    # Redirect HTTP to HTTPS
    redirect scheme https if !{ ssl_fc }
    
    default_backend web_servers
```

### Security Best Practices
```bash
# Configure firewall for load balancer
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw allow 8404/tcp # HAProxy stats (restrict to admin IPs)
sudo ufw enable

# Harden HAProxy configuration
# /etc/haproxy/haproxy.cfg additions:
global
    # Security settings
    tune.ssl.default-dh-param 2048
    ssl-default-bind-options no-sslv3 no-tlsv10 no-tlsv11
    ssl-default-bind-ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384

# Rate limiting
frontend web_frontend
    # Limit request rate
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny if { sc_http_req_rate(0) gt 20 }
```

## 🚀 Advanced Load Balancing Patterns

### Session Persistence (Sticky Sessions)
```bash
# Cookie-based session persistence
backend web_servers
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server web-01 10.0.1.4:80 check cookie web-01
    server web-02 10.0.1.5:80 check cookie web-02

# IP-based session persistence
backend web_servers
    balance source
    server web-01 10.0.1.4:80 check
    server web-02 10.0.1.5:80 check
```

### Blue-Green Deployment with Load Balancer
```bash
# Blue-Green deployment script
#!/bin/bash
# blue_green_deploy.sh

BLUE_SERVERS=("10.0.1.4" "10.0.1.5")
GREEN_SERVERS=("10.0.1.6" "10.0.1.7")
CURRENT_ENV="blue"

deploy_to_green() {
    echo "Deploying to green environment..."
    for server in "${GREEN_SERVERS[@]}"; do
        # Deploy application to green servers
        ssh root@$server "cd /app && git pull && systemctl restart app"
    done
}

switch_to_green() {
    echo "Switching traffic to green environment..."
    # Update HAProxy configuration to point to green servers
    sed -i 's/10.0.1.4/10.0.1.6/g; s/10.0.1.5/10.0.1.7/g' /etc/haproxy/haproxy.cfg
    systemctl reload haproxy
}

# Execute deployment
deploy_to_green
switch_to_green
echo "Deployment complete. Traffic switched to green environment."
```

## 📈 Scaling and Performance Optimization

### Auto-scaling with Load Balancer
```bash
#!/bin/bash
# auto_scale.sh - Simple auto-scaling based on load

MAX_SERVERS=10
MIN_SERVERS=2
SCALE_UP_THRESHOLD=80
SCALE_DOWN_THRESHOLD=30

get_current_load() {
    # Get average CPU usage across all backend servers
    uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//'
}

scale_up() {
    echo "Scaling up - adding new server"
    # Launch new instance and add to load balancer
    # This would integrate with cloud provider APIs
}

scale_down() {
    echo "Scaling down - removing server"
    # Remove server from load balancer and terminate instance
}

# Monitor and scale
current_load=$(get_current_load)
if (( $(echo "$current_load > $SCALE_UP_THRESHOLD" | bc -l) )); then
    scale_up
elif (( $(echo "$current_load < $SCALE_DOWN_THRESHOLD" | bc -l) )); then
    scale_down
fi
```

### Performance Tuning
```bash
# System-level optimizations for load balancer
echo "net.core.somaxconn = 65535" >> /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog = 65535" >> /etc/sysctl.conf
echo "net.core.netdev_max_backlog = 5000" >> /etc/sysctl.conf
echo "net.ipv4.tcp_fin_timeout = 10" >> /etc/sysctl.conf

sysctl -p

# HAProxy performance tuning
global
    maxconn 40000
    tune.bufsize 32768
    tune.maxrewrite 8192
    tune.rcvbuf.client 262144
    tune.rcvbuf.server 262144
    tune.sndbuf.client 262144
    tune.sndbuf.server 262144
```

## ✅ Requirements

- Ubuntu 16.04 LTS
- HAProxy 1.6 or later
- Nginx 1.10 or later
- Understanding of HTTP protocols
- Basic networking knowledge
- Puppet 3.4 or later (for automation tasks)

## 🎓 Resources

- [HAProxy Documentation](http://www.haproxy.org/#docs)
- [Nginx Load Balancing](https://nginx.org/en/docs/http/load_balancing.html)
- [Load Balancing Concepts](https://www.nginx.com/resources/glossary/load-balancing/)
- [High Availability Architecture](https://aws.amazon.com/architecture/well-architected/)
- [SSL/TLS Best Practices](https://wiki.mozilla.org/Security/Server_Side_TLS)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*