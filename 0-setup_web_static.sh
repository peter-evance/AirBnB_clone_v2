#!/usr/bin/env bash
# a Bash script that sets up your web servers for the deployment of web_static
# - Installs nginx if it doesn't exist
# - Sets up /var/www/html to serve content to our server
# - /data/web_static to server web_static content to server
if [ ! -x /etc/nginx ]; then
    apt-get update
    apt-get install -y nginx
fi

#creating the /var/ directory structure
if [ ! -d "/var/" ]; then
	mkdir /var
fi

if [ ! -d "/var/www/" ]; then
	mkdir /var/www
fi

if [ ! -d "/var/www/html/" ]; then
	mkdir /var/www/html
fi

if [ ! -f "/var/www/html/index.html" ]; then
	echo "Hello World" > /var/www/html/index.html
fi

# creating the /data/ directory structure
if [ ! -d "/data/" ]; then
        mkdir /data
fi

if [ ! -d "/data/web_static/" ]; then
        mkdir /data/web_static
fi

if [ ! -d "/data/web_static/releases/" ]; then
        mkdir /data/web_static/releases
fi

if [ ! -d "/data/web_static/shared/" ]; then
        mkdir /data/web_static/shared
fi

if [ ! -d "/data/web_static/releases/test/" ]; then
        mkdir /data/web_static/releases/test
fi

if [ ! -f "/data/web_static/releases/test/index.html" ]; then
        echo "<h1>Test website for AirBnB Project</h1>" > /data/web_static/releases/test/index.html
fi

if [ -L "/data/web_static/current" ]; then
        rm -rf /data/web_static/current
fi

ln -s /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

printf %s "server {
    listen 80;
    listen [::]:80 default_server;
    root   /var/www/html;
    index  index.html index.htm;
    add_header X-Served-By $HOSTNAME;
    location /redirect_me {
        return 301 http://youtube.com/;
    }
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
    location /hbnb_static{
    alias /data/web_static/current;
    }
}" > /etc/nginx/sites-available/default

service nginx restart
