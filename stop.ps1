# Gradio FastAPI Django Main - Docker Compose Stop Script

Write-Host "🛑 Stopping Gradio FastAPI Django Main Application" -ForegroundColor Red

# Stop and remove containers
docker-compose down

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Application stopped successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to stop application properly." -ForegroundColor Red
}

# Optional: Remove unused volumes and images
$cleanup = Read-Host "Do you want to clean up unused Docker resources? (y/N)"
if ($cleanup -eq "y" -or $cleanup -eq "Y") {
    Write-Host "🧹 Cleaning up Docker resources..." -ForegroundColor Yellow
    docker system prune -f
    Write-Host "✅ Cleanup completed!" -ForegroundColor Green
}