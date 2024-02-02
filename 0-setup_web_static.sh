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
echo "Test Content" | sudo tee /data/web_static/releases/test/index.html

# create symlink
sudo ln -sf "/data/web_static/releases/test/" "/data/web_static/current"

# change ownership of /data/
sudo chown -R ubuntu:ubuntu /path/

# configure server to listen on port 80
sudo sed -i '/listen 80 default_server;/a location \/hbnb_static { alias /data/web_static/current/; }' /etc/nginx/sites-enabled/default

# test server before restart
sudo nginx -t

# restart Nginx server
sudo service nginx restart
