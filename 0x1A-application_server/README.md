# 0x1A. Application Server

![Application Server](https://img.shields.io/badge/Application-Server-blue)
![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI-green)
![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-orange)

## 📋 Description

This project focuses on setting up and configuring an application server to serve dynamic content. You'll learn to deploy Python web applications using Gunicorn WSGI server, configure Nginx as a reverse proxy, and understand the difference between web servers and application servers.

## 🎯 Learning Objectives

By the end of this project, you should be able to explain:

- What is an application server vs a web server
- How to serve a Flask application with Gunicorn
- How to serve a Flask application with Gunicorn and Nginx
- How to configure Nginx as a reverse proxy
- How to set up upstart scripts for process management
- What is WSGI and how it works
- How to scale web applications with multiple workers

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-welcome_gunicorn-upstart_config` | Upstart configuration file for Gunicorn service |
| `1-pass_parameter-upstart_config` | Upstart config for Flask app with URL parameters |
| `2-app_server-nginx_config` | Nginx configuration for application server setup |
| `3-app_server-nginx_config` | Enhanced Nginx config with static files handling |
| `4-app_server-nginx_config` | Complete Nginx configuration for production |
| `5-app_server-nginx_config` | Final Nginx config with all routes configured |

## 🏗️ Architecture Overview

### Web Server vs Application Server

#### Web Server (Nginx)
- **Purpose**: Handle HTTP requests, serve static content
- **Capabilities**:
  - Static file serving (HTML, CSS, JS, images)
  - SSL/TLS termination
  - Load balancing
  - Reverse proxying
  - Caching

#### Application Server (Gunicorn)
- **Purpose**: Execute application code, serve dynamic content
- **Capabilities**:
  - Run Python WSGI applications
  - Process business logic
  - Database connections
  - Session management
  - Background task processing

### Request Flow
```
Client Request → Nginx (Web Server) → Gunicorn (App Server) → Flask Application
                     ↓
               Static Files (CSS, JS, Images)
```

## 🚀 Flask Application Setup

### Sample Flask Application
```python
# app.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'

@app.route('/airbnb-onepage/')
def airbnb_onepage():
    return '<h1>Welcome to AirBnB Clone!</h1>'

@app.route('/airbnb-dynamic/number_odd_or_even/<int:n>')
def number_odd_or_even(n):
    if n % 2 == 0:
        result = "even"
    else:
        result = "odd"
    return f'<h1>Number: {n} is {result}</h1>'

@app.route('/api/v1/stats')
def api_stats():
    return {'status': 'OK', 'users': 100, 'places': 50}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Development Server
```bash
# Run Flask development server
python3 app.py

# Test the application
curl http://localhost:5000/
curl http://localhost:5000/airbnb-onepage/
curl http://localhost:5000/airbnb-dynamic/number_odd_or_even/42
```

## 🔧 Gunicorn Configuration

### Installing Gunicorn
```bash
# Install Gunicorn
pip3 install gunicorn

# Install Flask (if not already installed)
pip3 install flask
```

### Basic Gunicorn Usage
```bash
# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 app:app

# Run with multiple workers
gunicorn --bind 0.0.0.0:5000 --workers 3 app:app

# Run in background
gunicorn --bind 0.0.0.0:5000 --workers 3 --daemon app:app

# Run with custom configuration
gunicorn -c gunicorn_config.py app:app
```

### Gunicorn Configuration File
```python
# gunicorn_config.py
bind = "0.0.0.0:5000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 5
preload_app = True
daemon = False
user = "ubuntu"
group = "ubuntu"
tmp_upload_dir = None
logfile = "/var/log/gunicorn/gunicorn.log"
loglevel = "info"
access_logfile = "/var/log/gunicorn/access.log"
error_logfile = "/var/log/gunicorn/error.log"
```

## 📋 Upstart Configuration

### Basic Upstart Script
```bash
# /etc/init/gunicorn-flask.conf
description "Gunicorn Flask Application"
start on runlevel [2345]
stop on runlevel [!2345]

respawn
setuid ubuntu
setgid ubuntu
chdir /home/ubuntu/AirBnB_clone_v2

env PATH=/usr/local/bin:/usr/bin:/bin
env PYTHONPATH=/home/ubuntu/AirBnB_clone_v2

exec gunicorn --bind 0.0.0.0:5000 --workers 3 web_flask.0-hello_route:app
```

### Enhanced Upstart Script
```bash
# /etc/init/gunicorn-airbnb.conf
description "Gunicorn application server handling AirBnB clone"

start on filesystem or runlevel [2345]
stop on shutdown

respawn
respawn limit 5 10

setuid ubuntu
setgid ubuntu

env PATH=/usr/local/bin:/usr/bin:/bin
env PYTHONPATH=/home/ubuntu/AirBnB_clone_v2

chdir /home/ubuntu/AirBnB_clone_v2

pre-start script
    echo "[`date`] Starting Gunicorn" >> /var/log/gunicorn.log
end script

exec gunicorn --config /home/ubuntu/gunicorn.conf.py web_flask.6-number_odd_or_even:app

pre-stop script
    echo "[`date`] Stopping Gunicorn" >> /var/log/gunicorn.log
end script
```

### Managing Upstart Services
```bash
# Start service
sudo start gunicorn-flask

# Stop service
sudo stop gunicorn-flask

# Restart service
sudo restart gunicorn-flask

# Check status
sudo status gunicorn-flask

# View logs
tail -f /var/log/upstart/gunicorn-flask.log
```

## 🌐 Nginx Configuration

### Basic Reverse Proxy
```nginx
# /etc/nginx/sites-available/default
server {
    listen 80;
    server_name localhost;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Advanced Configuration with Static Files
```nginx
# /etc/nginx/sites-available/airbnb
server {
    listen 80;
    server_name your_domain.com;
    
    # Serve static files directly
    location /static/ {
        alias /home/ubuntu/AirBnB_clone_v2/web_flask/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # API routes
    location /api/ {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Application routes
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Specific route configurations
    location /airbnb-onepage/ {
        proxy_pass http://127.0.0.1:5000/airbnb-onepage/;
    }
    
    location ~ /airbnb-dynamic/number_odd_or_even/(\d+)$ {
        proxy_pass http://127.0.0.1:5000/airbnb-dynamic/number_odd_or_even/$1;
    }
    
    # Error pages
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```

### Load Balancing Configuration
```nginx
# /etc/nginx/sites-available/load-balanced
upstream app_servers {
    server 127.0.0.1:5000 weight=1;
    server 127.0.0.1:5001 weight=1;
    server 127.0.0.1:5002 weight=1;
}

server {
    listen 80;
    server_name your_domain.com;
    
    location / {
        proxy_pass http://app_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Health checks
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
    }
}
```

## 🔄 Process Management

### Systemd Service (Modern Alternative)
```ini
# /etc/systemd/system/gunicorn.service
[Unit]
Description=Gunicorn instance to serve Flask App
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/AirBnB_clone_v2
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 web_flask.0-hello_route:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### Systemd Commands
```bash
# Enable service
sudo systemctl enable gunicorn

# Start service
sudo systemctl start gunicorn

# Check status
sudo systemctl status gunicorn

# View logs
sudo journalctl -u gunicorn -f

# Reload configuration
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

## 📊 Performance Optimization

### Gunicorn Tuning
```python
# Performance-oriented configuration
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"  # For I/O intensive apps
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True
timeout = 30
keepalive = 5
```

### Nginx Optimization
```nginx
# Performance optimizations
worker_processes auto;
worker_connections 1024;

http {
    # Enable gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript;
    
    # Enable caching
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=app_cache:10m inactive=60m;
    
    # Connection optimizations
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
}
```

## 🐛 Debugging and Troubleshooting

### Common Issues

#### Gunicorn Not Starting
```bash
# Check configuration
gunicorn --check-config app:app

# Run in foreground for debugging
gunicorn --bind 0.0.0.0:5000 app:app

# Check logs
tail -f /var/log/gunicorn/error.log
```

#### Nginx Configuration Errors
```bash
# Test configuration
sudo nginx -t

# Reload configuration
sudo nginx -s reload

# Check error logs
tail -f /var/log/nginx/error.log
```

#### Application Errors
```bash
# Check application logs
tail -f /var/log/gunicorn/access.log
tail -f /var/log/gunicorn/error.log

# Test direct access to app server
curl http://localhost:5000/

# Check process status
ps aux | grep gunicorn
netstat -tlnp | grep :5000
```

## 🔒 Security Considerations

### Application Security
```python
# Security headers in Flask
from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, force_https=False)  # Enable HTTPS in production

@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

### Nginx Security
```nginx
# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;

# Hide server information
server_tokens off;

# Rate limiting
limit_req_zone $binary_remote_addr zone=app:10m rate=10r/s;
limit_req zone=app burst=20 nodelay;
```

## ✅ Requirements

- Ubuntu 16.04 LTS
- Python 3.5 or higher
- Flask application
- Gunicorn WSGI server
- Nginx web server
- All configuration files must be properly formatted
- Services must start automatically on boot

## 🎓 Resources

- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [WSGI Specification](https://wsgi.readthedocs.io/)
- [Upstart Documentation](http://upstart.ubuntu.com/)
- [Systemd Documentation](https://systemd.io/)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
