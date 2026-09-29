# 🔒 Step-by-Step Guide: Enable HTTPS (SSL/TLS) on Live AWS EC2

This guide explains how to secure your portfolio on AWS EC2 with a **free Let's Encrypt HTTPS (SSL) Certificate** using **Nginx** and **Certbot**.

---

## 🎯 How HTTPS Works on AWS EC2

```
Visitor Browser (https://yourdomain.com)
       │
       ▼ (Port 443 - SSL Secured)
  [ AWS Security Group ]
       │
       ▼
 [ Nginx Reverse Proxy (Certbot SSL) ]  <-- Terminates SSL Encryption
       │
       ▼ (Port 8000 Internal)
[ Docker Container (Flask / Gunicorn) ]
```

---

## 📋 Step 1: Ensure Port 443 (HTTPS) is Open in AWS

1. Log into **AWS EC2 Console** -> Go to **Instances**.
2. Select your `Rajat-DevOps-Portfolio` instance -> Click the **Security** tab -> Click your **Security Group**.
3. Under **Inbound Rules**, click **Edit inbound rules** and ensure these 3 rules are enabled:

| Type | Protocol | Port Range | Source | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **SSH** | TCP | `22` | `0.0.0.0/0` | Terminal SSH access |
| **HTTP** | TCP | `80` | `0.0.0.0/0` | Web HTTP & SSL validation |
| **HTTPS**| TCP | `443` | `0.0.0.0/0` | **Secure HTTPS Web Traffic** |

Click **Save rules**.

---

## 🌐 Step 2: Point Your Domain to Your EC2 Public IP

To get a valid HTTPS certificate, Let's Encrypt requires a domain name pointing to your EC2 instance's Public IPv4 IP.

### Option A: If you own a Domain (GoDaddy, Namecheap, Route 53, Cloudflare, etc.)
1. Go to your domain provider's **DNS Management** page.
2. Add an **A Record**:
   - **Type**: `A`
   - **Name / Host**: `@` (and another for `www`)
   - **Value / Target**: `YOUR_EC2_PUBLIC_IP` (e.g. `54.210.12.34`)
   - **TTL**: `Automatic` or `300`

### Option B: If you DON'T own a domain yet (Use Free DuckDNS Subdomain)
You can get a 100% free domain in 1 minute using [DuckDNS](https://www.duckdns.org):
1. Sign in to [DuckDNS.org](https://www.duckdns.org).
2. Create a domain name like `rajat-portfolio` (Full domain: `rajat-portfolio.duckdns.org`).
3. Set the IP address to your **AWS EC2 Public IP**.

---

## 🚀 Step 3: Run the Automated HTTPS Setup Script on EC2

Connect to your EC2 instance terminal via SSH or EC2 Instance Connect, navigate to your `portfolio` directory, and execute `setup-https.sh`:

```bash
cd portfolio
chmod +x setup-https.sh
./setup-https.sh yourdomain.com rajatrajput076@gmail.com
```

*(Replace `yourdomain.com` with your actual domain or free DuckDNS domain, e.g., `rajat-portfolio.duckdns.org`).*

### What `setup-https.sh` Does Automatically:
1. Installs **Nginx**, **Certbot**, and the Nginx SSL plugin.
2. Binds the Docker application container to internal port `8000`.
3. Configures Nginx as a high-performance reverse proxy.
4. Obtains a free **Let's Encrypt SSL/TLS Certificate**.
5. Configures automatic HTTP to HTTPS redirect (`http://` -> `https://`).
6. Enables automatic SSL certificate renewal via systemd timer.

---

## ✅ Step 4: Verify Your Live HTTPS Site

Open your web browser and visit:
`https://yourdomain.com` (or `https://rajat-portfolio.duckdns.org`)

You will see:
- 🔒 **Security Padlock Icon** in your browser address bar.
- Valid 256-bit SSL encryption.
- Instant submission storage in SQLite + email dispatching to `rajatrajput076@gmail.com`.
