# 0x18. Webstack Monitoring

![Monitoring](https://img.shields.io/badge/Monitoring-Datadog-purple)
![Metrics](https://img.shields.io/badge/Metrics-Performance-blue)
![Alerting](https://img.shields.io/badge/Alerting-Real--time-green)

## 📋 Description

This project introduces web stack monitoring using Datadog, a comprehensive monitoring and analytics platform. You'll learn to set up monitoring for servers, applications, and infrastructure, create dashboards, and configure alerts for proactive system management.

## 🎯 Learning Objectives

By the end of this project, you should be able to explain:

- Why monitoring is needed
- What are the 2 main areas of monitoring
- What are access logs for a web server (such as Nginx)
- What are error logs for a web server (such as Nginx)
- How to set up monitoring with Datadog
- How to create dashboards and alerts
- What metrics to monitor for web applications
- How to track application performance and user experience

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-setup_datadog` | Script or configuration file to set up Datadog monitoring |
| `1-install_datadog_agent` | Script to install and configure the Datadog agent |
| `2-setup_mysql` | Configuration to monitor MySQL with Datadog |

## 🚀 Datadog Setup

### Account Setup

1. **Create Datadog Account**:
   ```bash
   # Sign up at https://www.datadoghq.com/
   # Get your API key from the Datadog dashboard
   ```

2. **Install Datadog Agent**:
   ```bash
   # Download and install the agent
   DD_API_KEY=your_api_key bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
   
   # Or using one-liner
   DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=your_api_key DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
   ```

3. **Verify Installation**:
   ```bash
   # Check agent status
   sudo datadog-agent status
   
   # Check agent configuration
   sudo datadog-agent configcheck
   ```

## 📊 Monitoring Areas

### 1. Infrastructure Monitoring

#### System Metrics
- **CPU Usage**: Processor utilization and load
- **Memory Usage**: RAM consumption and availability
- **Disk Usage**: Storage utilization and I/O
- **Network**: Bandwidth usage and connection status

#### Server Health
```bash
# Check system resources
htop                        # Real-time system monitor
iostat -x 1                # Disk I/O statistics
free -h                    # Memory usage
df -h                      # Disk space usage
```

### 2. Application Performance Monitoring (APM)

#### Web Server Metrics
- **Request Rate**: Requests per second
- **Response Time**: Average response latency
- **Error Rate**: 4xx/5xx HTTP errors
- **Throughput**: Data transfer rates

#### Application Metrics
- **Database Queries**: Query performance and timing
- **Cache Hit Rate**: Cache effectiveness
- **Queue Length**: Background job queues
- **User Sessions**: Active user count

## 🔍 Log Monitoring

### Web Server Logs

#### Nginx Access Logs
```bash
# Default location
tail -f /var/log/nginx/access.log

# Common log format
127.0.0.1 - - [25/Dec/2021:10:30:45 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0..."

# Parse access logs for monitoring
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr
```

#### Nginx Error Logs
```bash
# Default location
tail -f /var/log/nginx/error.log

# Error log format
2021/12/25 10:30:45 [error] 1234#0: *1 connect() failed (111: Connection refused)
```

#### Apache Logs
```bash
# Access logs
tail -f /var/log/apache2/access.log

# Error logs
tail -f /var/log/apache2/error.log
```

### Application Logs
```bash
# System logs
journalctl -f                    # Follow systemd logs
tail -f /var/log/syslog         # System messages
tail -f /var/log/auth.log       # Authentication logs

# Application-specific logs
tail -f /var/log/application.log
tail -f /var/log/mysql/error.log
```

## 📈 Datadog Agent Configuration

### Basic Configuration
```yaml
# /etc/datadog-agent/datadog.yaml
api_key: your_api_key
site: datadoghq.com
hostname: your-server-name

# Enable log collection
logs_enabled: true

# Enable process monitoring
process_config:
  enabled: "true"

# Enable network monitoring
network_config:
  enabled: true
```

### Web Server Integration

#### Nginx Monitoring
```yaml
# /etc/datadog-agent/conf.d/nginx.d/conf.yaml
init_config:

instances:
  - nginx_status_url: http://localhost/nginx_status/
    tags:
      - "instance:nginx-primary"
```

#### Nginx Status Configuration
```nginx
# Add to nginx configuration
server {
    listen 81;
    server_name localhost;
    
    location /nginx_status {
        stub_status on;
        access_log off;
        allow 127.0.0.1;
        deny all;
    }
}
```

### MySQL Monitoring
```yaml
# /etc/datadog-agent/conf.d/mysql.d/conf.yaml
init_config:

instances:
  - host: localhost
    port: 3306
    username: datadog
    password: your_password
    tags:
      - "instance:mysql-primary"
    
    options:
      replication: true
      galera_cluster: false
```

#### MySQL User for Datadog
```sql
-- Create monitoring user
CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'password';
GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost';
GRANT PROCESS ON *.* TO 'datadog'@'localhost';
GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';
FLUSH PRIVILEGES;
```

## 📊 Creating Dashboards

### Infrastructure Dashboard
```json
{
  "title": "Infrastructure Overview",
  "widgets": [
    {
      "type": "timeseries",
      "title": "CPU Usage",
      "queries": ["system.cpu.user", "system.cpu.system"]
    },
    {
      "type": "timeseries", 
      "title": "Memory Usage",
      "queries": ["system.mem.used", "system.mem.total"]
    },
    {
      "type": "timeseries",
      "title": "Disk I/O",
      "queries": ["system.io.read_bytes", "system.io.write_bytes"]
    }
  ]
}
```

### Application Dashboard
```json
{
  "title": "Web Application Performance",
  "widgets": [
    {
      "type": "query_value",
      "title": "Request Rate",
      "queries": ["nginx.net.request_per_s"]
    },
    {
      "type": "timeseries",
      "title": "Response Time",
      "queries": ["nginx.response_time"]
    },
    {
      "type": "toplist",
      "title": "Top Error Pages",
      "queries": ["nginx.error_rate by {status_code}"]
    }
  ]
}
```

## 🚨 Setting Up Alerts

### Infrastructure Alerts
```yaml
# High CPU usage alert
name: "High CPU Usage"
query: "avg(last_5m):avg:system.cpu.user{*} > 80"
message: |
  CPU usage is above 80% on {{host.name}}
  
  Current value: {{value}}%
  
  Please investigate immediately.

# Low disk space alert
name: "Low Disk Space"
query: "avg(last_5m):avg:system.disk.free{*} < 10"
message: |
  Disk space is below 10% on {{host.name}}
  
  Please clean up or add storage.
```

### Application Alerts
```yaml
# High error rate alert
name: "High Error Rate"
query: "avg(last_10m):avg:nginx.error_rate{*} > 5"
message: |
  Error rate is above 5% for {{host.name}}
  
  Current error rate: {{value}}%
  
  Check application logs for details.

# Slow response time alert
name: "Slow Response Time"
query: "avg(last_5m):avg:nginx.response_time{*} > 2"
message: |
  Response time is above 2 seconds
  
  Current response time: {{value}}s
```

## 📱 Notification Channels

### Email Notifications
```yaml
# Configure email alerts
notifications:
  - type: email
    addresses:
      - admin@company.com
      - ops-team@company.com
```

### Slack Integration
```yaml
# Slack webhook configuration
notifications:
  - type: slack
    webhook_url: "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
    channel: "#alerts"
    username: "Datadog"
```

### PagerDuty Integration
```yaml
# PagerDuty for critical alerts
notifications:
  - type: pagerduty
    service_key: "your_pagerduty_service_key"
```

## 🔧 Custom Metrics

### Application Metrics
```python
# Python application with custom metrics
from datadog import initialize, statsd

# Initialize Datadog
initialize(api_key='your_api_key', app_key='your_app_key')

# Send custom metrics
statsd.increment('web.requests.count')
statsd.histogram('web.response_time', response_time)
statsd.gauge('database.connections.active', active_connections)
```

### Shell Script Metrics
```bash
#!/bin/bash
# Send custom metrics from shell script

# Count active connections
CONNECTIONS=$(netstat -an | grep ESTABLISHED | wc -l)
curl -X POST "https://api.datadoghq.com/api/v1/series?api_key=YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d "{
  \"series\": [{
    \"metric\": \"custom.connections.active\",
    \"points\": [[$(date +%s), $CONNECTIONS]],
    \"host\": \"$(hostname)\"
  }]
}"
```

## 📋 Monitoring Checklist

### Essential Metrics to Monitor
- ✅ **System Resources**: CPU, Memory, Disk, Network
- ✅ **Web Server**: Request rate, response time, error rate
- ✅ **Database**: Query performance, connection count
- ✅ **Application**: Custom business metrics
- ✅ **Security**: Failed login attempts, suspicious activity
- ✅ **User Experience**: Page load times, user sessions

### Alert Configuration
- ✅ **Critical Alerts**: System down, high error rates
- ✅ **Warning Alerts**: Resource usage thresholds
- ✅ **Info Alerts**: Deployment notifications
- ✅ **Escalation Rules**: Progressive alert severity

## ✅ Requirements

- Ubuntu 16.04 LTS or Ubuntu 18.04 LTS
- Datadog account with valid API key
- Web server (Nginx/Apache) installed and configured
- MySQL server for database monitoring
- All configuration files must be properly formatted
- Scripts must be executable and pass shellcheck

## 🎓 Resources

- [Datadog Documentation](https://docs.datadoghq.com/)
- [Datadog Agent Installation](https://docs.datadoghq.com/agent/)
- [Nginx Monitoring with Datadog](https://docs.datadoghq.com/integrations/nginx/)
- [MySQL Monitoring with Datadog](https://docs.datadoghq.com/integrations/mysql/)
- [Creating Dashboards](https://docs.datadoghq.com/dashboards/)
- [Setting up Alerts](https://docs.datadoghq.com/monitors/)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
