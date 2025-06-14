# 🦀 Gradio FastAPI Django Main - Docker Setup

Based on the configuration in README.md:
- **Title**: Gradio fastapi_django_main
- **Emoji**: 🦀
- **SDK**: Gradio 4.29.0
- **App File**: app.py

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- PowerShell (Windows) or Bash (Linux/macOS)

### 🚀 Start Application
```powershell
# Windows
.\start.ps1

# Or manually:
docker-compose up --build -d
```

### 🛑 Stop Application
```powershell
# Windows
.\stop.ps1

# Or manually:
docker-compose down
```

## Configuration

### Environment Variables
Copy `.env.example` to `.env` and update the values:

```bash
# Groq API Configuration
OPENAI_API_BASE=https://api.groq.com/openai/v1
OPENAI_API_KEY=your_actual_api_key_here
MODEL_NAME=llama3-8b-8192
LOCAL_MODEL=true

# Gradio Configuration
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
```

## Services

### Main Application
- **Container**: `gradio-fastapi-django-main`
- **Port**: 7860
- **URL**: http://localhost:7860

### Features
- Gradio 4.29.0 Web Interface
- FastAPI Backend
- Django Integration
- Groq API Support
- Health Checks
- Auto-restart on failure

## Docker Commands

```bash
# Build only
docker-compose build

# Start in foreground (see logs)
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Stop and remove
docker-compose down

# Rebuild and start
docker-compose up --build

# Clean up everything
docker-compose down -v --remove-orphans
docker system prune -f
```

## Troubleshooting

### Container won't start
1. Check Docker Desktop is running
2. Check logs: `docker-compose logs`
3. Verify `.env` file exists and has correct values
4. Ensure port 7860 is not in use

### API Key Issues
1. Update `OPENAI_API_KEY` in `.env` file
2. Restart containers: `docker-compose restart`

### Performance Issues
1. Allocate more memory to Docker Desktop
2. Check container resources: `docker stats`

## Development

### Local Development with Docker
```bash
# Mount source code for live reloading
docker-compose -f docker-compose.dev.yml up
```

### Access Container Shell
```bash
docker-compose exec gradio-fastapi-django bash
```