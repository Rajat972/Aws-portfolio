#!/bin/bash
# ==============================================================================
# Automated HTTPS SSL Certificate Setup Script for AWS EC2
# Target OS: Ubuntu 22.04 LTS / Ubuntu 24.04 LTS
# Uses Nginx + Certbot (Let's Encrypt)
# ==============================================================================

set -e

if [ -z "$1" ]; then
    echo "❌ Error: Please provide your domain name."
    echo "Usage: ./setup-https.sh yourdomain.com [your-email@example.com]"
    echo "Example: ./setup-https.sh rajatdevops.com rajatrajput076@gmail.com"
    exit 1
fi

DOMAIN="$1"
EMAIL="${2:-rajatrajput076@gmail.com}"

echo "🔒 Starting HTTPS SSL Setup for domain: $DOMAIN..."

# 1. Install Nginx and Certbot
echo "📦 Installing Nginx, Certbot, and Python Certbot plugin..."
sudo apt-get update -y
sudo apt-get install -y nginx certbot python3-certbot-nginx

# 2. Reconfigure Docker container port to 8000 so Nginx can bind to Port 80 & 443
echo "⚙️ Reconfiguring Docker port mapping to 8000..."
cat << 'EOF' > docker-compose.override.yml
version: '3.8'
services:
  portfolio-web:
    ports:
      - "127.0.0.1:8000:8000"
EOF

sudo docker-compose down || true
sudo docker-compose up -d --build

# 3. Create Nginx Configuration for Domain
echo "📄 Generating Nginx reverse proxy configuration..."
sudo cat << EOF > /etc/nginx/sites-available/portfolio
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/portfolio
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

# 4. Request Let's Encrypt SSL Certificate via Certbot
echo "🔑 Requesting Let's Encrypt SSL Certificate for $DOMAIN..."
sudo certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos -m "$EMAIL" --redirect

# 5. Enable Certbot Auto-Renewal Timer
echo "🔄 Setting up SSL auto-renewal cron timer..."
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

echo "=============================================================================="
echo "🎉 HTTPS SETUP COMPLETE!"
echo "Your portfolio is now securely running live with SSL!"
echo "Access it securely at: https://$DOMAIN"
echo "=============================================================================="
