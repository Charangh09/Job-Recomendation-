# 🚀 Deployment Guide - SHL Assessment Recommendation System

## Quick Deployment Options

### Option 1: Local Deployment (Fastest)

#### Step 1: Install Dependencies
```powershell
cd "c:\Users\sirik\OneDrive\Desktop\SHL assignment"
py -m pip install -r requirements.txt
```

#### Step 2: Deploy Both Services
```powershell
# Start API Server (Port 5000)
Start-Process py -ArgumentList "api_simple.py" -WindowStyle Normal

# Start Web App (Port 8501)
Start-Process py -ArgumentList "-m streamlit run app.py" -WindowStyle Normal
```

#### Step 3: Access the Application
- **Web Interface**: http://localhost:8501
- **API Endpoint**: http://localhost:5000/recommend
- **API Test Page**: Open `api_test.html` in browser

---

### Option 2: Production Deployment (Cloud)

#### For Streamlit Cloud (Free)

1. **Push to GitHub**:
```powershell
git init
git add .
git commit -m "SHL Assessment System"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

2. **Deploy on Streamlit Cloud**:
   - Go to https://share.streamlit.io
   - Connect your GitHub repository
   - Select `app.py` as main file
   - Click Deploy

3. **Add Secrets** (if needed):
   - In Streamlit Cloud dashboard
   - Add `OPENAI_API_KEY` if using LLM features

#### For Heroku

1. **Create Procfile**:
```
web: sh setup.sh && streamlit run app.py --server.port=$PORT
api: gunicorn api_simple:app
```

2. **Create setup.sh**:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

3. **Deploy**:
```powershell
heroku login
heroku create shl-assessment-system
git push heroku main
```

---

### Option 3: Docker Deployment

#### Step 1: Build Docker Image
```powershell
docker build -t shl-assessment-system .
```

#### Step 2: Run Container
```powershell
# Run Web App
docker run -d -p 8501:8501 --name shl-web shl-assessment-system streamlit run app.py

# Run API
docker run -d -p 5000:5000 --name shl-api shl-assessment-system python api_simple.py
```

---

## Deployment Checklist

### Pre-Deployment
- [ ] All dependencies installed
- [ ] Vector database built (data/vector_db/)
- [ ] Data files present (data/processed/assessments.csv)
- [ ] Configuration updated (config.yaml)
- [ ] Environment variables set (if using OpenAI)

### Post-Deployment
- [ ] Test API endpoint: `curl http://localhost:5000/health`
- [ ] Test web app: Open http://localhost:8501
- [ ] Verify search functionality
- [ ] Check error logs
- [ ] Monitor performance

---

## Environment Variables

Create `.env` file:
```env
OPENAI_API_KEY=your_key_here_if_needed
FLASK_ENV=production
STREAMLIT_SERVER_PORT=8501
API_SERVER_PORT=5000
```

---

## Production Configuration

### For Production Use:

1. **Update config.yaml**:
```yaml
server:
  host: 0.0.0.0
  port: 5000
  debug: false

retrieval:
  top_k: 10
  similarity_threshold: 0.1
```

2. **Enable HTTPS** (if deploying to cloud)
3. **Add Authentication** (if required)
4. **Setup Monitoring** (logs, metrics)

---

## Scaling Options

### Horizontal Scaling
- Deploy multiple API instances behind a load balancer
- Use Redis for caching query results
- Deploy vector DB separately (e.g., Pinecone, Weaviate)

### Optimization
- Use GPU for faster embeddings (if available)
- Cache frequent queries
- Implement CDN for static assets

---

## Monitoring & Logs

### Check Logs:
```powershell
# API logs
Get-Content api.log -Tail 50 -Wait

# Streamlit logs
Get-Content streamlit.log -Tail 50 -Wait
```

### Health Checks:
```powershell
# API Health
Invoke-RestMethod http://localhost:5000/health

# Web App Health
Invoke-WebRequest http://localhost:8501/_stcore/health
```

---

## Troubleshooting

### Common Issues:

1. **Port Already in Use**:
```powershell
# Find process on port 5000
Get-NetTCPConnection -LocalPort 5000
# Kill process
Stop-Process -Id PROCESS_ID -Force
```

2. **Vector DB Not Found**:
```powershell
py src/embeddings/build_vector_db.py
```

3. **Dependencies Missing**:
```powershell
py -m pip install -r requirements.txt --upgrade
```

---

## Quick Deploy Script

Save as `deploy.ps1`:
```powershell
Write-Host "🚀 Deploying SHL Assessment System..." -ForegroundColor Green

# Check dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
py -m pip install -r requirements.txt -q

# Build vector DB if needed
if (!(Test-Path "data/vector_db")) {
    Write-Host "🔨 Building vector database..." -ForegroundColor Yellow
    py src/embeddings/build_vector_db.py
}

# Start services
Write-Host "🌐 Starting services..." -ForegroundColor Yellow
Start-Process py -ArgumentList "api_simple.py" -WindowStyle Minimized
Start-Sleep -Seconds 5
Start-Process py -ArgumentList "-m streamlit run app.py" -WindowStyle Normal

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "📍 Web App: http://localhost:8501" -ForegroundColor Cyan
Write-Host "📍 API: http://localhost:5000" -ForegroundColor Cyan
```

Run:
```powershell
.\deploy.ps1
```

---

## URLs for Access

After deployment:
- **Main Web App**: http://localhost:8501
- **API Endpoint**: http://localhost:5000/recommend
- **API Documentation**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **Test Interface**: Open `api_test.html`

---

## Next Steps

1. ✅ Deploy locally for testing
2. ✅ Test all functionality
3. ✅ Choose cloud platform (Streamlit Cloud, Heroku, AWS)
4. ✅ Configure domain name (optional)
5. ✅ Setup monitoring
6. ✅ Share with stakeholders

---

**🎉 Your system is ready to deploy!**
