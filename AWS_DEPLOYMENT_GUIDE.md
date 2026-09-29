# ☁️ AWS Deployment Guide for Rajat Bandhral's Portfolio

This guide provides step-by-step instructions to deploy your portfolio on **Amazon Web Services (AWS)** using **AWS EC2**, **Security Groups**, **Docker**, **SQLite**, and **SMTP Email Notifications** sent to `rajatrajput076@gmail.com`.

---

## 🛠️ AWS Services Utilized

- **AWS EC2 (Elastic Compute Cloud)**: Free Tier (`t2.micro` or `t3.micro`) Linux server hosting your application.
- **AWS Security Groups (VPC)**: Virtual firewall controlling inbound HTTP (80), HTTPS (443), and SSH (22) traffic.
- **AWS IAM & Key Pairs**: Secure authentication for server management.
- **Terraform (Optional IaC)**: Automated infrastructure provisioning using HashiCorp Terraform.

---

## 📋 OPTION 1: Deploying via AWS Management Console (Recommended for Beginners)

### Step 1: Launch your AWS EC2 Instance
1. Log into your [AWS Management Console](https://console.aws.amazon.com/ec2).
2. Go to **EC2** -> Click **Launch Instance**.
3. Fill in the details:
   - **Name**: `Rajat-DevOps-Portfolio`
   - **OS Image**: Select **Ubuntu 24.04 LTS** (or 22.04 LTS).
   - **Instance Type**: Select `t2.micro` (or `t3.micro` - **Free Tier Eligible**).
   - **Key Pair**: Select an existing key pair or click **Create new key pair** (`rajat-key.pem`). Download and save this `.pem` file on your computer.

### Step 2: Configure AWS Security Group (Firewall)
Under **Network Settings**, click **Edit** and ensure these 3 rules exist:

| Type | Protocol | Port Range | Source | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **SSH** | TCP | `22` | My IP or `0.0.0.0/0` | Terminal access |
| **HTTP** | TCP | `80` | `0.0.0.0/0` | Public web access |
| **HTTPS**| TCP | `443` | `0.0.0.0/0` | Secure SSL access |

Click **Launch Instance**.

---

### Step 3: Connect to Your EC2 Instance

#### Method A: Browser-based EC2 Instance Connect (Easiest)
1. In AWS Console, select your `Rajat-DevOps-Portfolio` instance.
2. Click **Connect** (top right) -> Select **EC2 Instance Connect** -> Click **Connect**.

#### Method B: Terminal SSH
```bash
chmod 400 rajat-key.pem
ssh -i rajat-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

---

### Step 4: Transfer Project Code to AWS EC2

#### Option A: Via Git
```bash
git clone https://github.com/your-username/portfolio.git
cd portfolio
```

#### Option B: Upload directly from Windows via `scp`
Run this command from your Windows PowerShell:
```powershell
scp -i "C:\path\to\rajat-key.pem" -r "C:\Users\lenov0\.gemini\antigravity\scratch\portfolio" ubuntu@YOUR_EC2_PUBLIC_IP:~/portfolio
```

---

### Step 5: Execute 1-Click Automated Deployment Script

On your AWS EC2 terminal inside the `portfolio` folder:

```bash
chmod +x deploy-aws.sh
./deploy-aws.sh
```

**What this script automates:**
- Installs Docker & Docker Compose on Ubuntu
- Configures persistent SQLite storage (`portfolio.db`)
- Builds and starts your container on Port 80

---

### Step 6: Configure SMTP Email Notifications

1. Edit the `.env` file on your EC2 server:
   ```bash
   nano .env
   ```
2. Enter your Gmail credentials so notifications land directly in `rajatrajput076@gmail.com`:
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=rajatrajput076@gmail.com
   SENDER_PASSWORD=your_16_char_gmail_app_password
   RECEIVER_EMAIL=rajatrajput076@gmail.com
   ```
   > 💡 **Generating a Gmail App Password:**
   > Go to [Google Account Security](https://myaccount.google.com/security) -> Enable **2-Step Verification** -> Search for **App Passwords** -> Create a password named `Portfolio Server` -> Copy the 16-character code.

3. Restart the Docker container:
   ```bash
   sudo docker-compose restart
   ```

---

### Step 7: Test Your Live Portfolio!

Open your browser and navigate to:
`http://YOUR_EC2_PUBLIC_IP`

Fill out the **"Write Your Details"** contact box:
1. Submission is stored instantly in `portfolio.db`.
2. An email notification is sent to **rajatrajput076@gmail.com**.
3. View the entry anytime by clicking **"DB Messages"** in the top navbar!

---

## 🏗️ OPTION 2: Automated Infrastructure as Code (IaC) via Terraform

Since you are a **DevOps Engineer**, you can also provision your entire AWS infrastructure using the included Terraform module inside `terraform/`:

1. Install Terraform on your local machine or AWS CloudShell:
2. Navigate to `terraform/`:
   ```bash
   cd terraform
   terraform init
   terraform plan
   terraform apply -auto-approve
   ```
3. Terraform will provision the Security Group, EC2 Instance, and output your live website URL!
