"""
FastAPI application - AI Fraud Detection System
AI Genesis Hackathon 2025

Technologies:
1. Google Gemini - Multimodal AI
2. Opus - Workflow Automation
3. Qdrant - Vector Search
4. AI/ML API - Multi-model Access
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from app.core.config import settings
from app.api.routes import router

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    🚀 AI-Powered Financial Fraud Detection & Prevention System

    Built for AI Genesis Hackathon 2025

    ## Technologies Used:

    - 🧠 **Google Gemini**: Multimodal AI for pattern analysis & document verification
    - ⚙️ **Opus**: Workflow automation for regulated banking processes
    - 🔍 **Qdrant**: Vector similarity search for fraud pattern matching
    - 🤖 **AI/ML API**: Multi-model ensemble (GPT-4, Claude, LLama, Qwen)

    ## Features:

    - Real-time transaction fraud detection
    - Document fraud analysis (invoices, bank statements, IDs)
    - Automated investigation workflows
    - Historical fraud pattern matching
    - Explainable AI decisions
    - Compliance automation (AML, KYC, BSA)

    ## API Endpoints:

    - `POST /api/analyze/transaction` - Analyze transaction for fraud
    - `POST /api/analyze/document` - Analyze document for fraud
    - `POST /api/workflow/create` - Create investigation workflow
    - `GET /api/fraud-patterns/similar` - Find similar fraud patterns
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["Fraud Detection"])


@app.on_event("startup")
async def startup_event():
    """Startup tasks"""
    logger.info("=" * 60)
    logger.info("🚀 AI Fraud Detection System Starting...")
    logger.info("=" * 60)
    logger.info(f"App Name: {settings.APP_NAME}")
    logger.info(f"Version: {settings.APP_VERSION}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    logger.info("")
    logger.info("🔧 Technology Stack:")
    logger.info(f"  ✓ Google Gemini: {'Configured' if settings.GOOGLE_API_KEY else 'Mock Mode'}")
    logger.info(f"  ✓ Opus: {'Configured' if settings.OPUS_API_KEY else 'Mock Mode'}")
    logger.info(f"  ✓ Qdrant: {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
    logger.info(f"  ✓ AI/ML API: {'Configured' if settings.AIML_API_KEY else 'Mock Mode'}")
    logger.info("")
    logger.info("📚 Documentation available at: http://localhost:8000/docs")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup tasks"""
    logger.info("Shutting down AI Fraud Detection System...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
