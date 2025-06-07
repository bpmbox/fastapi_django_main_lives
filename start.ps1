# Gradio FastAPI Django Main - Docker Compose Start Script
# Based on README.md configuration: Gradio 4.29.0, app.py

Write-Host "🦀 Starting Gradio FastAPI Django Main Application" -ForegroundColor Cyan
Write-Host "Emoji: 🦀" -ForegroundColor Yellow
Write-Host "SDK: Gradio 4.29.0" -ForegroundColor Green
Write-Host "App File: app.py" -ForegroundColor Blue

# Check if Docker is running
if (!(Get-Process "Docker Desktop" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Desktop is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Build and start the containers
Write-Host "🔨 Building and starting containers..." -ForegroundColor Cyan
docker-compose up --build -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Application started successfully!" -ForegroundColor Green
    Write-Host "🌐 Application is running at: http://localhost:7860" -ForegroundColor Blue
    Write-Host "📊 Container status:" -ForegroundColor Yellow
    docker-compose ps
    
    Write-Host "`n📝 To view logs: docker-compose logs -f" -ForegroundColor Cyan
    Write-Host "🛑 To stop: docker-compose down" -ForegroundColor Cyan
} else {
    Write-Host "❌ Failed to start application. Check the logs:" -ForegroundColor Red
    docker-compose logs
}