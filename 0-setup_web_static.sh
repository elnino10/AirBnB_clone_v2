#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static

# update packet list
sudo apt update

# install nginx
sudo apt install -y nginx

# configure Uncomplicated Firewall
sudo ufw allow 'Nginx HTTP'

sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

# create fake content in index,html
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# create symlink
sudo ln -sf "/data/web_static/releases/test/" "/data/web_static/current"

# change ownership of /data/
sudo chown -R ubuntu:ubuntu /data/

# configure server to listen on port 80
echo "server {
        listen 80 default_server;
        listen [::]:80 default_server;
        server_name  _;

        location  /  {
                root     /var/www/html;
                index    index.html;
                add_header X-Served-By $HOSTNAME;
        }

	location /hbnb_static {
		alias /data/web_static/current/;
	}

        location  /redirect_me  {
                return 301 https://joe-chidiebere-portfolio.onrender.com/;
        }

        error_page 404 /404.html;
        location = /404.html  {
                root /var/www/html;
                internal;
                return 404 'Ceci n\'est pas une page\n';
        }
}"  |  sudo tee /etc/nginx/sites-available/default

# create a symbolic link 
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# test server before restart
sudo nginx -t

# restart Nginx server
sudo service nginx restart
