# Setting up a Webserver on EC2 (Ubuntu)

This guide will walk you through the process of setting up an Apache webserver on an Ubuntu EC2 instance to serve a file `comp370_hw2.txt` on port 8008.

## Step 1: **Connect to Your Instance**:
After your instance is running, connect to it via SSH using the Lightsail console or using an SSH client like PuTTY or Terminal.

```bash
ssh -i /path/to/your-key.pem ubuntu@X.Y.Z.W
```

Replace `/path/to/your-key.pem` with the path to your key file and `X.Y.Z.W` with your EC2's public IP address.

## Step 2: **Update the system and install Apache**

Once connected, update the system and install Apache:

```bash
sudo apt update
sudo apt install apache2 -y
```
Enable Apache to Start at Boot:

```bash
sudo systemctl enable apache2
```

## Step 3: **Configure Apache to listen on port 8008**

Edit the Apache ports configuration file:

```bash
sudo nano /etc/apache2/ports.conf
```

Add or modify the following line:

```
Listen 8008
```

Save and exit the file (Ctrl+X, then Y, then Enter).

Next, edit the default virtual host configuration:

```bash
sudo nano /etc/apache2/sites-available/000-default.conf
```

Change the `<VirtualHost *:80>` line to `<VirtualHost *:8008>`. Save and exit the file.

## Step 4: Create the **comp370_hw2.txt file**

Create and edit the file:

```bash
sudo nano /var/www/html/comp370_hw2.txt
```

Add some content to the file, then save and exit.

Alternatively, you can transfer files from your local to the remote instance using scp (secure copy)

```bash
scp -i /path/to/private_key /path/to/local/file ubuntu@X.Y.Z.W:/home/ubuntu/
```
And then move the file to the correct directory:
```bash
sudo mv /home/ubuntu/comp370_hw2.html /var/www/html/
```

Set the correct permissions:

```bash
sudo chmod 644 /var/www/html/comp370_hw2.txt
```


## Step 5: **Restart Apache**

After making these changes, restart Apache:

```bash
sudo systemctl restart apache2
```

## Step 6: **Configure Lightsail Firewall**
Allow Port 8008 in the Lightsail Firewall:
1. Navigate to your Lightsail instance in the AWS console.
2. Under the Networking tab, find the IPv4 Firewall section.
3. Click Add another.
4. Set the application to Custom.
5. Set the protocol to TCP.
6. Enter 8008 in the port range.
7. Set the source to Any IPv4 address (0.0.0.0/0).
8. Save the rule.

## Step 8: **Test your setup**

Access your file by opening a web browser and navigating to:

```
http://X.Y.Z.W:8008/comp370_hw2.txt
```

Replace X.Y.Z.W with your EC2's public IP address.

## Troubleshooting

If you encounter issues, follow these troubleshooting steps:

1. Verify Apache is running:
   ```bash
   sudo systemctl status apache2
   ```

2. Check if Apache is listening on port 8008:
   ```bash
   sudo ss -tlnp | grep :8008
   ```

3. Verify the content of ports.conf:
   ```bash
   cat /etc/apache2/ports.conf
   ```
   Ensure it contains `Listen 8008`.

4. Check the content of 000-default.conf:
   ```bash
   cat /etc/apache2/sites-available/000-default.conf
   ```
   Ensure it starts with `<VirtualHost *:8008>`.

5. Verify UFW status and rules:
   ```bash
   sudo ufw status
   ```
   Ensure port 8008 is allowed.

6. Check file permissions:
   ```bash
   ls -l /var/www/html/comp370_hw2.txt
   ```
   Ensure it has the correct permissions (should be -rw-r--r--).

7. Check Apache error logs:
   ```bash
   sudo tail -n 50 /var/log/apache2/error.log
   ```


If you're still experiencing issues after these steps, consider the following:

- Try accessing the website from within the EC2 instance:
  ```bash
  curl http://localhost:8008/comp370_hw2.txt
  ```
  
- Check if Apache is configured to listen on port 8008. Run:
    ```bash
    sudo lsof -i -P -n | grep LISTEN
    ```

You should see something like this for port 8008:
    ```bash
    apache2  1337  www-data    4u  IPv4  1234567  0t0  TCP *:8008 (LISTEN)
    ```