# Deployment Guide

## Prerequisites

- Docker & Docker Compose (for containerized deployment)
- PostgreSQL 15+ (for database)
- Domain name with SSL certificate (for production)
- Google Cloud account (for Cloud Run deployment)

---

## 🐳 Docker Deployment (Recommended)

### Local Development

```bash
# 1. Clone repository
git clone <repository-url>
cd ai-factguard-studio

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys and settings

# 3. Start services
docker-compose up -d

# 4. Check status
docker-compose ps

# 5. View logs
docker-compose logs -f

# 6. Stop services
docker-compose down
```

### Production Docker

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start with production config
docker-compose -f docker-compose.prod.yml up -d

# Database migration
docker-compose exec backend alembic upgrade head
```

---

## ☁️ Google Cloud Run Deployment

### Backend Deployment

```bash
# 1. Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# 2. Login and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 3. Deploy backend
cd backend
gcloud run deploy factguard-api \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL="postgresql://..." \
  --set-env-vars GEMINI_API_KEY="..." \
  --memory 2Gi \
  --cpu 2

# 4. Get backend URL
gcloud run services describe factguard-api --format='value(status.url)'
```

### Frontend Deployment

```bash
# 1. Update API URL
# Edit frontend/.env.production
NEXT_PUBLIC_API_URL=https://your-backend-url.run.app/api

# 2. Deploy frontend
cd frontend
gcloud run deploy factguard-app \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 512Mi

# 3. Get frontend URL
gcloud run services describe factguard-app --format='value(status.url)'
```

### Database Setup (CloudSQL)

```bash
# Create PostgreSQL instance
gcloud sql instances create factguard-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1

# Create database
gcloud sql databases create factguard_db --instance=factguard-db

# Set password
gcloud sql users set-password postgres \
  --instance=factguard-db \
  --password=YOUR_SECURE_PASSWORD

# Connect backend to CloudSQL
# Add to backend Cloud Run service:
# --add-cloudsql-instances=PROJECT_ID:us-central1:factguard-db
```

---

## 🔧 Traditional VPS Deployment

### Ubuntu 22.04 Server

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
sudo apt install -y python3.11 python3.11-venv nodejs npm postgresql nginx

# 3. Clone repository
git clone <repository-url> /var/www/factguard
cd /var/www/factguard

# 4. Setup backend
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Setup database
sudo -u postgres createdb factguard_db
sudo -u postgres createuser factguard

# 6. Configure environment
cp .env.example .env
# Edit .env with production values

# 7. Setup systemd service for backend
sudo nano /etc/systemd/system/factguard-api.service
```

**factguard-api.service:**
```ini
[Unit]
Description=FactGuard API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/factguard/backend
Environment="PATH=/var/www/factguard/backend/venv/bin"
ExecStart=/var/www/factguard/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Start backend service
sudo systemctl enable factguard-api
sudo systemctl start factguard-api

# 8. Setup frontend
cd /var/www/factguard/frontend
npm install
npm run build

# 9. Install PM2 for frontend
sudo npm install -g pm2
pm2 start npm --name "factguard-app" -- start
pm2 save
pm2 startup
```

### Nginx Configuration

```nginx
# /etc/nginx/sites-available/factguard
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeout for long analysis
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
    }

    # File upload size
    client_max_body_size 100M;
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/factguard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL with Certbot
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 🔐 Security Checklist

- [ ] Change default database credentials
- [ ] Generate strong secret keys
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable firewall (UFW)
- [ ] Regular security updates
- [ ] Implement authentication
- [ ] API key rotation
- [ ] Database backups

---

## 📊 Monitoring

### Health Checks

```bash
# Backend health
curl https://your-api.com/health

# Check logs
docker-compose logs -f backend
# or
sudo journalctl -u factguard-api -f
```

### Performance Monitoring

Consider integrating:
- **Sentry**: Error tracking
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Google Cloud Monitoring**: For Cloud Run

---

## 🔄 Updates & Maintenance

```bash
# Pull latest code
cd /var/www/factguard
git pull

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart factguard-api

# Update frontend
cd ../frontend
npm install
npm run build
pm2 restart factguard-app
```

---

## 🆘 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -h localhost -U factguard -d factguard_db
```

### Port Conflicts
```bash
# Check port usage
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :3000
```

### Memory Issues
```bash
# Increase Docker memory limit
# Edit docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 4G
```

---

## 📝 Backup Strategy

```bash
# Database backup
pg_dump -h localhost -U factguard factguard_db > backup_$(date +%Y%m%d).sql

# Automated backups with cron
0 2 * * * pg_dump -h localhost -U factguard factguard_db > /backups/factguard_$(date +\%Y\%m\%d).sql
```

---

## 🎯 Production Best Practices

1. **Database**: Use managed PostgreSQL (CloudSQL, RDS)
2. **File Storage**: Use object storage (Google Cloud Storage, S3)
3. **CDN**: Serve static assets via CDN
4. **Caching**: Implement Redis for session/cache
5. **Load Balancing**: Multiple backend instances
6. **Auto-scaling**: Configure based on traffic
7. **Logging**: Centralized log management
8. **Monitoring**: Real-time alerts
