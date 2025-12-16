# Deployment Script for SHL Assessment System
# Run this to deploy both API and Web App

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🚀 SHL ASSESSMENT RECOMMENDATION SYSTEM - DEPLOYMENT" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Change to project directory
$projectPath = "c:\Users\sirik\OneDrive\Desktop\SHL assignment"
Set-Location $projectPath

# Step 1: Check Python
Write-Host "1️⃣  Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = py --version
    Write-Host "   ✅ $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "   ❌ Python not found! Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Step 2: Install Dependencies
Write-Host ""
Write-Host "2️⃣  Installing dependencies..." -ForegroundColor Yellow
py -m pip install -r requirements.txt --quiet --disable-pip-version-check
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Dependencies installed" -ForegroundColor Green
}
else {
    Write-Host "   ⚠️  Some dependencies may have issues" -ForegroundColor Yellow
}

# Step 3: Check Vector Database
Write-Host ""
Write-Host "3️⃣  Checking vector database..." -ForegroundColor Yellow
if (Test-Path "data\vector_db\chroma.sqlite3") {
    Write-Host "   ✅ Vector database found ($(Get-ChildItem 'data\processed\assessments.csv' | Select-Object -ExpandProperty Length) bytes)" -ForegroundColor Green
}
else {
    Write-Host "   ⚠️  Vector database not found. Building now..." -ForegroundColor Yellow
    py src\embeddings\build_vector_db.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Vector database built successfully" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ Failed to build vector database" -ForegroundColor Red
    }
}

# Step 4: Check Data Files
Write-Host ""
Write-Host "4️⃣  Checking data files..." -ForegroundColor Yellow
if (Test-Path "data\processed\assessments.csv") {
    $lines = (Get-Content "data\processed\assessments.csv").Count
    Write-Host "   ✅ Assessment data found ($lines lines)" -ForegroundColor Green
}
else {
    Write-Host "   ❌ Assessment data not found!" -ForegroundColor Red
}

# Step 5: Kill existing processes
Write-Host ""
Write-Host "5️⃣  Stopping existing services..." -ForegroundColor Yellow
Get-Process | Where-Object { $_.ProcessName -like "*streamlit*" } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Write-Host "   ✅ Cleared existing services" -ForegroundColor Green

# Step 6: Start API Server
Write-Host ""
Write-Host "6️⃣  Starting API Server..." -ForegroundColor Yellow
$apiJob = Start-Job -ScriptBlock {
    Set-Location "c:\Users\sirik\OneDrive\Desktop\SHL assignment"
    py api_simple.py
}
Start-Sleep -Seconds 3
Write-Host "   ✅ API Server starting (Job ID: $($apiJob.Id))" -ForegroundColor Green
Write-Host "   📍 http://localhost:5000" -ForegroundColor Cyan

# Step 7: Start Web Application
Write-Host ""
Write-Host "7️⃣  Starting Web Application..." -ForegroundColor Yellow
Start-Process py -ArgumentList "-m streamlit run app.py" -WindowStyle Normal
Start-Sleep -Seconds 2
Write-Host "   ✅ Web App starting..." -ForegroundColor Green
Write-Host "   📍 http://localhost:8501" -ForegroundColor Cyan

# Step 8: Wait for services to start
Write-Host ""
Write-Host "8️⃣  Waiting for services to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Step 9: Health Check
Write-Host ""
Write-Host "9️⃣  Performing health checks..." -ForegroundColor Yellow
try {
    $apiHealth = Invoke-RestMethod -Uri "http://localhost:5000/health" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "   ✅ API is healthy: $($apiHealth.status)" -ForegroundColor Green
}
catch {
    Write-Host "   ⚠️  API may still be starting up..." -ForegroundColor Yellow
}

try {
    $webHealth = Invoke-WebRequest -Uri "http://localhost:8501/_stcore/health" -TimeoutSec 5 -ErrorAction SilentlyContinue
    if ($webHealth.StatusCode -eq 200) {
        Write-Host "   ✅ Web App is healthy" -ForegroundColor Green
    }
}
catch {
    Write-Host "   ⚠️  Web App may still be starting up..." -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "✅ DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 ACCESS YOUR APPLICATION:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   📱 Web Interface:  http://localhost:8501" -ForegroundColor Cyan
Write-Host "   🔌 API Endpoint:   http://localhost:5000/recommend" -ForegroundColor Cyan
Write-Host "   📄 API Test Page:  api_test.html (open in browser)" -ForegroundColor Cyan
Write-Host "   ❤️  Health Check:   http://localhost:5000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 Quick Test Commands:" -ForegroundColor Yellow
Write-Host ""
Write-Host '   Invoke-RestMethod http://localhost:5000/health' -ForegroundColor Gray
Write-Host '   Start-Process "http://localhost:8501"' -ForegroundColor Gray
Write-Host '   Start-Process "api_test.html"' -ForegroundColor Gray
Write-Host ""
Write-Host "🛑 To stop services:" -ForegroundColor Yellow
Write-Host '   Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process' -ForegroundColor Gray
Write-Host ""
Write-Host "📖 For deployment help: See DEPLOYMENT.md" -ForegroundColor Cyan
Write-Host ""

# Open browser automatically
Start-Sleep -Seconds 5
Write-Host "🌐 Opening web interface..." -ForegroundColor Green
Start-Process "http://localhost:8501"
