#!/bin/bash
# ==============================================================================
# Automated AWS EC2 Deployment Script for Portfolio Web Application
# Target OS: Ubuntu 22.04 LTS / Ubuntu 24.04 LTS / Amazon Linux 2023
# ==============================================================================

set -e

echo "🚀 Starting Automated AWS EC2 Portfolio Deployment..."

# 1. Update package manager
echo "📦 Updating system packages..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update -y
    sudo apt-get install -y curl git docker.io docker-compose
elif command -v dnf &> /dev/null; then
    sudo dnf update -y
    sudo dnf install -y docker git
    sudo systemctl enable --now docker
    # Install docker-compose standalone binary
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# 2. Ensure current user is in docker group
echo "👤 Configuring Docker permissions..."
sudo usermod -aG docker $USER || true
sudo systemctl enable docker
sudo systemctl start docker

# 3. Create persistent database and log files if they don't exist yet
echo "🗄️ Initializing storage volume files..."
touch portfolio.db
touch notifications.log

if [ ! -f .env ]; then
    echo "📄 Creating default .env file..."
    cp .env.example .env
fi

# 4. Build and start containers
echo "🐳 Building Docker image and starting container..."
sudo docker-compose down || true
sudo docker-compose up -d --build

# 5. Check container status
echo "🔍 Checking container health..."
sudo docker-compose ps

echo "=============================================================================="
echo "🎉 DEPLOYMENT COMPLETE!"
echo "Your portfolio is now running live on AWS EC2!"
echo "Access it in your browser at: http://$(curl -s ifconfig.me)"
echo "=============================================================================="
