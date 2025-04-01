#!/bin/bash

domains=(macaceres2.me www.macaceres2.me)
email="macaceres2@uc.cl"
data_path="./certbot"

# Create required directories
mkdir -p "$data_path/conf"
mkdir -p "$data_path/www"

# Stop existing containers
docker-compose down

# Start nginx with basic configuration
docker-compose up -d nginx

# Request certificates
docker-compose run --rm certbot certonly --webroot -w /var/www/certbot \
  --email $email \
  --agree-tos \
  --no-eff-email \
  -d ${domains[0]} -d ${domains[1]} \
  --force-renewal

# Reload nginx to use new certificates
docker-compose restart nginx