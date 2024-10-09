1. Run "sudo apt update"
2. Run "sudo apt install mariadb-server"
3. Run "sudo mysql_secure_installation"
4. Add "port = 6002" to "etc/mysql/my.cnf"
5. Run "sudo mysql" to enter MariaDB interface
6. Create database with "CREATE DATABASE comp370_test"
7. Create user with "CREATE UESR comp370 IDENTIFIED BY '$ungl@ss3s'"