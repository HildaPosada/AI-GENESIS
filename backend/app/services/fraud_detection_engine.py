"""
Core Fraud Detection Engine
Integrates ALL 4 hackathon technologies:
1. Google Gemini - Multimodal analysis
2. Opus - Workflow automation
3. Qdrant - Vector similarity search
4. AI/ML API - Multi-model ensemble
"""
from typing import Dict, Any, List
from loguru import logger
from datetime import datetime
import uuid

from app.services.gemini_service import gemini_service
from app.services.opus_service import opus_service
from app.services.qdrant_service import qdrant_service
from app.services.aiml_service import aiml_service
from app.models.schemas import Transaction, FraudAnalysisResult, FraudType


class FraudDetectionEngine:
    """
    Comprehensive fraud detection system using all 4 technologies
    """

    def __init__(self):
        self.gemini = gemini_service
        self.opus = opus_service
        self.qdrant = qdrant_service
        self.aiml = aiml_service

    async def analyze_transaction(
        self,
        transaction: Transaction,
        historical_data: List[Dict[str, Any]] = None
    ) -> FraudAnalysisResult:
        """
        Complete fraud analysis pipeline using all 4 technologies
        """
        logger.info(f"Analyzing transaction: {transaction.transaction_id}")

        case_id = f"CASE-{uuid.uuid4().hex[:8].upper()}"

        # Step 1: Multi-model analysis via AI/ML API
        logger.info("Step 1: Running multi-model ensemble analysis (AI/ML API)")
        transaction_dict = transaction.dict()
        aiml_analysis = await self.aiml.analyze_with_multiple_models(
            transaction_dict,
            models=["gpt-4", "claude-3-opus", "llama-3"]
        )

        # Step 2: Gemini multimodal analysis
        logger.info("Step 2: Running Gemini pattern analysis")
        if historical_data is None:
            historical_data = self._get_mock_history(transaction.user_id)

        gemini_analysis = await self.gemini.analyze_transaction_pattern(
            transaction_dict,
            historical_data
        )

        # Step 3: Generate embedding and search for similar cases (Qdrant)
        logger.info("Step 3: Searching similar fraud patterns (Qdrant)")
        transaction_text = self._transaction_to_text(transaction)
        embedding = await self.aiml.generate_embedding(transaction_text)
        similar_cases = await self.qdrant.find_similar_fraud_cases(
            embedding,
            limit=5,
            score_threshold=0.7
        )

        # Step 4: Combine all analyses
        logger.info("Step 4: Combining analyses and making decision")
        fraud_decision = self._make_fraud_decision(
            aiml_analysis,
            gemini_analysis,
            similar_cases
        )

        # Step 5: If fraud detected, create investigation workflow (Opus)
        workflow_info = None
        if fraud_decision["is_fraudulent"]:
            logger.info("Step 5: Creating fraud investigation workflow (Opus)")
            workflow_info = await self.opus.create_fraud_investigation_workflow(
                case_data={
                    "case_id": case_id,
                    "transaction_id": transaction.transaction_id,
                    "user_id": transaction.user_id,
                    "fraud_type": fraud_decision["fraud_type"],
                    "risk_level": fraud_decision["risk_level"],
                    "confidence": fraud_decision["confidence_score"]
                },
                priority="high" if fraud_decision["risk_level"] == "critical" else "medium"
            )

        # Step 6: Store case in vector database for future matching
        if fraud_decision["is_fraudulent"]:
            logger.info("Step 6: Storing fraud case (Qdrant)")
            await self.qdrant.store_fraud_case(
                case_id=case_id,
                fraud_type=fraud_decision["fraud_type"],
                embedding=embedding,
                metadata={
                    "transaction_id": transaction.transaction_id,
                    "user_id": transaction.user_id,
                    "amount": transaction.amount,
                    "timestamp": transaction.timestamp.isoformat()
                }
            )

        # Step 7: Generate explanation (Gemini)
        logger.info("Step 7: Generating human-readable explanation (Gemini)")
        explanation = await self.gemini.generate_fraud_explanation({
            "case_id": case_id,
            "transaction": transaction_dict,
            "analysis": fraud_decision,
            "similar_cases": similar_cases
        })

        # Build final result
        result = FraudAnalysisResult(
            is_fraudulent=fraud_decision["is_fraudulent"],
            confidence_score=fraud_decision["confidence_score"],
            fraud_type=FraudType(fraud_decision["fraud_type"]),
            risk_level=fraud_decision["risk_level"],
            reasons=fraud_decision["reasons"],
            similar_cases=similar_cases,
            recommended_actions=fraud_decision["recommended_actions"],
            analysis_details={
                "case_id": case_id,
                "aiml_ensemble": aiml_analysis,
                "gemini_analysis": gemini_analysis,
                "similar_cases_count": len(similar_cases),
                "workflow": workflow_info,
                "explanation": explanation,
                "technologies_used": {
                    "google_gemini": "Pattern analysis & explanation generation",
                    "opus": "Automated investigation workflow" if workflow_info else "Not triggered",
                    "qdrant": f"Found {len(similar_cases)} similar cases",
                    "aiml_api": f"Ensemble of {len(aiml_analysis.get('individual_models', {}))} models"
                }
            }
        )

        logger.info(f"Analysis complete: Fraud={result.is_fraudulent}, Confidence={result.confidence_score}")
        return result

    async def analyze_document(
        self,
        document_base64: str,
        document_type: str,
        user_id: str
    ) -> FraudAnalysisResult:
        """
        Analyze documents for fraud (invoices, bank statements, IDs)
        Uses Gemini Vision for multimodal document analysis
        """
        logger.info(f"Analyzing {document_type} document for user {user_id}")

        # Use Gemini Vision for document analysis
        gemini_doc_analysis = await self.gemini.analyze_document(
            document_base64,
            document_type
        )

        # Generate embedding for similarity search
        doc_description = f"{document_type} fraud analysis: {gemini_doc_analysis}"
        embedding = await self.aiml.generate_embedding(doc_description)

        # Search for similar document fraud cases
        similar_cases = await self.qdrant.find_similar_fraud_cases(
            embedding,
            limit=3
        )

        is_fraudulent = gemini_doc_analysis.get("is_fraudulent", False)
        confidence = gemini_doc_analysis.get("confidence", 0.5)

        # Create workflow if fraud detected
        workflow_info = None
        if is_fraudulent and confidence > 0.7:
            case_id = f"DOC-{uuid.uuid4().hex[:8].upper()}"
            workflow_info = await self.opus.create_fraud_investigation_workflow(
                case_data={
                    "case_id": case_id,
                    "user_id": user_id,
                    "fraud_type": "document_fraud",
                    "document_type": document_type,
                    "confidence": confidence
                },
                priority="high"
            )

        return FraudAnalysisResult(
            is_fraudulent=is_fraudulent,
            confidence_score=confidence,
            fraud_type=FraudType.IDENTITY_THEFT if is_fraudulent else FraudType.UNKNOWN,
            risk_level=self._calculate_risk_level(confidence),
            reasons=gemini_doc_analysis.get("fraud_indicators", []),
            similar_cases=similar_cases,
            recommended_actions=gemini_doc_analysis.get("recommendations", []),
            analysis_details={
                "document_type": document_type,
                "gemini_analysis": gemini_doc_analysis,
                "workflow": workflow_info,
                "authenticity_score": gemini_doc_analysis.get("authenticity_score", 0)
            }
        )

    def _make_fraud_decision(
        self,
        aiml_analysis: Dict[str, Any],
        gemini_analysis: Dict[str, Any],
        similar_cases: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Combine all analyses to make final fraud decision
        """
        # Get ensemble decision from AI/ML API
        ensemble = aiml_analysis.get("ensemble_decision", {})
        aiml_fraud_prob = ensemble.get("fraud_probability", 0.5)
        aiml_confidence = ensemble.get("confidence", 0.7)

        # Get Gemini analysis
        gemini_suspicious = gemini_analysis.get("is_suspicious", False)
        gemini_confidence = gemini_analysis.get("confidence", 0.5)

        # Boost if similar fraud cases found
        similarity_boost = 0.15 if len(similar_cases) > 0 else 0

        # Calculate final fraud score
        final_fraud_score = (
            (aiml_fraud_prob * 0.5) +
            (gemini_confidence if gemini_suspicious else (1 - gemini_confidence)) * 0.35 +
            similarity_boost * 0.15
        )

        # Calculate final confidence
        final_confidence = (aiml_confidence + gemini_confidence) / 2

        # Determine if fraudulent
        is_fraudulent = final_fraud_score > 0.7

        # Collect all reasons
        reasons = []
        reasons.extend(ensemble.get("risk_factors", []))
        reasons.extend(gemini_analysis.get("anomalies", []))
        if similar_cases:
            reasons.append(f"Similar to {len(similar_cases)} known fraud patterns")

        # Determine fraud type
        fraud_type = self._determine_fraud_type(
            similar_cases,
            gemini_analysis,
            aiml_analysis
        )

        # Calculate risk level
        risk_level = self._calculate_risk_level(final_fraud_score)

        # Recommended actions
        recommended_actions = self._get_recommended_actions(
            is_fraudulent,
            risk_level,
            fraud_type
        )

        return {
            "is_fraudulent": is_fraudulent,
            "confidence_score": round(final_confidence, 2),
            "fraud_type": fraud_type,
            "risk_level": risk_level,
            "reasons": list(set(reasons))[:5],  # Top 5 unique reasons
            "recommended_actions": recommended_actions,
            "scores": {
                "aiml_ensemble": aiml_fraud_prob,
                "gemini_analysis": gemini_confidence if gemini_suspicious else 0,
                "similarity_boost": similarity_boost,
                "final_score": final_fraud_score
            }
        }

    def _determine_fraud_type(
        self,
        similar_cases: List[Dict[str, Any]],
        gemini_analysis: Dict[str, Any],
        aiml_analysis: Dict[str, Any]
    ) -> str:
        """Determine the type of fraud"""
        # Check similar cases
        if similar_cases:
            fraud_types = [case.get("type", "unknown") for case in similar_cases]
            most_common = max(set(fraud_types), key=fraud_types.count)
            return most_common

        # Default
        return "card_fraud"

    def _calculate_risk_level(self, score: float) -> str:
        """Calculate risk level from score"""
        if score >= 0.9:
            return "critical"
        elif score >= 0.75:
            return "high"
        elif score >= 0.5:
            return "medium"
        else:
            return "low"

    def _get_recommended_actions(
        self,
        is_fraudulent: bool,
        risk_level: str,
        fraud_type: str
    ) -> List[str]:
        """Get recommended actions based on analysis"""
        if not is_fraudulent:
            return ["Transaction approved", "Continue monitoring"]

        actions = []

        if risk_level in ["critical", "high"]:
            actions.append("IMMEDIATE: Block transaction")
            actions.append("IMMEDIATE: Freeze account pending investigation")
            actions.append("Contact customer via verified phone number")

        actions.extend([
            "Create fraud investigation case",
            "Review recent transaction history",
            "Verify customer identity",
            "Check for similar patterns in other accounts"
        ])

        if fraud_type == "money_laundering":
            actions.append("File Suspicious Activity Report (SAR)")

        return actions

    def _transaction_to_text(self, transaction: Transaction) -> str:
        """Convert transaction to text for embedding"""
        return f"""
        Transaction: {transaction.transaction_type}
        Amount: {transaction.amount} {transaction.currency}
        Merchant: {transaction.merchant_name or 'Unknown'}
        Location: {transaction.location or 'Unknown'}
        Time: {transaction.timestamp}
        """

    def _get_mock_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get mock historical transactions"""
        return [
            {"amount": 45.20, "merchant": "Coffee Shop", "time": "2025-11-10 08:30"},
            {"amount": 120.00, "merchant": "Grocery Store", "time": "2025-11-09 18:00"},
            {"amount": 35.50, "merchant": "Gas Station", "time": "2025-11-08 12:00"},
            {"amount": 89.99, "merchant": "Online Retailer", "time": "2025-11-07 20:00"},
            {"amount": 250.00, "merchant": "Restaurant", "time": "2025-11-06 19:30"}
        ]


# Singleton instance
fraud_engine = FraudDetectionEngine()
