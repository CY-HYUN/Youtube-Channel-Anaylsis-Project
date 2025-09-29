# 🚀 Production Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the YouTube Channel Analysis Platform in production environments. It covers multiple deployment strategies, from single-server setups to enterprise-scale Kubernetes deployments.

## 📋 Prerequisites

### System Requirements

#### Minimum Requirements (Small-scale deployment)
- **CPU**: 2 cores
- **Memory**: 4GB RAM
- **Storage**: 50GB SSD
- **Network**: 100 Mbps
- **OS**: Ubuntu 20.04+ / CentOS 8+ / Docker-compatible

#### Recommended Requirements (Production-scale)
- **CPU**: 8 cores
- **Memory**: 16GB RAM
- **Storage**: 200GB SSD
- **Network**: 1 Gbps
- **OS**: Ubuntu 22.04 LTS

#### Enterprise Requirements (High-availability)
- **CPU**: 16+ cores
- **Memory**: 32GB+ RAM
- **Storage**: 500GB+ NVMe SSD
- **Network**: 10 Gbps
- **Load Balancer**: HA proxy or cloud LB

### Software Dependencies
```bash
# Core dependencies
Docker >= 20.10
Docker Compose >= 2.0
Python >= 3.8
Git >= 2.30

# Optional (for Kubernetes)
kubectl >= 1.20
helm >= 3.0
```

## 🐳 Docker Deployment (Recommended)

### 1. Quick Start with Docker Compose

#### Clone and Setup
```bash
# Clone the repository
git clone https://github.com/CY-HYUN/Youtube-Channel-Anaylsis-Project.git
cd Youtube-Channel-Anaylsis-Project

# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

#### Environment Configuration
```bash
# .env file configuration
YOUTUBE_API_KEY=your_youtube_api_key_here
DATABASE_URL=postgresql://user:password@postgres:5432/youtube_analytics
REDIS_URL=redis://redis:6379/0
APP_ENV=production
LOG_LEVEL=INFO
WORKERS=4

# Optional: Monitoring
GRAFANA_USER=admin
GRAFANA_PASSWORD=secure_admin_password
```

#### Deploy with Docker Compose
```bash
# Production deployment
docker-compose -f deployment/docker-compose.yml up -d

# Check services status
docker-compose ps

# View logs
docker-compose logs -f youtube-analytics
```

### 2. Production Docker Configuration

#### Custom Dockerfile Build
```bash
# Build production image
docker build -f deployment/Dockerfile -t youtube-analytics:latest .

# Run with production settings
docker run -d \
  --name youtube-analytics \
  --restart unless-stopped \
  -p 8000:8000 \
  -e YOUTUBE_API_KEY=${YOUTUBE_API_KEY} \
  -e DATABASE_URL=${DATABASE_URL} \
  -v /opt/youtube-analytics/data:/app/data \
  -v /opt/youtube-analytics/logs:/app/logs \
  youtube-analytics:latest
```

### 3. Multi-Container Production Setup

#### Service Architecture
```yaml
# deployment/docker-compose.prod.yml
services:
  app:
    image: youtube-analytics:latest
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
```

## ☸️ Kubernetes Deployment

### 1. Kubernetes Manifests

#### Namespace and ConfigMap
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: youtube-analytics

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: youtube-analytics-config
  namespace: youtube-analytics
data:
  APP_ENV: "production"
  LOG_LEVEL: "INFO"
  WORKERS: "4"
```

#### Secret Management
```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: youtube-analytics-secrets
  namespace: youtube-analytics
type: Opaque
data:
  youtube-api-key: <base64-encoded-key>
  database-url: <base64-encoded-url>
  redis-url: <base64-encoded-url>
```

#### Application Deployment
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: youtube-analytics
  namespace: youtube-analytics
spec:
  replicas: 3
  selector:
    matchLabels:
      app: youtube-analytics
  template:
    metadata:
      labels:
        app: youtube-analytics
    spec:
      containers:
      - name: youtube-analytics
        image: youtube-analytics:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: youtube-analytics-config
        - secretRef:
            name: youtube-analytics-secrets
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 2. Helm Chart Deployment

#### Install Helm Chart
```bash
# Add custom helm repository
helm repo add youtube-analytics ./helm

# Install with custom values
helm install youtube-analytics ./helm/youtube-analytics \
  --namespace youtube-analytics \
  --create-namespace \
  --values production-values.yaml
```

#### Production Helm Values
```yaml
# production-values.yaml
replicaCount: 3

image:
  repository: youtube-analytics
  tag: latest
  pullPolicy: Always

service:
  type: LoadBalancer
  port: 80

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: analytics.yourdomain.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: analytics-tls
      hosts:
        - analytics.yourdomain.com

resources:
  limits:
    cpu: 2000m
    memory: 4Gi
  requests:
    cpu: 1000m
    memory: 2Gi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

postgresql:
  enabled: true
  auth:
    database: youtube_analytics
    username: analytics_user
  primary:
    persistence:
      size: 100Gi

redis:
  enabled: true
  auth:
    enabled: false
  master:
    persistence:
      size: 20Gi
```

## 🏗️ Infrastructure as Code (Terraform)

### AWS Deployment
```hcl
# terraform/aws/main.tf
provider "aws" {
  region = var.aws_region
}

# EKS Cluster
module "eks" {
  source = "terraform-aws-modules/eks/aws"

  cluster_name    = "youtube-analytics"
  cluster_version = "1.21"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  node_groups = {
    main = {
      desired_capacity = 3
      max_capacity     = 10
      min_capacity     = 3

      instance_types = ["t3.large"]

      k8s_labels = {
        Environment = "production"
        Application = "youtube-analytics"
      }
    }
  }
}

# RDS Database
resource "aws_db_instance" "postgresql" {
  identifier = "youtube-analytics-db"

  engine         = "postgres"
  engine_version = "13.7"
  instance_class = "db.t3.micro"

  allocated_storage     = 100
  max_allocated_storage = 1000

  db_name  = "youtube_analytics"
  username = var.db_username
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Sun:04:00-Sun:05:00"

  skip_final_snapshot = false
  final_snapshot_identifier = "youtube-analytics-final-snapshot"

  tags = {
    Name = "youtube-analytics-db"
  }
}

# ElastiCache Redis
resource "aws_elasticache_subnet_group" "main" {
  name       = "youtube-analytics-cache-subnet"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "youtube-analytics-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis6.x"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.main.name
  security_group_ids   = [aws_security_group.redis.id]
}
```

## 🔧 Environment-Specific Configurations

### Development Environment
```bash
# development.env
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
ENABLE_CACHING=false
DATABASE_URL=sqlite:///./dev.db
REDIS_URL=redis://localhost:6379/0
```

### Staging Environment
```bash
# staging.env
APP_ENV=staging
DEBUG=false
LOG_LEVEL=INFO
ENABLE_CACHING=true
DATABASE_URL=postgresql://user:pass@staging-db:5432/analytics
REDIS_URL=redis://staging-redis:6379/0
SENTRY_DSN=https://staging-sentry-dsn
```

### Production Environment
```bash
# production.env
APP_ENV=production
DEBUG=false
LOG_LEVEL=WARNING
ENABLE_CACHING=true
DATABASE_URL=postgresql://user:pass@prod-db:5432/analytics
REDIS_URL=redis://prod-redis:6379/0
SENTRY_DSN=https://production-sentry-dsn
NEW_RELIC_LICENSE_KEY=your-key
```

## 📊 Monitoring and Logging Setup

### Prometheus Configuration
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: 'youtube-analytics'
    static_configs:
      - targets: ['app:8000']
    metrics_path: /metrics
    scrape_interval: 10s
```

### Grafana Dashboard Setup
```bash
# Import pre-configured dashboards
curl -X POST \
  -H "Content-Type: application/json" \
  -d @monitoring/grafana-dashboard.json \
  http://admin:password@grafana:3000/api/dashboards/db
```

### Log Aggregation
```yaml
# logging/fluentd.conf
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<match youtube.analytics.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  index_name youtube-analytics
  type_name logs
</match>
```

## 🛡️ Security Configuration

### SSL/TLS Setup
```bash
# Generate SSL certificates with Let's Encrypt
certbot certonly --webroot \
  -w /var/www/html \
  -d analytics.yourdomain.com \
  --email admin@yourdomain.com \
  --agree-tos \
  --non-interactive
```

### Nginx Security Configuration
```nginx
# nginx/security.conf
server {
    listen 443 ssl http2;
    server_name analytics.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/analytics.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/analytics.yourdomain.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔄 Backup and Recovery

### Database Backup Strategy
```bash
#!/bin/bash
# backup.sh
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/opt/backups"

# Create database backup
pg_dump $DATABASE_URL > "$BACKUP_DIR/db_backup_$DATE.sql"

# Compress backup
gzip "$BACKUP_DIR/db_backup_$DATE.sql"

# Upload to S3 (optional)
aws s3 cp "$BACKUP_DIR/db_backup_$DATE.sql.gz" \
  s3://your-backup-bucket/database/

# Cleanup old backups (keep last 30 days)
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +30 -delete
```

### Automated Backup with Cron
```bash
# Add to crontab
0 2 * * * /opt/scripts/backup.sh
0 6 * * 0 /opt/scripts/weekly_backup.sh
```

## 🚀 Deployment Automation

### CI/CD Pipeline (GitHub Actions)
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: |
          docker build -t youtube-analytics:${{ github.sha }} .
          docker tag youtube-analytics:${{ github.sha }} youtube-analytics:latest

      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push youtube-analytics:${{ github.sha }}
          docker push youtube-analytics:latest

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/youtube-analytics \
            youtube-analytics=youtube-analytics:${{ github.sha }} \
            --namespace=youtube-analytics
```

### Blue-Green Deployment
```bash
#!/bin/bash
# blue-green-deploy.sh

# Deploy to green environment
kubectl apply -f k8s/green-deployment.yaml

# Wait for green to be ready
kubectl rollout status deployment/youtube-analytics-green

# Switch traffic to green
kubectl patch service youtube-analytics \
  -p '{"spec":{"selector":{"version":"green"}}}'

# Cleanup blue environment
sleep 300  # Wait 5 minutes
kubectl delete deployment youtube-analytics-blue
```

## 📈 Performance Optimization

### Database Optimization
```sql
-- Create optimized indexes
CREATE INDEX CONCURRENTLY idx_videos_published_at ON videos(published_at);
CREATE INDEX CONCURRENTLY idx_channels_subscriber_count ON channels(subscriber_count);

-- Analyze table statistics
ANALYZE videos;
ANALYZE channels;
```

### Application Performance
```python
# Performance monitoring middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## 📋 Health Checks and Monitoring

### Application Health Check
```python
# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0",
        "database": await check_database_connection(),
        "redis": await check_redis_connection(),
        "youtube_api": await check_youtube_api()
    }
```

### Kubernetes Health Checks
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

## 🎯 Troubleshooting Guide

### Common Issues

#### 1. API Rate Limiting
```bash
# Check API quota usage
kubectl logs deployment/youtube-analytics | grep "quota"

# Increase rate limiting
kubectl patch configmap youtube-analytics-config \
  -p '{"data":{"RATE_LIMIT_PER_MINUTE":"120"}}'
```

#### 2. Database Connection Issues
```bash
# Check database connectivity
kubectl exec -it deployment/youtube-analytics -- \
  python -c "from src.database import check_connection; print(check_connection())"

# Check connection pool
kubectl top pods | grep postgres
```

#### 3. Memory Issues
```bash
# Check memory usage
kubectl top pods

# Increase memory limits
kubectl patch deployment youtube-analytics \
  -p '{"spec":{"template":{"spec":{"containers":[{"name":"youtube-analytics","resources":{"limits":{"memory":"8Gi"}}}]}}}}'
```

---

This deployment guide provides comprehensive instructions for production deployment across multiple environments and platforms. Follow the appropriate sections based on your infrastructure requirements and scaling needs.