# 0x07. Networking Basics

![Networking](https://img.shields.io/badge/Networking-Fundamentals-blue)
![OSI](https://img.shields.io/badge/OSI-Model-green)
![TCP/IP](https://img.shields.io/badge/TCP%2FIP-Protocol-orange)

## 📋 Description

This project introduces fundamental networking concepts including the OSI model, TCP/UDP protocols, IP addressing, and basic network troubleshooting. You'll learn how computers communicate over networks and understand the layers of network communication.

## 🎯 Learning Objectives

By the end of this project, you should be able to explain:

- What is the OSI model and what are its 7 layers
- What is a LAN, WAN, and the Internet
- What are IP addresses (IPv4 and IPv6)
- What are localhost, 127.0.0.1, and 0.0.0.0
- What are TCP and UDP protocols
- What are ports and well-known port numbers
- What tool/protocol is often used to check if a device is connected to a network

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-OSI_model` | Answers about the OSI model layers and organization |
| `1-types_of_network` | Answers about different types of networks (LAN, WAN, Internet) |
| `2-MAC_and_IP_address` | Answers about MAC and IP addresses |
| `3-UDP_and_TCP` | Answers about UDP and TCP protocols |
| `4-TCP_and_UDP_ports` | Bash script that displays listening ports |
| `5-is_the_host_on_the_network` | Bash script that pings an IP address |

## 🌐 OSI Model

### The 7 Layers

| Layer | Name | Description | Examples |
|-------|------|-------------|----------|
| 7 | Application | User interface, network services | HTTP, FTP, SMTP, DNS |
| 6 | Presentation | Data formatting, encryption, compression | SSL/TLS, JPEG, MPEG |
| 5 | Session | Session management, dialog control | NetBIOS, RPC, SQL |
| 4 | Transport | End-to-end delivery, error correction | TCP, UDP |
| 3 | Network | Routing, logical addressing | IP, ICMP, ARP |
| 2 | Data Link | Frame formatting, error detection | Ethernet, WiFi, PPP |
| 1 | Physical | Physical transmission of data | Cables, hubs, repeaters |

### How Data Flows
```
Application Data
      ↓ (Encapsulation)
[Header|Data|Trailer] - Each layer adds headers
      ↓
Physical transmission
      ↓
[Header|Data|Trailer] - Each layer removes headers
      ↓ (Decapsulation)
Application Data
```

## 🔗 Network Types

### LAN (Local Area Network)
- **Scope**: Small geographical area (home, office, school)
- **Size**: Few meters to few kilometers
- **Ownership**: Usually privately owned
- **Examples**: Home WiFi, office network

### WAN (Wide Area Network)
- **Scope**: Large geographical area (cities, countries)
- **Size**: Hundreds to thousands of kilometers
- **Ownership**: Usually public infrastructure
- **Examples**: Internet, corporate networks across cities

### MAN (Metropolitan Area Network)
- **Scope**: City or metropolitan area
- **Size**: 5-50 kilometers
- **Examples**: City-wide WiFi, cable TV networks

## 🌍 IP Addressing

### IPv4 Addresses
- **Format**: 32-bit (4 bytes) - xxx.xxx.xxx.xxx
- **Range**: 0.0.0.0 to 255.255.255.255
- **Classes**:
  - Class A: 1.0.0.0 to 126.255.255.255 (large networks)
  - Class B: 128.0.0.0 to 191.255.255.255 (medium networks)
  - Class C: 192.0.0.0 to 223.255.255.255 (small networks)

### Special IP Addresses
- **127.0.0.1**: Localhost (loopback)
- **0.0.0.0**: All interfaces / any address
- **255.255.255.255**: Broadcast address
- **10.0.0.0/8**: Private network (Class A)
- **172.16.0.0/12**: Private network (Class B)
- **192.168.0.0/16**: Private network (Class C)

### IPv6 Addresses
- **Format**: 128-bit (16 bytes) - xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx
- **Example**: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
- **Loopback**: ::1

## 🔌 MAC vs IP Addresses

### MAC Address (Media Access Control)
- **Purpose**: Physical addressing at data link layer
- **Format**: 48-bit (6 bytes) - XX:XX:XX:XX:XX:XX
- **Scope**: Local network segment only
- **Example**: 00:1B:44:11:3A:B7
- **Characteristics**: Burned into network interface card

### IP Address (Internet Protocol)
- **Purpose**: Logical addressing at network layer
- **Format**: 32-bit (IPv4) or 128-bit (IPv6)
- **Scope**: Global internet routing
- **Characteristics**: Can be changed, assigned by network

## 🚛 Transport Protocols

### TCP (Transmission Control Protocol)
- **Type**: Connection-oriented
- **Reliability**: Guaranteed delivery
- **Features**:
  - Error checking and correction
  - Flow control
  - Packet ordering
  - Acknowledgments
- **Use Cases**: Web browsing, email, file transfer
- **Header Size**: 20-60 bytes

### UDP (User Datagram Protocol)
- **Type**: Connectionless
- **Reliability**: Best effort (no guarantees)
- **Features**:
  - Fast transmission
  - No acknowledgments
  - No error correction
  - Minimal overhead
- **Use Cases**: Streaming, gaming, DNS queries
- **Header Size**: 8 bytes

### Protocol Comparison
| Feature | TCP | UDP |
|---------|-----|-----|
| Connection | Required | Not required |
| Reliability | High | Low |
| Speed | Slower | Faster |
| Overhead | High | Low |
| Use Case | Accuracy important | Speed important |

## 🔌 Common Ports

### Well-Known Ports (0-1023)
| Port | Protocol | Service |
|------|----------|---------|
| 20/21 | FTP | File Transfer Protocol |
| 22 | SSH | Secure Shell |
| 23 | Telnet | Remote terminal |
| 25 | SMTP | Email sending |
| 53 | DNS | Domain Name System |
| 80 | HTTP | Web traffic |
| 110 | POP3 | Email retrieval |
| 143 | IMAP | Email access |
| 443 | HTTPS | Secure web traffic |
| 993 | IMAPS | Secure IMAP |
| 995 | POP3S | Secure POP3 |

### Port Ranges
- **Well-known**: 0-1023 (system/root privileges)
- **Registered**: 1024-49151 (user applications)
- **Dynamic/Private**: 49152-65535 (temporary connections)

## 🛠 Network Tools

### Connectivity Testing
```bash
# Ping - Test connectivity
ping 8.8.8.8                    # Test connectivity to Google DNS
ping -c 4 google.com            # Send 4 packets

# Traceroute - Show path to destination
traceroute google.com
tracert google.com              # Windows version
```

### Port Scanning
```bash
# Netstat - Show listening ports
netstat -tuln                   # Show all listening ports
netstat -an | grep :80         # Check if port 80 is open

# SS - Modern netstat replacement
ss -tuln                        # Show listening ports
ss -tp                          # Show processes using ports
```

### DNS Tools
```bash
# Nslookup - DNS queries
nslookup google.com

# Dig - Advanced DNS queries
dig google.com
dig @8.8.8.8 google.com MX     # Query specific DNS server for MX records
```

## 🔍 Network Troubleshooting

### Basic Troubleshooting Steps
1. **Check physical connection**
2. **Verify IP configuration**
3. **Test local connectivity** (ping gateway)
4. **Test remote connectivity** (ping external host)
5. **Check DNS resolution**
6. **Verify application-specific settings**

### Common Commands
```bash
# Check network interface configuration
ifconfig                        # Linux/macOS
ip addr show                    # Modern Linux
ipconfig                        # Windows

# Check routing table
route -n                        # Linux
ip route show                   # Modern Linux
route print                     # Windows

# Check ARP table
arp -a                          # Show ARP cache
ip neigh show                   # Modern Linux
```

## ✅ Requirements

- All answer files tested on Ubuntu 20.04 LTS
- Answer files should contain only the correct answer
- Bash scripts must be executable
- All scripts should be exactly 3 lines long
- First line should be `#!/usr/bin/env bash`
- Second line should be a comment explaining the script

## 🎓 Resources

- [OSI Model](https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/)
- [Types of Networks](https://www.geeksforgeeks.org/types-of-network-lan-man-wan/)
- [MAC Address vs IP Address](https://www.geeksforgeeks.org/difference-between-mac-address-and-ip-address/)
- [TCP vs UDP](https://www.geeksforgeeks.org/differences-between-tcp-and-udp/)
- [List of Well-Known Ports](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers)
- [Internet Protocol](https://en.wikipedia.org/wiki/Internet_Protocol)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
