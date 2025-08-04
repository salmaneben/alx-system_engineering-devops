# 0x10. HTTPS SSL

![HTTPS](https://img.shields.io/badge/HTTPS-SSL%2FTLS-green)
![Security](https://img.shields.io/badge/Security-Encryption-blue)
![Certificates](https://img.shields.io/badge/Certificates-Let's%20Encrypt-orange)

## 📋 Description

This project focuses on HTTPS implementation and SSL/TLS security. You'll learn about the importance of HTTPS, how SSL certificates work, and how to configure secure web servers using Let's Encrypt certificates and HAProxy SSL termination for enhanced security and performance.

## 🎯 Learning Objectives

By the end of this project, you should be able to explain:

- What is HTTPS SSL and its 2 main roles
- What is the purpose of encrypting traffic
- What SSL termination means
- How to configure HAProxy with SSL termination
- How to obtain and configure SSL certificates
- What are the main elements that SSL is providing
- How to implement SSL/TLS best practices

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-world_wide_web` | Bash script that displays information about subdomains and their DNS records |
| `1-haproxy_ssl_termination` | HAProxy configuration file that accepts encrypted traffic for subdomain www |
| `100-redirect_http_to_https` | HAProxy configuration that automatically redirects HTTP traffic to HTTPS |

## 🔒 HTTPS and SSL/TLS Fundamentals

### What is HTTPS?
HTTPS (HyperText Transfer Protocol Secure) is the secure version of HTTP that uses SSL/TLS encryption to protect data transmission between client and server.

### SSL/TLS Main Roles
1. **Authentication**: Verify the identity of the server
2. **Encryption**: Protect data confidentiality during transmission

### Why HTTPS is Important
- **Data Protection**: Prevents eavesdropping and data theft
- **Integrity**: Ensures data hasn't been tampered with
- **Authentication**: Confirms you're communicating with the intended server
- **SEO Benefits**: Search engines favor HTTPS sites
- **User Trust**: Browsers mark HTTP sites as "Not Secure"
- **Compliance**: Required for handling sensitive data (PCI DSS, GDPR)

## 🌐 Domain and Subdomain Configuration

### DNS Records for Web Infrastructure

#### A Records (Address Records)
```bash
# Check A record for domain
dig domain.com A

# Expected output format:
# domain.com.  300  IN  A  IP_ADDRESS
```

#### Subdomain Configuration
Common subdomains for web infrastructure:
- `www` - Main website
- `lb-01` - Load balancer
- `web-01` - Web server 1
- `web-02` - Web server 2

### Bash Script for Domain Information
```bash
#!/usr/bin/env bash
# 0-world_wide_web - displays subdomain information

domain=$1
subdomain=$2

get_subdomain_info() {
    local sub=$1
    local dom=$2
    local record_info
    
    record_info=$(dig "${sub}.${dom}" | grep -A1 'ANSWER SECTION:' | tail -1)
    record_type=$(echo "$record_info" | awk '{print $4}')
    destination=$(echo "$record_info" | awk '{print $5}')
    
    echo "The subdomain $sub is a $record_type record and points to $destination"
}

if [ -z "$subdomain" ]; then
    # Check default subdomains
    for sub in www lb-01 web-01 web-02; do
        get_subdomain_info "$sub" "$domain"
    done
else
    get_subdomain_info "$subdomain" "$domain"
fi
```

## 🔧 SSL Certificate Management

### Let's Encrypt with Certbot

#### Installation
```bash
# Install Certbot
sudo apt update
sudo apt install certbot

# Install nginx plugin (if using nginx)
sudo apt install python3-certbot-nginx

# Install apache plugin (if using apache)
sudo apt install python3-certbot-apache
```

#### Obtaining Certificates
```bash
# Get certificate for domain
sudo certbot certonly --standalone -d domain.com -d www.domain.com

# Using nginx plugin
sudo certbot --nginx -d domain.com -d www.domain.com

# Using webroot method
sudo certbot certonly --webroot -w /var/www/html -d domain.com
```

#### Certificate Renewal
```bash
# Test renewal
sudo certbot renew --dry-run

# Set up automatic renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Certificate Locations
```bash
# Certificate files location
/etc/letsencrypt/live/domain.com/
├── cert.pem          # Server certificate
├── chain.pem         # Intermediate certificate
├── fullchain.pem     # cert.pem + chain.pem
└── privkey.pem       # Private key
```

## ⚖️ HAProxy SSL Configuration

### Basic SSL Termination
```bash
# /etc/haproxy/haproxy.cfg
global
    daemon
    maxconn 2048
    tune.ssl.default-dh-param 2048

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms
    option httplog

frontend web_frontend
    bind *:80
    bind *:443 ssl crt /etc/ssl/certs/domain.com.pem
    
    # Redirect HTTP to HTTPS
    redirect scheme https if !{ ssl_fc }
    
    default_backend web_servers

backend web_servers
    balance roundrobin
    server web-01 web-01-ip:80 check
    server web-02 web-02-ip:80 check
```

### Advanced SSL Configuration
```bash
# Enhanced security configuration
global
    daemon
    maxconn 2048
    tune.ssl.default-dh-param 2048
    ssl-default-bind-options no-sslv3 no-tlsv10 no-tlsv11
    ssl-default-bind-ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms
    option httplog
    option forwardfor
    option http-server-close

frontend https_frontend
    bind *:443 ssl crt /etc/ssl/certs/domain.com.pem
    
    # Security headers
    http-response set-header Strict-Transport-Security "max-age=31536000; includeSubDomains"
    http-response set-header X-Frame-Options "DENY"
    http-response set-header X-Content-Type-Options "nosniff"
    
    default_backend web_servers

frontend http_frontend
    bind *:80
    # Redirect all HTTP to HTTPS
    redirect scheme https code 301

backend web_servers
    balance roundrobin
    option httpchk GET /health
    server web-01 10.0.1.4:80 check
    server web-02 10.0.1.5:80 check
```

### SSL Certificate Preparation for HAProxy
```bash
# Combine certificate files for HAProxy
sudo cat /etc/letsencrypt/live/domain.com/fullchain.pem \
         /etc/letsencrypt/live/domain.com/privkey.pem > \
         /etc/ssl/certs/domain.com.pem

# Set proper permissions
sudo chmod 600 /etc/ssl/certs/domain.com.pem
sudo chown haproxy:haproxy /etc/ssl/certs/domain.com.pem
```

## 🔄 HTTP to HTTPS Redirection

### HAProxy Redirection Configuration
```bash
# Method 1: Conditional redirect
frontend web_frontend
    bind *:80
    bind *:443 ssl crt /etc/ssl/certs/domain.com.pem
    
    # Redirect HTTP to HTTPS
    redirect scheme https code 301 if !{ ssl_fc }
    
    default_backend web_servers

# Method 2: Separate frontends
frontend http_frontend
    bind *:80
    redirect scheme https code 301

frontend https_frontend
    bind *:443 ssl crt /etc/ssl/certs/domain.com.pem
    default_backend web_servers
```

### Nginx Redirection
```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name domain.com www.domain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server block
server {
    listen 443 ssl http2;
    server_name domain.com www.domain.com;
    
    ssl_certificate /etc/letsencrypt/live/domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/domain.com/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔍 SSL Testing and Validation

### Command Line Testing
```bash
# Test SSL connection
openssl s_client -connect domain.com:443 -servername domain.com

# Check certificate details
openssl x509 -in /etc/letsencrypt/live/domain.com/cert.pem -text -noout

# Test SSL configuration
curl -I https://domain.com

# Check SSL Labs rating
curl -s "https://api.ssllabs.com/api/v3/analyze?host=domain.com"
```

### SSL Configuration Verification
```bash
# Check HAProxy configuration
sudo haproxy -c -f /etc/haproxy/haproxy.cfg

# Test SSL handshake
nmap --script ssl-enum-ciphers -p 443 domain.com

# Verify certificate chain
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt /etc/letsencrypt/live/domain.com/cert.pem
```

## 🛡️ SSL Security Best Practices

### Strong SSL Configuration
```bash
# Disable weak protocols and ciphers
ssl-default-bind-options no-sslv3 no-tlsv10 no-tlsv11 no-tls-tickets
ssl-default-bind-ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-CHACHA20-POLY1305

# Enable HSTS
http-response set-header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"

# Additional security headers
http-response set-header X-Frame-Options "DENY"
http-response set-header X-Content-Type-Options "nosniff"
http-response set-header X-XSS-Protection "1; mode=block"
```

### Certificate Management
- **Regular Renewal**: Automate certificate renewal
- **Strong Keys**: Use at least 2048-bit RSA or 256-bit ECC keys
- **Certificate Monitoring**: Monitor expiration dates
- **Backup**: Keep secure backups of private keys
- **Revocation**: Know how to revoke compromised certificates

## 📊 Performance Optimization

### SSL Performance Tuning
```bash
# HAProxy SSL optimizations
global
    tune.ssl.default-dh-param 2048
    tune.ssl.cachesize 100000
    tune.ssl.maxrecord 1460
    tune.ssl.lifetime 300

# Enable SSL session reuse
ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets

# Use efficient ciphers
ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
```

### Monitoring SSL Performance
```bash
# Monitor SSL handshake time
curl -w "@curl-format.txt" -o /dev/null -s https://domain.com

# curl-format.txt content:
#     time_namelookup:  %{time_namelookup}\n
#      time_connect:  %{time_connect}\n
#   time_appconnect:  %{time_appconnect}\n
#  time_pretransfer:  %{time_pretransfer}\n
```

## ✅ Requirements

- Ubuntu 16.04 LTS
- HAProxy version 1.5 or higher
- Valid domain name pointing to your servers
- All configuration files must be properly formatted
- SSL certificates must be properly configured
- All scripts should pass shellcheck

## 🎓 Resources

- [What is HTTPS?](https://www.cloudflare.com/learning/ssl/what-is-https/)
- [SSL and SSL Certificates Explained](https://www.digicert.com/what-is-ssl-tls-and-https)
- [HAProxy SSL Termination](https://www.haproxy.com/blog/haproxy-ssl-termination/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [SSL Labs Server Test](https://www.ssllabs.com/ssltest/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
  configuration file that accepts encrypted SSL traffic for the subdomain
  `www.` on TCP port 443.

* **3. No loophole in your website traffic**
  * [100-redirect_http_to_https](./100-redirect_http_to_https): HAproxy
  configuration file that automatically redirects HTTP traffic to HTTPS.
