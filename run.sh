#!/bin/bash

# AI Fraud Detection System - Startup Script

echo "🚀 Starting AI Fraud Detection System..."
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file. Please add your API keys to .env"
    echo ""
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "🐳 Starting services with Docker Compose..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 5

echo ""
echo "✅ Services started successfully!"
echo ""
echo "📚 Access points:"
echo "   - API Documentation: http://localhost:8000/docs"
echo "   - Frontend Dashboard: http://localhost:3000"
echo "   - Qdrant Dashboard: http://localhost:6333/dashboard"
echo ""
echo "🔧 Technology Stack:"
echo "   ✓ Google Gemini (Multimodal AI)"
echo "   ✓ Opus (Workflow Automation)"
echo "   ✓ Qdrant (Vector Search)"
echo "   ✓ AI/ML API (Multi-model Access)"
echo ""
echo "📝 View logs with: docker-compose logs -f"
echo "🛑 Stop with: docker-compose down"
echo ""
