# 0x09. Web Infrastructure Design

![Infrastructure](https://img.shields.io/badge/Infrastructure-Design-blue)
![Architecture](https://img.shields.io/badge/Web-Architecture-green)
![Scalability](https://img.shields.io/badge/Scalability-High%20Availability-orange)

## 📋 Description

This project focuses on designing web infrastructure from simple single-server setups to complex distributed systems. You'll learn about load balancing, database clustering, security considerations, and monitoring strategies for building scalable and reliable web applications.

**Note**: To view the infrastructure diagrams, download the image files and add the ".png" extension.

## 🎯 Learning Objectives

By the end of this project, you should be able to explain:

- What is a server and where servers usually live
- What is the role of the domain name
- What type of DNS record www is in www.foobar.com
- What is the role of the web server
- What is the role of the application server
- What is the role of the database
- What is the difference between a web server and an application server
- What is DNS and its main role
- What are DNS record types (A, CNAME, TXT, MX)
- What is a load balancer and its distribution algorithms
- What is a single point of failure (SPOF)
- How to avoid downtime when deploying new code
- What is high availability and what does it mean
- What is redundancy
- What is a firewall

## 📁 Files and Diagrams

| File | Description |
|------|-------------|
| `0-simple_web_stack` | Diagram of a simple web infrastructure with one server |
| `1-distributed_web_infrastructure` | Diagram of a three-server web infrastructure |
| `2-secured_and_monitored_web_infrastructure` | Diagram of a secured and monitored three-server web infrastructure |
| `3-scale_up` | Diagram of a scaled-up infrastructure with load balancer cluster |

## 🏗️ Infrastructure Components

### Web Server
- **Role**: Handle HTTP requests and serve static content
- **Examples**: Nginx, Apache HTTP Server
- **Functions**:
  - Serve static files (HTML, CSS, JS, images)
  - Handle SSL/TLS termination
  - Reverse proxy to application servers
  - Load balancing and caching

### Application Server
- **Role**: Execute business logic and dynamic content generation
- **Examples**: Gunicorn, uWSGI, Passenger, Tomcat
- **Functions**:
  - Run application code (Python, Ruby, Java, etc.)
  - Process dynamic requests
  - Connect to databases
  - Session management

### Database
- **Role**: Store and manage application data
- **Types**:
  - **Relational**: MySQL, PostgreSQL
  - **NoSQL**: MongoDB, Redis
  - **In-memory**: Redis, Memcached
- **Functions**:
  - Data persistence
  - Transaction management
  - Data integrity and security

### Load Balancer
- **Role**: Distribute incoming requests across multiple servers
- **Types**:
  - **Layer 4**: Transport layer (TCP/UDP)
  - **Layer 7**: Application layer (HTTP)
- **Algorithms**:
  - Round Robin
  - Least Connections
  - IP Hash
  - Weighted Round Robin

## 🌐 DNS (Domain Name System)

### DNS Record Types
| Type | Purpose | Example |
|------|---------|---------|
| A | Map domain to IPv4 address | example.com → 192.168.1.1 |
| AAAA | Map domain to IPv6 address | example.com → 2001:db8::1 |
| CNAME | Alias for another domain | www.example.com → example.com |
| MX | Mail exchange servers | example.com → mail.example.com |
| TXT | Text information | SPF, DKIM records |
| NS | Name servers | example.com → ns1.example.com |

### DNS Resolution Process
1. User types www.example.com
2. Browser checks local cache
3. Query local DNS resolver
4. Query root name servers
5. Query TLD name servers (.com)
6. Query authoritative name servers
7. Return IP address to browser

## 🏗️ Infrastructure Evolution

### 1. Simple Web Stack (LAMP)
```
Internet → Web Server (Nginx) → Application Server → Database (MySQL)
```
**Components:**
- One server hosting everything
- Domain name pointing to server IP
- Web server (Nginx) handling requests
- Application code processing logic
- Database storing data

**Issues:**
- Single Point of Failure (SPOF)
- No scalability
- Downtime during maintenance
- Resource limitations

### 2. Distributed Web Infrastructure
```
Internet → Load Balancer → [Web Server 1, Web Server 2] → Application Servers → Database
```
**Improvements:**
- Load balancer distributes traffic
- Multiple web servers for redundancy
- Dedicated database server
- Better resource utilization

**Remaining Issues:**
- Database is still a SPOF
- No SSL termination
- No monitoring

### 3. Secured and Monitored Infrastructure
```
Internet → Firewall → Load Balancer (SSL) → [Web Servers] → [App Servers] → Database Cluster
                                                                                    ↓
                                                                              Monitoring System
```
**Security Additions:**
- Firewalls protecting each layer
- SSL certificates for HTTPS
- Database clustering (Master-Slave)
- Monitoring and alerting

### 4. Scaled Infrastructure
```
Internet → [Load Balancer Cluster] → [Web Server Cluster] → [App Server Cluster] → [Database Cluster]
```
**Scalability Features:**
- Load balancer redundancy
- Auto-scaling groups
- Database read replicas
- CDN integration
- Microservices architecture

## 🔒 Security Considerations

### Firewalls
- **Network Firewall**: Controls traffic between networks
- **Host Firewall**: Controls traffic to/from individual servers
- **Application Firewall**: Filters application-layer attacks

### SSL/HTTPS
- **Purpose**: Encrypt data in transit
- **Benefits**:
  - Data confidentiality
  - Data integrity
  - Authentication
  - SEO benefits

### Security Best Practices
- Regular security updates
- Principle of least privilege
- Network segmentation
- Intrusion detection systems
- Regular security audits

## 📊 High Availability & Monitoring

### High Availability Strategies
- **Redundancy**: Multiple components performing same function
- **Failover**: Automatic switching to backup systems
- **Load Distribution**: Spreading load across multiple systems
- **Geographic Distribution**: Multiple data centers

### Monitoring Components
- **Infrastructure Monitoring**: Server health, resources
- **Application Monitoring**: Response times, error rates
- **Log Monitoring**: Application and system logs
- **User Experience Monitoring**: Real user metrics

### Key Metrics
- **Availability**: Uptime percentage (99.9% = 8.76 hours downtime/year)
- **Performance**: Response time, throughput
- **Error Rates**: 4xx/5xx HTTP responses
- **Resource Utilization**: CPU, memory, disk, network

## 🔄 Deployment Strategies

### Zero-Downtime Deployment
- **Blue-Green Deployment**: Switch between two identical environments
- **Rolling Deployment**: Gradually update servers one by one
- **Canary Deployment**: Test with small subset of users first

### Database Strategies
- **Master-Slave Replication**: One write node, multiple read nodes
- **Master-Master Replication**: Multiple write nodes
- **Database Clustering**: Shared storage cluster
- **Database Sharding**: Horizontal partitioning

## ⚖️ Load Balancing Algorithms

### Round Robin
- Distributes requests sequentially
- Simple and fair distribution
- Good for similar server capabilities

### Least Connections
- Routes to server with fewest active connections
- Better for varying request processing times
- Dynamic load distribution

### IP Hash
- Routes based on client IP hash
- Ensures session persistence
- Useful for stateful applications

### Weighted Round Robin
- Assigns weights to servers based on capacity
- Better utilization of heterogeneous servers
- Configurable based on server specifications

## ✅ Requirements

- All diagrams must be whiteboard or digital design tools
- Screenshots should be saved without extension (add .png when viewing)
- Must explain each component's role
- Must identify single points of failure
- Must address security requirements
- Must include monitoring strategy

## 🎓 Resources

- [Network basics](https://www.techtarget.com/searchnetworking/definition/network)
- [Server](https://en.wikipedia.org/wiki/Server_%28computing%29)
- [Web server](https://en.wikipedia.org/wiki/Web_server)
- [DNS](https://www.cloudflare.com/learning/dns/what-is-dns/)
- [Load balancer](https://www.nginx.com/resources/glossary/load-balancing/)
- [Monitoring](https://www.datadoghq.com/knowledge-center/what-is-monitoring/)
- [Database](https://searchdatamanagement.techtarget.com/definition/database)
- [Difference between web server and app server](https://www.nginx.com/resources/glossary/application-server-vs-web-server/)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
