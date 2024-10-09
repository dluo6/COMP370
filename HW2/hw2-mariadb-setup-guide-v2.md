# Setting Up MariaDB on AWS Lightsail Ubuntu Instance

## 1. Install MariaDB:
```
sudo apt install mariadb-server
```

## 2. Configure MariaDB to Run on Port 6002
Edit the MariaDB configuration file:

```
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```

Find the [mysqld] section and add or modify the port setting:

```
[mysqld]
port = 6002
```

Save and exit the editor (in Nano, press Ctrl+X, then Y, then Enter).

Restart MariaDB to apply the changes:

```
sudo systemctl restart mariadb
```

## 3. Create the Database and User
Log into MariaDB:

```
sudo mysql
```

Create the comp370_test database:

```sql
CREATE DATABASE comp370_test;
```

Create the comp370 user and grant permissions:

```sql
CREATE USER 'comp370'@'%' IDENTIFIED BY '$ungl@ss3s';
GRANT ALL PRIVILEGES ON comp370_test.* TO 'comp370'@'%';
FLUSH PRIVILEGES;
```

Exit the MariaDB prompt:

```sql
EXIT;
```

## 4. Allow External Access
Edit the MariaDB configuration file to allow remote connections:

```
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```

Find the bind-address setting and change it:

```
bind-address = 0.0.0.0
```

Save and exit the editor.

Open port 6002 in your Lightsail firewall settings:

1. Log in to AWS Lightsail Console:
   - Go to the AWS Lightsail console.

2. Select Your Instance:
   - On the Lightsail dashboard, you'll see a list of your instances.
   - Click on the name of the instance where you want to open port 6002.

3. Navigate to the Networking Tab:
   - Once you're on the instance management page, you'll see a series of tabs at the top.
   - Click on the Networking tab.

4. Edit the Firewall Rules:
   - In the Networking tab, you'll find a section called Firewall.
   - Click the Edit rules button to modify the firewall rules.

5. Add a New Rule:
   - Click on Add another to create a new rule.
   - Application: Select Custom
   - Protocol: Ensure TCP is selected.
   - Port/Range: Enter 6002.

6. Save the Rule:
   - After entering the rule details, click on Save or Save rules (depending on the interface) to apply the changes.

Restart MariaDB:

```
sudo systemctl restart mariadb
```

## 5. Test the Connection
Install a database client (e.g., DBeaver) on your personal computer.

Connect to the database using the following details:
```
Host: Your Lightsail instance's public IP address
Port: 6002
Database: comp370_test
User: comp370
Password: $ungl@ss3s
```
Replace your-instance-public-ip with the public IP address of your Lightsail instance.

You should now be able to connect to your MariaDB instance running on port 6002.
