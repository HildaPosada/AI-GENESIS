"""
Data models and schemas for fraud detection
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    """Transaction types"""
    CREDIT_CARD = "credit_card"
    WIRE_TRANSFER = "wire_transfer"
    ACH = "ach"
    CRYPTO = "crypto"
    CASH_WITHDRAWAL = "cash_withdrawal"


class FraudType(str, Enum):
    """Fraud types detected"""
    IDENTITY_THEFT = "identity_theft"
    CARD_FRAUD = "card_fraud"
    MONEY_LAUNDERING = "money_laundering"
    ACCOUNT_TAKEOVER = "account_takeover"
    SYNTHETIC_IDENTITY = "synthetic_identity"
    PHISHING = "phishing"
    UNKNOWN = "unknown"


class Transaction(BaseModel):
    """Transaction data model"""
    transaction_id: str
    user_id: str
    amount: float
    currency: str = "USD"
    transaction_type: TransactionType
    merchant_name: Optional[str] = None
    merchant_category: Optional[str] = None
    location: Optional[str] = None
    ip_address: Optional[str] = None
    device_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None


class DocumentAnalysisRequest(BaseModel):
    """Request for document fraud analysis"""
    document_type: str  # "invoice", "bank_statement", "id_card", etc.
    document_url: Optional[str] = None
    document_base64: Optional[str] = None
    user_id: str
    metadata: Optional[Dict[str, Any]] = None


class FraudAnalysisResult(BaseModel):
    """Fraud analysis result"""
    is_fraudulent: bool
    confidence_score: float
    fraud_type: FraudType
    risk_level: str  # "low", "medium", "high", "critical"
    reasons: List[str]
    similar_cases: List[Dict[str, Any]] = []
    recommended_actions: List[str]
    analysis_details: Dict[str, Any]


class WorkflowRequest(BaseModel):
    """Workflow automation request for Opus"""
    workflow_type: str  # "fraud_investigation", "account_review", "transaction_verification"
    transaction_id: Optional[str] = None
    case_id: Optional[str] = None
    priority: str = "medium"  # "low", "medium", "high", "urgent"
    additional_context: Optional[Dict[str, Any]] = None


class WorkflowResponse(BaseModel):
    """Workflow automation response"""
    workflow_id: str
    status: str
    steps_completed: List[str]
    current_step: str
    next_actions: List[str]
    estimated_completion: Optional[datetime] = None
    results: Optional[Dict[str, Any]] = None


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    services: Dict[str, bool]
    version: str
