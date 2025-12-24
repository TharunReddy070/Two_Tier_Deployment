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
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Docker Environment                       │ │
│  │                                                             │ │
│  │   Internet                                                  │ │
│  │      ↓                                                      │ │
│  │   Port 80                                                   │ │
│  │      ↓                                                      │ │
│  │  ┌─────────────────────────────────────┐                   │ │
│  │  │     Nginx Container                 │                   │ │
│  │  │  ┌───────────────────────────────┐  │                   │ │
│  │  │  │  - Serves static files        │  │                   │ │
│  │  │  │    (CSS, JS, Images)          │  │                   │ │
│  │  │  │  - Reverse proxy to Flask     │  │                   │ │
│  │  │  │  - Port: 80                   │  │                   │ │
│  │  │  └───────────────────────────────┘  │                   │ │
│  │  └─────────────────┬───────────────────┘                   │ │
│  │                    │ Port 8181                             │ │
│  │                    ↓                                        │ │
│  │  ┌─────────────────────────────────────┐                   │ │
│  │  │     Flask Container                 │                   │ │
│  │  │  ┌───────────────────────────────┐  │                   │ │
│  │  │  │  - Gunicorn WSGI Server       │  │                   │ │
│  │  │  │  - Flask Application          │  │                   │ │
│  │  │  │  - Business Logic             │  │                   │ │
│  │  │  │  - Port: 8181                 │  │                   │ │
│  │  │  └───────────────────────────────┘  │                   │ │
│  │  └─────────────────┬───────────────────┘                   │ │
│  │                    │ Port 3306                             │ │
│  │                    ↓                                        │ │
│  │  ┌─────────────────────────────────────┐                   │ │
│  │  │     MySQL Container                 │                   │ │
│  │  │  ┌───────────────────────────────┐  │                   │ │
│  │  │  │  - MySQL 5.7 Database         │  │                   │ │
│  │  │  │  - Data Persistence           │  │                   │ │
│  │  │  │  - Port: 3306                 │  │                   │ │
│  │  │  └───────────────────────────────┘  │                   │ │
│  │  └─────────────────┬───────────────────┘                   │ │
│  │                    │                                        │ │
│  │                    ↓                                        │ │
│  │            Docker Volume (mysql_data)                       │ │
│  │                                                             │ │
│  │              Docker Bridge Network                          │ │
│  │          (phonebook-net / default)                          │ │
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
- **Nginx**: Entry point, serves static assets and proxies dynamic requests
- **Flask + Gunicorn**: Application layer handling business logic
- **MySQL**: Data persistence layer with volume mounting
- **Docker Network**: Isolated network for inter-container communication

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Application | Flask + Gunicorn |
| Web Server | Nginx |
| Database | MySQL 5.7 |
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
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Deploy Application

```bash
# Create deployment directory
mkdir -p ~/phonebook-deploy
cd ~/phonebook-deploy

# Create docker-compose.prod.yml (modify from local version)
# Create .env file with production credentials

# Pull and run
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

### Security Group Configuration

- Port 22: SSH access
- Port 80: HTTP traffic

## Environment Variables

Required variables (see `.env.example`):

```
MYSQL_ROOT_PASSWORD=<secure_password>
MYSQL_DATABASE=crud_flask
MYSQL_USER=dev
MYSQL_PASSWORD=<secure_password>
SECRET_KEY=<random_string_32+_chars>
DB_HOST=phonebook-mysql
DB_USER=dev
DB_PASSWORD=<secure_password>
DB_NAME=crud_flask
```

## Project Structure

```
Two_Tier_Deployment/
├── docker-compose.yml          # Local development
├── dockerfile-flask            # Flask container
├── dockerfile-mysql            # MySQL container
├── dockerfile-nginx            # Nginx container
├── jenkinsfile                 # CI/CD pipeline (practice)
├── nginx.conf                  # Nginx configuration
├── .env.example                # Environment template
├── database/
│   └── crud_flask.sql          # Database initialization
└── source_code/
    ├── requirements.txt
    ├── server.py
    ├── module/
    │   └── database.py
    ├── static/                 # CSS, JS, fonts
    └── templates/              # HTML templates
```

## Troubleshooting

**Check container status:**
```bash
docker compose ps
docker compose logs <service_name>
```

**Database connection issues:**
```bash
docker exec phonebook-mysql mysqladmin ping -h localhost
docker compose restart flask-app
```

**Rebuild containers:**
```bash
docker compose down
docker compose up --build -d
```

## Author

**Tharun Reddy**  
GitHub: [@TharunReddy070](https://github.com/TharunReddy070)
