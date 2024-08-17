-- Create salmaneben_user if it doesn't exist
CREATE USER IF NOT EXISTS 'salmaneben_user'@'localhost' IDENTIFIED BY "projectcorrection280hbtn";
GRANT REPLICATION CLIENT ON *.* TO 'salmaneben_user'@'localhost';

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS tyrell_corp;
USE tyrell_corp;

-- Create the table if it doesn't exist
CREATE TABLE IF NOT EXISTS nexus6(id INTEGER, name TEXT);

-- Insert data only if it doesn't exist
INSERT INTO nexus6 (id, name) SELECT 0, 'Jarvis' WHERE NOT EXISTS (SELECT 1 FROM nexus6 WHERE id = 0);

-- Grant privileges to salmaneben_user
GRANT SELECT ON tyrell_corp.nexus6 TO 'salmaneben_user'@'localhost';

-- Create replica_user if it doesn't exist
CREATE USER IF NOT EXISTS 'replica_user'@'%' IDENTIFIED BY "replica_user";
GRANT REPLICATION SLAVE ON *.* TO 'replica_user'@'%';
GRANT SELECT ON mysql.user TO 'salmaneben_user'@'localhost';

-- Create web02 user if it doesn't exist
CREATE USER IF NOT EXISTS 'web02'@'100.26.252.211' IDENTIFIED BY "web02";
GRANT REPLICATION SLAVE ON *.* TO 'web02'@'100.26.252.211';

