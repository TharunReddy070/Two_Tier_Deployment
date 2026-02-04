# Two-Tier Flask Application - DevOps Project

A DevOps implementation demonstrating containerization and deployment of a two-tier web application using Docker, Docker Compose, and AWS EC2.

**Note**: The Flask application code was sourced from an existing repository. This project focuses on the DevOps implementation aspects.

## Table of Contents

- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Deployment Workflow](#deployment-workflow)
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [AWS EC2 Deployment](#aws-ec2-deployment)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

## Architecture

### System Design Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          AWS EC2 Instance                        │
│                                                                  │
│       Internet                                                   │
│          ↓                                                       │
│       Port 80                                                    │
│          ↓                                                       │
│  ┌──────────────────────────────────────────────────┐           │
│  │  Nginx (Installed on EC2)                        │           │
│  │  ┌────────────────────────────────────────────┐  │           │
│  │  │  - Serves static files directly from EC2  │  │           │
│  │  │  - Reverse proxy to Flask container        │  │           │
│  │  │  - Port: 80                                │  │           │
│  │  │  - Config: /etc/nginx/nginx.conf          │  │           │
│  │  └────────────────────────────────────────────┘  │           │
│  └────────────────────┬─────────────────────────────┘           │
│                       │ localhost:8181                          │
│                       ↓                                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Docker Environment                       │ │
│  │                                                             │ │
│  │  ┌─────────────────────────────────────┐                   │ │
│  │  │     Flask Container                 │                   │ │
│  │  │  ┌───────────────────────────────┐  │                   │ │
│  │  │  │  - Gunicorn WSGI Server       │  │                   │ │
│  │  │  │  - Flask Application          │  │                   │ │
│  │  │  │  - Business Logic             │  │                   │ │
│  │  │  │  - Port: 8181 (exposed)       │  │                   │ │
│  │  │  └───────────────────────────────┘  │                   │ │
│  │  └─────────────────┬───────────────────┘                   │ │
│  │                    │ Port 3306                             │ │
│  │                    ↓                                        │ │
│  │  ┌─────────────────────────────────────┐                   │ │
│  │  │     MySQL Container                 │                   │ │
│  │  │  ┌───────────────────────────────┐  │                   │ │
│  │  │  │  - MySQL 5.7 Database         │  │                   │ │
│  │  │  │  - Data Persistence           │  │                   │ │
│  │  │  │  - Port: 3306 (internal)      │  │                   │ │
│  │  │  └───────────────────────────────┘  │                   │ │
│  │  └─────────────────┬───────────────────┘                   │ │
│  │                    │                                        │ │
│  │                    ↓                                        │ │
│  │            Docker Volume (mysql_data)                       │ │
│  │                                                             │ │
│  │              Docker Bridge Network                          │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

          Local Development Machine               Docker Hub
                    ↓                                  ↓
          Build Images Locally      →→→→→    Push Images to Registry
                                              (devalapallitharun/*)
                                                       ↓
                                              Pull Images on EC2
```

**Components:**
- **Nginx** (on EC2): Entry point, serves static assets and proxies dynamic requests to Flask
- **Flask + Gunicorn** (containerized): Application layer handling business logic
- **MySQL** (containerized): Data persistence layer with volume mounting
- **Docker Network**: Isolated network for inter-container communication

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Application | Flask + Gunicorn |
| Web Server | Nginx (on EC2) |
| Database | MySQL 5.7 (containerized) |
| Containerization | Docker & Docker Compose |
| Registry | Docker Hub |
| Deployment | AWS EC2 |

## Deployment Workflow

1. **Local**: Build images using `docker-compose.yml`, push to Docker Hub
2. **Production**: Pull images on AWS EC2, run with `docker-compose.prod.yml`
3. **CI/CD**: Jenkinsfile included for practice (not used in production)

## Prerequisites

- Docker & Docker Compose
- Docker Hub account
- AWS EC2 instance (for production deployment)

## Local Setup

```bash
# Clone repository
git clone https://github.com/TharunReddy070/Two_Tier_Deployment.git
cd Two_Tier_Deployment

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Build and run
docker compose up --build -d

# Access application
# http://localhost

# Push to Docker Hub
docker login
docker compose push
```

## AWS EC2 Deployment

### Setup EC2 Instance

```bash
# Update system
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Nginx (directly on EC2, not containerized)
sudo apt-get install -y nginx
```

### Deploy Application

```bash
# Clone repository
cd /home/ubuntu
git clone https://github.com/TharunReddy070/Two_Tier_Deployment.git
cd Two_Tier_Deployment

# Create .env file with production credentials
nano .env
# Add your environment variables (see Environment Variables section)

# Configure Nginx
sudo cp nginx.conf /etc/nginx/nginx.conf
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
sudo systemctl enable nginx

# Start Docker containers (Flask and MySQL only)
docker-compose up -d

# Verify deployment
docker-compose ps
sudo systemctl status nginx
```

### Alternative: Automated Setup

Use the provided setup script:

```bash
cd /home/ubuntu/Two_Tier_Deployment
chmod +x ec2-setup.sh
./ec2-setup.sh
# Edit .env with your credentials
nano .env
docker-compose down && docker-compose up -d
```

### Security Group Configuration

- Port 22: SSH access
- Port 80: HTTP traffic

## Environment Variables

**⚠️ Security Best Practice**: This project uses environment variables for all sensitive credentials. **No default passwords are provided** to enforce proper configuration and prevent accidental use of weak credentials in production.

### Required Configuration

All credentials must be provided via environment variables. Create a `.env` file from the template:

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual credentials
# NEVER commit the .env file to version control
```

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MYSQL_ROOT_PASSWORD` | MySQL root password | Strong password (min 16 chars) |
| `MYSQL_DATABASE` | Database name | `crud_flask` |
| `MYSQL_USER` | Application database user | `app_user` |
| `MYSQL_PASSWORD` | Application user password | Strong password (min 16 chars) |
| `SECRET_KEY` | Flask secret key | Generate with: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `FLASK_ENV` | Flask environment | `development` or `production` |

### Environment-Specific Recommendations

**Development:**
```bash
MYSQL_ROOT_PASSWORD=dev_root_password_123
MYSQL_USER=dev_user
MYSQL_PASSWORD=dev_user_password_123
SECRET_KEY=dev_secret_key_for_testing_only
FLASK_ENV=development
```

**Production:**
- Use strong, randomly generated passwords (16+ characters)
- Generate secret key: `python -c "import secrets; print(secrets.token_hex(32))"`
- Set `FLASK_ENV=production`
- Store credentials in secure secret management systems (AWS Secrets Manager, HashiCorp Vault, etc.)
- Never commit `.env` files (already in `.gitignore`)

## Project Structure

```
Two_Tier_Deployment/
├── docker-compose.yml          # Orchestrates Flask and MySQL containers
├── dockerfile-flask            # Flask container build
├── dockerfile-mysql            # MySQL container build
├── dockerfile-nginx            # (Not used - Nginx on EC2)
├── nginx.conf                  # Nginx config (copied to /etc/nginx/)
├── ec2-setup.sh                # Automated EC2 setup script
├── DEPLOYMENT.md               # Detailed deployment guide
├── .env.example                # Environment template
├── database/
│   └── crud_flask.sql          # Database initialization
└── source_code/
    ├── requirements.txt
    ├── server.py
    ├── module/
    │   └── database.py
    ├── static/                 # CSS, JS, fonts (served by Nginx)
    └── templates/              # HTML templates
```

## Troubleshooting

**Check Nginx status:**
```bash
sudo systemctl status nginx
sudo nginx -t  # Test configuration
sudo tail -f /var/log/nginx/error.log
```

**Check container status:**
```bash
docker-compose ps
docker-compose logs flask-app
docker-compose logs phonebook-mysql
```

**Database connection issues:**
```bash
docker exec phonebook-mysql mysqladmin ping -h localhost
docker-compose restart flask-app
```

**Restart services:**
```bash
# Restart Nginx
sudo systemctl restart nginx

# Restart containers
docker-compose restart

# Full rebuild
docker-compose down
docker-compose up --build -d
```

## Author

**Tharun Reddy**  
GitHub: [@TharunReddy070](https://github.com/TharunReddy070)
