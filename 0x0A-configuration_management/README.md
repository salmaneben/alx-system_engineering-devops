# 0x0A. Configuration Management

![Puppet](https://img.shields.io/badge/Puppet-Configuration%20Management-orange)
![DevOps](https://img.shields.io/badge/DevOps-Automation-blue)
![Infrastructure](https://img.shields.io/badge/Infrastructure-as%20Code-green)

## 📋 Description

This project introduces configuration management using Puppet, a powerful automation tool for managing infrastructure as code. You'll learn to write Puppet manifests to automate system configuration, package management, service control, and file management across multiple servers consistently and reliably.

## 🎯 Learning Objectives

By the end of this project, you should be able to:

- Understand the importance of configuration management
- Write and execute Puppet manifests
- Manage files, packages, and services with Puppet
- Use Puppet resources and resource types effectively
- Implement idempotent configuration management
- Handle dependencies and ordering in Puppet
- Debug and troubleshoot Puppet manifests
- Apply configuration management best practices
- Understand Infrastructure as Code principles

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-create_a_file.pp` | Puppet manifest that creates a file with specific permissions and content |
| `1-install_a_package.pp` | Puppet manifest that installs a specific version of Flask using pip3 |
| `2-execute_a_command.pp` | Puppet manifest that kills a process using the pkill command |

## 🔧 Configuration Management Fundamentals

### What is Configuration Management?

Configuration Management is the practice of handling changes systematically so that a system maintains its integrity over time. It involves:

- **Consistency**: Ensuring all systems have the same configuration
- **Automation**: Reducing manual intervention and human error
- **Scalability**: Managing hundreds or thousands of servers efficiently
- **Auditability**: Tracking what changes were made and when
- **Recovery**: Quickly restoring systems to a known good state

### Benefits of Configuration Management
- **Reproducibility**: Create identical environments consistently
- **Version Control**: Track configuration changes over time
- **Disaster Recovery**: Quickly rebuild systems from code
- **Compliance**: Ensure systems meet security and regulatory requirements
- **Cost Reduction**: Reduce manual configuration time and errors

## 🚀 Puppet Fundamentals

### Puppet Architecture
```
Puppet Master (Server)
├── Manifests (Configuration files)
├── Modules (Reusable components)
└── Facts (System information)
        ↓
Puppet Agent (Client)
├── Catalog (Compiled configuration)
├── Resources (System components)
└── Reports (Execution results)
```

### Basic Puppet Syntax
```puppet
# Resource declaration
resource_type { 'resource_title':
  attribute => value,
  attribute => value,
}

# Example: File resource
file { '/tmp/example':
  ensure  => file,
  content => 'Hello World',
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
}
```

## 📝 Puppet Manifest Examples

### Task 0: Create a File
```puppet
# 0-create_a_file.pp
# Create a file in /tmp with specific attributes

file { '/tmp/school':
  ensure  => file,
  mode    => '0744',
  owner   => 'www-data',
  group   => 'www-data',
  content => 'I love Puppet',
}
```

**Explanation:**
- `ensure => file`: Creates a file (not directory or link)
- `mode => '0744'`: Sets permissions (owner: rwx, group: r--, others: r--)
- `owner => 'www-data'`: Sets file owner
- `group => 'www-data'`: Sets file group
- `content => 'I love Puppet'`: Sets file content

### Task 1: Install a Package
```puppet
# 1-install_a_package.pp
# Install Flask version 2.1.0 using pip3

package { 'flask':
  ensure   => '2.1.0',
  provider => 'pip3',
}
```

**Explanation:**
- `ensure => '2.1.0'`: Installs specific version of Flask
- `provider => 'pip3'`: Uses pip3 package manager

### Task 2: Execute a Command
```puppet
# 2-execute_a_command.pp
# Kill a process named killmenow using pkill

exec { 'kill_killmenow_process':
  command => '/usr/bin/pkill killmenow',
  onlyif  => '/usr/bin/pgrep killmenow',
}
```

**Explanation:**
- `command => '/usr/bin/pkill killmenow'`: Command to execute
- `onlyif => '/usr/bin/pgrep killmenow'`: Only run if process exists

## 🔧 Advanced Puppet Concepts

### Resource Types and Attributes

#### File Resource
```puppet
file { '/etc/motd':
  ensure  => file,
  content => "Welcome to ${hostname}\n",
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  backup  => true,
}
```

#### Package Resource
```puppet
package { 'nginx':
  ensure => installed,
}

package { 'apache2':
  ensure => absent,
}

package { ['git', 'curl', 'vim']:
  ensure => installed,
}
```

#### Service Resource
```puppet
service { 'nginx':
  ensure => running,
  enable => true,
  require => Package['nginx'],
}
```

#### User Resource
```puppet
user { 'developer':
  ensure     => present,
  uid        => 1001,
  gid        => 1001,
  shell      => '/bin/bash',
  home       => '/home/developer',
  managehome => true,
}
```

#### Group Resource
```puppet
group { 'developers':
  ensure => present,
  gid    => 1001,
}
```

### Dependencies and Ordering

#### Using require
```puppet
package { 'nginx':
  ensure => installed,
}

service { 'nginx':
  ensure  => running,
  enable  => true,
  require => Package['nginx'],
}
```

#### Using before
```puppet
package { 'nginx':
  ensure => installed,
  before => Service['nginx'],
}

service { 'nginx':
  ensure => running,
  enable => true,
}
```

#### Using notify and subscribe
```puppet
file { '/etc/nginx/nginx.conf':
  ensure  => file,
  content => template('nginx/nginx.conf.erb'),
  notify  => Service['nginx'],
}

service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/nginx.conf'],
}
```

## 🗂️ Puppet Modules Structure

### Module Directory Structure
```
modules/
└── webserver/
    ├── manifests/
    │   ├── init.pp
    │   ├── config.pp
    │   └── service.pp
    ├── files/
    │   └── nginx.conf
    ├── templates/
    │   └── virtualhost.erb
    ├── lib/
    ├── facts.d/
    └── examples/
        └── init.pp
```

### Example Module: webserver
```puppet
# modules/webserver/manifests/init.pp
class webserver (
  $package_name = 'nginx',
  $service_name = 'nginx',
  $config_file  = '/etc/nginx/nginx.conf',
) {
  
  package { $package_name:
    ensure => installed,
  }
  
  file { $config_file:
    ensure  => file,
    source  => 'puppet:///modules/webserver/nginx.conf',
    require => Package[$package_name],
    notify  => Service[$service_name],
  }
  
  service { $service_name:
    ensure => running,
    enable => true,
  }
}
```

## 🔍 Puppet Facts and Variables

### System Facts
```puppet
# Using facts in manifests
file { '/tmp/system_info':
  ensure  => file,
  content => "Hostname: ${facts['hostname']}
OS: ${facts['os']['name']} ${facts['os']['release']['full']}
Architecture: ${facts['architecture']}
Memory: ${facts['memory']['system']['total']}",
}
```

### Custom Facts
```puppet
# Custom fact example
# /etc/facter/facts.d/custom_fact.txt
application_version=1.2.3
environment=production
```

### Variables and Conditionals
```puppet
$environment = 'production'

if $environment == 'production' {
  $max_connections = 1000
} else {
  $max_connections = 100
}

file { '/etc/app.conf':
  content => "max_connections=${max_connections}\n",
}
```

## 📊 Puppet Testing and Validation

### Syntax Checking
```bash
# Check Puppet syntax
puppet parser validate manifest.pp

# Check all manifests in directory
find . -name "*.pp" -exec puppet parser validate {} \;
```

### Dry Run (Noop Mode)
```bash
# Test what would happen without making changes
puppet apply --noop manifest.pp

# Verbose output
puppet apply --noop --verbose manifest.pp
```

### Puppet Lint
```bash
# Install puppet-lint
gem install puppet-lint

# Check code style
puppet-lint manifest.pp

# Fix automatically when possible
puppet-lint --fix manifest.pp
```

## 🛠️ Advanced Configuration Examples

### Web Server Configuration
```puppet
class apache_webserver {
  # Install Apache
  package { 'apache2':
    ensure => installed,
  }
  
  # Configure Apache
  file { '/etc/apache2/sites-available/000-default.conf':
    ensure  => file,
    content => template('apache/virtualhost.erb'),
    require => Package['apache2'],
    notify  => Service['apache2'],
  }
  
  # Enable site
  exec { 'enable-default-site':
    command => '/usr/sbin/a2ensite 000-default.conf',
    unless  => '/usr/sbin/a2ensite -l | grep 000-default',
    require => File['/etc/apache2/sites-available/000-default.conf'],
    notify  => Service['apache2'],
  }
  
  # Start service
  service { 'apache2':
    ensure => running,
    enable => true,
  }
}
```

### Database Server Configuration
```puppet
class mysql_server (
  $root_password = 'secure_password',
) {
  # Install MySQL
  package { 'mysql-server':
    ensure => installed,
  }
  
  # Configure MySQL
  file { '/etc/mysql/mysql.conf.d/mysqld.cnf':
    ensure  => file,
    content => template('mysql/mysqld.cnf.erb'),
    require => Package['mysql-server'],
    notify  => Service['mysql'],
  }
  
  # Set root password
  exec { 'set-mysql-password':
    command => "/usr/bin/mysqladmin -u root password '${root_password}'",
    unless  => "/usr/bin/mysqladmin -u root -p'${root_password}' status",
    require => Service['mysql'],
  }
  
  # Start service
  service { 'mysql':
    ensure => running,
    enable => true,
  }
}
```

### User Management
```puppet
class user_management {
  # Create groups
  group { 'developers':
    ensure => present,
    gid    => 1001,
  }
  
  group { 'admins':
    ensure => present,
    gid    => 1002,
  }
  
  # Create users
  user { 'john':
    ensure     => present,
    uid        => 1001,
    gid        => 1001,
    groups     => ['developers', 'admins'],
    shell      => '/bin/bash',
    home       => '/home/john',
    managehome => true,
    require    => [Group['developers'], Group['admins']],
  }
  
  # SSH key management
  ssh_authorized_key { 'john@company.com':
    ensure => present,
    user   => 'john',
    type   => 'ssh-rsa',
    key    => 'AAAAB3NzaC1yc2EAAAADAQABAAABgQC...',
  }
}
```

## 🔐 Security and Best Practices

### File Security
```puppet
# Secure configuration file
file { '/etc/app/config.conf':
  ensure  => file,
  content => template('app/config.conf.erb'),
  owner   => 'root',
  group   => 'app',
  mode    => '0640',
  backup  => true,
}

# Secure directory
file { '/etc/ssl/private':
  ensure => directory,
  owner  => 'root',
  group  => 'ssl-cert',
  mode   => '0710',
}
```

### Package Security
```puppet
# Ensure security updates
package { 'unattended-upgrades':
  ensure => installed,
}

# Remove unwanted packages
package { ['telnet', 'rsh-server']:
  ensure => absent,
}
```

### Service Security
```puppet
# Disable unnecessary services
service { ['rpcbind', 'nfs-server']:
  ensure => stopped,
  enable => false,
}
```

## 📋 Best Practices

### Code Organization
1. **Use modules**: Organize code into reusable modules
2. **Follow naming conventions**: Use descriptive, consistent names
3. **Document code**: Add comments explaining complex logic
4. **Version control**: Use Git for configuration management
5. **Test thoroughly**: Validate changes before production

### Performance Optimization
```puppet
# Use arrays for multiple resources
package { ['git', 'curl', 'vim', 'htop']:
  ensure => installed,
}

# Use collectors for efficient resource management
Package <| tag == 'development' |>
```

### Error Handling
```puppet
# Graceful failure handling
exec { 'optional-command':
  command  => '/usr/bin/some-command',
  returns  => [0, 1],  # Accept exit codes 0 or 1
  timeout  => 30,
  tries    => 3,
  try_sleep => 5,
}
```

## ✅ Requirements

- Ubuntu 16.04 LTS or later
- Puppet 5.5 or later
- Understanding of Linux system administration
- Basic knowledge of YAML and Ruby syntax
- Familiarity with package managers (apt, yum, etc.)

## 🎓 Resources

- [Puppet Documentation](https://puppet.com/docs/)
- [Puppet Language Reference](https://puppet.com/docs/puppet/latest/lang_summary.html)
- [Puppet Forge](https://forge.puppet.com/) - Module repository
- [Puppet Style Guide](https://puppet.com/docs/puppet/latest/style_guide.html)
- [Infrastructure as Code Best Practices](https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/infrastructure-as-code.html)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.*

* **1. Install a package**
  * [1-install_a_package.pp](./1-install_a_package.pp): Puppet manifest file
  that install `flask` from pip3.

* **2. Execute a command**
  * [2-execute_a_command.pp](./2-execute_a_command.pp): Puppet manifest file
  that kills the process `killmenow`.
