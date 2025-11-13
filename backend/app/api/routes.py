"""
API routes for fraud detection system
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from datetime import datetime

from app.models.schemas import (
    Transaction,
    DocumentAnalysisRequest,
    FraudAnalysisResult,
    WorkflowRequest,
    WorkflowResponse,
    HealthCheck
)
from app.services.fraud_detection_engine import fraud_engine
from app.services.opus_service import opus_service
from app.services.qdrant_service import qdrant_service
from app.core.config import settings
from loguru import logger

router = APIRouter()


@router.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "AI Fraud Detection System - AI Genesis Hackathon",
        "version": settings.APP_VERSION,
        "technologies": "Google Gemini + Opus + Qdrant + AI/ML API"
    }


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    services = {
        "gemini": bool(settings.GOOGLE_API_KEY),
        "opus": bool(settings.OPUS_API_KEY),
        "qdrant": True,  # Always available with mock
        "aiml_api": bool(settings.AIML_API_KEY)
    }

    return HealthCheck(
        status="healthy",
        timestamp=datetime.utcnow(),
        services=services,
        version=settings.APP_VERSION
    )


@router.post("/analyze/transaction", response_model=FraudAnalysisResult)
async def analyze_transaction(transaction: Transaction):
    """
    Analyze a transaction for fraud using all 4 technologies:

    1. **Google Gemini**: Multimodal pattern analysis
    2. **AI/ML API**: Multi-model ensemble (GPT-4, Claude, LLama)
    3. **Qdrant**: Vector similarity search for fraud patterns
    4. **Opus**: Automated investigation workflow (if fraud detected)

    Returns comprehensive fraud analysis with recommendations.
    """
    try:
        logger.info(f"Received transaction analysis request: {transaction.transaction_id}")
        result = await fraud_engine.analyze_transaction(transaction)
        return result
    except Exception as e:
        logger.error(f"Transaction analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/document", response_model=FraudAnalysisResult)
async def analyze_document(request: DocumentAnalysisRequest):
    """
    Analyze documents for fraud (invoices, bank statements, IDs)

    Uses **Google Gemini Vision** for multimodal document analysis
    """
    try:
        logger.info(f"Received document analysis request: {request.document_type}")

        if not request.document_base64 and not request.document_url:
            raise HTTPException(
                status_code=400,
                detail="Either document_base64 or document_url must be provided"
            )

        # For demo, use base64 or fetch from URL
        document_data = request.document_base64 or "MOCK_BASE64_DATA"

        result = await fraud_engine.analyze_document(
            document_base64=document_data,
            document_type=request.document_type,
            user_id=request.user_id
        )
        return result
    except Exception as e:
        logger.error(f"Document analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflow/create", response_model=Dict[str, Any])
async def create_workflow(request: WorkflowRequest):
    """
    Create fraud investigation workflow using **Opus**

    Opus automates critical processes in regulated banking:
    - Compliance checks (AML, KYC, BSA)
    - Risk assessment
    - Case routing
    - Document verification
    """
    try:
        logger.info(f"Creating workflow: {request.workflow_type}")

        case_data = {
            "workflow_type": request.workflow_type,
            "transaction_id": request.transaction_id,
            "case_id": request.case_id or f"CASE-AUTO-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "priority": request.priority,
            "additional_context": request.additional_context or {}
        }

        workflow = await opus_service.create_fraud_investigation_workflow(
            case_data=case_data,
            priority=request.priority
        )

        return workflow
    except Exception as e:
        logger.error(f"Workflow creation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workflow/{workflow_id}", response_model=Dict[str, Any])
async def get_workflow_status(workflow_id: str):
    """Get status of fraud investigation workflow"""
    try:
        status = await opus_service.get_workflow_status(workflow_id)
        return status
    except Exception as e:
        logger.error(f"Workflow status error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fraud-patterns/similar", response_model=List[Dict[str, Any]])
async def find_similar_patterns(
    transaction_text: str,
    limit: int = 5
):
    """
    Find similar fraud patterns using **Qdrant** vector search

    Performs semantic similarity search across historical fraud cases
    """
    try:
        from app.services.aiml_service import aiml_service

        # Generate embedding
        embedding = await aiml_service.generate_embedding(transaction_text)

        # Search similar cases
        similar_cases = await qdrant_service.find_similar_fraud_cases(
            embedding,
            limit=limit
        )

        return similar_cases
    except Exception as e:
        logger.error(f"Similarity search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fraud-patterns/statistics", response_model=Dict[str, Any])
async def get_fraud_statistics():
    """Get statistics about stored fraud patterns (Qdrant)"""
    try:
        stats = await qdrant_service.get_fraud_statistics()
        return stats
    except Exception as e:
        logger.error(f"Statistics error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/demo/generate-sample-transaction", response_model=Transaction)
async def generate_sample_transaction(fraud_type: str = "normal"):
    """
    Generate sample transaction for testing

    fraud_type: normal, suspicious, fraud
    """
    from app.models.schemas import TransactionType
    import uuid

    if fraud_type == "fraud":
        return Transaction(
            transaction_id=f"TXN-{uuid.uuid4().hex[:8].upper()}",
            user_id="USER-12345",
            amount=15000.00,  # Unusually high
            currency="USD",
            transaction_type=TransactionType.CREDIT_CARD,
            merchant_name="Electronics Store",
            merchant_category="Electronics",
            location="Tokyo, Japan",  # Unusual location
            ip_address="203.0.113.42",
            device_id="new-device-unknown",
            timestamp=datetime.utcnow().replace(hour=3, minute=30)  # Odd time
        )
    elif fraud_type == "suspicious":
        return Transaction(
            transaction_id=f"TXN-{uuid.uuid4().hex[:8].upper()}",
            user_id="USER-12345",
            amount=2500.00,
            currency="USD",
            transaction_type=TransactionType.WIRE_TRANSFER,
            merchant_name="Unknown Recipient",
            merchant_category="Transfer",
            location="Unknown",
            ip_address="198.51.100.123",
            timestamp=datetime.utcnow()
        )
    else:  # normal
        return Transaction(
            transaction_id=f"TXN-{uuid.uuid4().hex[:8].upper()}",
            user_id="USER-12345",
            amount=45.99,
            currency="USD",
            transaction_type=TransactionType.CREDIT_CARD,
            merchant_name="Coffee Shop",
            merchant_category="Food & Beverage",
            location="New York, USA",
            ip_address="192.0.2.1",
            device_id="regular-device-123",
            timestamp=datetime.utcnow()
        )
