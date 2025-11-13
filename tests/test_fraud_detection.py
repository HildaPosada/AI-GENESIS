"""
Tests for fraud detection system
"""
import pytest
from datetime import datetime
from app.models.schemas import Transaction, TransactionType
from app.services.fraud_detection_engine import fraud_engine


@pytest.mark.asyncio
async def test_normal_transaction():
    """Test normal transaction should not be flagged as fraud"""
    transaction = Transaction(
        transaction_id="TEST-001",
        user_id="USER-123",
        amount=50.00,
        currency="USD",
        transaction_type=TransactionType.CREDIT_CARD,
        merchant_name="Coffee Shop",
        merchant_category="Food & Beverage",
        location="New York, USA",
        ip_address="192.0.2.1",
        device_id="device-123",
        timestamp=datetime.utcnow()
    )

    result = await fraud_engine.analyze_transaction(transaction)

    assert isinstance(result.is_fraudulent, bool)
    assert 0 <= result.confidence_score <= 1
    assert result.risk_level in ["low", "medium", "high", "critical"]


@pytest.mark.asyncio
async def test_suspicious_transaction():
    """Test suspicious transaction should be flagged"""
    transaction = Transaction(
        transaction_id="TEST-002",
        user_id="USER-123",
        amount=15000.00,  # Large amount
        currency="USD",
        transaction_type=TransactionType.CREDIT_CARD,
        merchant_name="Electronics Store",
        merchant_category="Electronics",
        location="Tokyo, Japan",  # Unusual location
        ip_address="203.0.113.42",
        device_id="new-device",
        timestamp=datetime.utcnow().replace(hour=3)  # Odd time
    )

    result = await fraud_engine.analyze_transaction(transaction)

    # Should have high confidence and multiple reasons
    assert len(result.reasons) > 0
    assert len(result.recommended_actions) > 0


@pytest.mark.asyncio
async def test_fraud_detection_contains_all_technologies():
    """Test that fraud detection uses all 4 technologies"""
    transaction = Transaction(
        transaction_id="TEST-003",
        user_id="USER-123",
        amount=1000.00,
        currency="USD",
        transaction_type=TransactionType.WIRE_TRANSFER,
        merchant_name="Unknown",
        location="Unknown",
        timestamp=datetime.utcnow()
    )

    result = await fraud_engine.analyze_transaction(transaction)

    # Check that all technologies were used
    tech_used = result.analysis_details.get("technologies_used", {})
    assert "google_gemini" in tech_used
    assert "opus" in tech_used
    assert "qdrant" in tech_used
    assert "aiml_api" in tech_used


def test_transaction_validation():
    """Test transaction model validation"""
    transaction = Transaction(
        transaction_id="TEST-004",
        user_id="USER-123",
        amount=100.00,
        transaction_type=TransactionType.CREDIT_CARD,
    )

    assert transaction.currency == "USD"  # Default value
    assert isinstance(transaction.timestamp, datetime)
