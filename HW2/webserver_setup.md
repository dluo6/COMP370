1. Connect to Lightsail with ssh command
2. Run "sudo apt update"
3. Run "sudo apt install apache2"
4. Create comp370_hw2.txt in the directory "var/www/html"
5. Edit  "/etc/apache2/ports.conf" to include "Listen 8008"
6. Edit "/etc/apache2/sites-enables/000-default.conf" to include "<VirtualHost *: 8008> #same configurations </VirtualHost>"
7. Restart with "sudo apache2ctl restart"