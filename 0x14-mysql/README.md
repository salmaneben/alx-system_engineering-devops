# 0x14. MySQL

![MySQL](https://img.shields.io/badge/MySQL-Database-blue)
![Replication](https://img.shields.io/badge/Database-Replication-green)
![Backup](https://img.shields.io/badge/Database-Backup-orange)

## 📋 Description

This project focuses on MySQL database management, including installation, configuration, replication setup, and backup strategies. You'll learn to set up MySQL servers, configure master-slave replication for high availability, and implement proper backup and recovery procedures.

## 🎯 Learning Objectives

By the end of this project, you should be able to explain:

- What is the main role of a database
- What is a database replica
- What is the purpose of a database replica
- Why database backups need to be stored in different physical locations
- What operation should you regularly perform to make sure that your database backup strategy actually works
- How to set up MySQL replication
- How to build a robust database backup strategy

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `4-mysql_configuration_primary` | MySQL configuration file for the primary (master) server |
| `4-mysql_configuration_replica` | MySQL configuration file for the replica (slave) server |
| `5-mysql_backup` | Bash script that generates a MySQL dump and creates a compressed archive |

## 🚀 Installation and Setup

### Install MySQL Server

```bash
# Update package repository
sudo apt update

# Install MySQL Server
sudo apt install mysql-server

# Secure MySQL installation
sudo mysql_secure_installation

# Start and enable MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql

# Check MySQL status
sudo systemctl status mysql
```

### Initial Configuration

```bash
# Connect to MySQL as root
sudo mysql

# Create a new user for replication
CREATE USER 'replica_user'@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO 'replica_user'@'%';

# Create database and user for holberton
CREATE DATABASE holberton;
CREATE USER 'holberton_user'@'localhost' IDENTIFIED BY 'projectcorrection280hbtn';
GRANT SELECT ON holberton.* TO 'holberton_user'@'localhost';

# Create sample table
USE holberton;
CREATE TABLE nexus6 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(256) NOT NULL
);

# Insert sample data
INSERT INTO nexus6 (name) VALUES ('Leon');

FLUSH PRIVILEGES;
```

## 🔄 MySQL Replication Setup

### Primary Server Configuration

#### Edit MySQL Configuration
```bash
# Edit MySQL configuration file
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

**Key Configuration Settings:**
```ini
[mysqld]
# Server identification
server-id = 1

# Enable binary logging
log_bin = /var/log/mysql/mysql-bin.log

# Databases to replicate
binlog_do_db = holberton

# Bind to all interfaces
bind-address = 0.0.0.0
```

#### Configure Replication User
```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create replication user
CREATE USER 'replica_user'@'replica_server_ip' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO 'replica_user'@'replica_server_ip';
FLUSH PRIVILEGES;

-- Check master status
SHOW MASTER STATUS;
-- Note the File and Position values
```

### Replica Server Configuration

#### Edit MySQL Configuration
```bash
# Edit MySQL configuration file
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

**Key Configuration Settings:**
```ini
[mysqld]
# Server identification (must be different from master)
server-id = 2

# Enable relay logging
relay-log = /var/log/mysql/mysql-relay-bin.log

# Database to replicate
replicate-do-db = holberton

# Bind to all interfaces
bind-address = 0.0.0.0
```

#### Configure Slave Connection
```sql
-- Connect to MySQL as root
mysql -u root -p

-- Configure slave to connect to master
CHANGE MASTER TO
MASTER_HOST='primary_server_ip',
MASTER_USER='replica_user',
MASTER_PASSWORD='password',
MASTER_LOG_FILE='mysql-bin.000001',
MASTER_LOG_POS=154;

-- Start slave replication
START SLAVE;

-- Check slave status
SHOW SLAVE STATUS\G
```

## 💾 Database Backup Strategy

### Creating Backups

#### MySQL Dump Backup
```bash
#!/usr/bin/env bash
# Creates a MySQL dump of all databases

# Variables
BACKUP_DIR="/var/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_${DATE}.sql"
ARCHIVE_FILE="${DATE}.tar.gz"

# Create backup directory
mkdir -p $BACKUP_DIR

# Create MySQL dump
mysqldump -u root --all-databases --single-transaction --routines --triggers > $BACKUP_DIR/$BACKUP_FILE

# Create compressed archive
tar -czf $BACKUP_DIR/$ARCHIVE_FILE -C $BACKUP_DIR $BACKUP_FILE

# Remove uncompressed dump
rm $BACKUP_DIR/$BACKUP_FILE

echo "Backup created: $BACKUP_DIR/$ARCHIVE_FILE"
```

#### Automated Backup Script
```bash
#!/usr/bin/env bash
# 5-mysql_backup - Creates compressed MySQL dump

# Check if password is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <mysql_password>"
    exit 1
fi

MYSQL_PASSWORD=$1
DATE=$(date +"%d-%m-%Y")
BACKUP_FILE="backup.sql"
ARCHIVE_FILE="${DATE}.tar.gz"

# Create MySQL dump
mysqldump -u root -p$MYSQL_PASSWORD --all-databases > $BACKUP_FILE

# Create compressed archive
tar -czf $ARCHIVE_FILE $BACKUP_FILE

# Remove uncompressed dump
rm $BACKUP_FILE

echo "Backup completed: $ARCHIVE_FILE"
```

### Backup Best Practices

#### Storage Locations
- **Local Backup**: On same server (quick recovery)
- **Remote Backup**: Different server/location (disaster recovery)
- **Cloud Backup**: Cloud storage (AWS S3, Google Cloud)
- **Offsite Backup**: Physical different location

#### Backup Frequency
- **Critical Data**: Every hour or real-time
- **Important Data**: Daily backups
- **Regular Data**: Weekly backups
- **Archive Data**: Monthly backups

#### Backup Testing
```bash
# Test backup restoration
mysql -u root -p < backup.sql

# Verify data integrity
mysql -u root -p -e "SELECT COUNT(*) FROM holberton.nexus6;"

# Test backup automation
crontab -e
# Add: 0 2 * * * /path/to/backup_script.sh password
```

## 📊 Replication Monitoring

### Check Replication Status

#### On Master Server
```sql
-- Show master status
SHOW MASTER STATUS;

-- Show binary logs
SHOW BINARY LOGS;

-- Show slave hosts
SHOW SLAVE HOSTS;
```

#### On Slave Server
```sql
-- Show slave status (detailed)
SHOW SLAVE STATUS\G

-- Key fields to monitor:
-- Slave_IO_Running: Yes
-- Slave_SQL_Running: Yes
-- Seconds_Behind_Master: 0 (or low number)
-- Last_Error: (should be empty)
```

### Troubleshooting Replication

#### Common Issues
```sql
-- Slave not connecting
SHOW SLAVE STATUS\G
-- Check: Last_IO_Error

-- Slave lagging behind
SHOW SLAVE STATUS\G
-- Check: Seconds_Behind_Master

-- SQL errors on slave
SHOW SLAVE STATUS\G
-- Check: Last_SQL_Error

-- Reset slave if needed
STOP SLAVE;
RESET SLAVE;
-- Reconfigure and start
```

#### Replication Repair
```sql
-- Skip one statement causing error
SET GLOBAL sql_slave_skip_counter = 1;
START SLAVE;

-- Or reset and resync
STOP SLAVE;
RESET SLAVE;
-- Restore from fresh backup
-- Reconfigure replication
```

## 🔧 Database Maintenance

### Regular Maintenance Tasks

#### Optimize Tables
```sql
-- Optimize specific table
OPTIMIZE TABLE holberton.nexus6;

-- Optimize all tables in database
SELECT CONCAT('OPTIMIZE TABLE ', table_schema, '.', table_name, ';')
FROM information_schema.tables
WHERE table_schema = 'holberton';
```

#### Check Table Integrity
```sql
-- Check table for errors
CHECK TABLE holberton.nexus6;

-- Repair table if needed
REPAIR TABLE holberton.nexus6;
```

#### Monitor Disk Usage
```sql
-- Check database sizes
SELECT 
    table_schema AS 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables
GROUP BY table_schema;
```

## 🔒 Security Best Practices

### User Management
```sql
-- Create users with minimal privileges
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON app_db.* TO 'app_user'@'localhost';

-- Remove anonymous users
DELETE FROM mysql.user WHERE User='';

-- Remove test database
DROP DATABASE IF EXISTS test;

FLUSH PRIVILEGES;
```

### Network Security
```bash
# Configure firewall
sudo ufw allow from trusted_ip to any port 3306
sudo ufw deny 3306

# Use SSL connections
# Edit /etc/mysql/mysql.conf.d/mysqld.cnf
# ssl-ca=/path/to/ca.pem
# ssl-cert=/path/to/server-cert.pem
# ssl-key=/path/to/server-key.pem
```

## 📈 Performance Optimization

### Configuration Tuning
```ini
# /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
# Memory settings
innodb_buffer_pool_size = 70% of RAM
innodb_log_file_size = 256M
innodb_log_buffer_size = 16M

# Connection settings
max_connections = 200
thread_cache_size = 16

# Query cache (for older MySQL versions)
query_cache_type = 1
query_cache_size = 256M
```

### Monitoring Performance
```sql
-- Show running processes
SHOW PROCESSLIST;

-- Show slow queries
SHOW VARIABLES LIKE 'slow_query_log';
SET GLOBAL slow_query_log = 'ON';

-- Check InnoDB status
SHOW ENGINE INNODB STATUS;
```

## ✅ Requirements

- MySQL 5.7.x installed on Ubuntu 16.04 LTS
- All SQL files must end with a new line
- All Bash scripts must be executable
- All scripts should pass shellcheck
- First line of all Bash scripts: `#!/usr/bin/env bash`
- Second line should be a comment explaining the script

## 🎓 Resources

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [MySQL Replication](https://dev.mysql.com/doc/refman/5.7/en/replication.html)
- [MySQL Backup and Recovery](https://dev.mysql.com/doc/refman/5.7/en/backup-and-recovery.html)
- [MySQL Performance Tuning](https://dev.mysql.com/doc/refman/5.7/en/optimization.html)
- [MySQL Security](https://dev.mysql.com/doc/refman/5.7/en/security.html)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*
