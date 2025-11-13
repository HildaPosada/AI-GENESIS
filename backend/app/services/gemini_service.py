"""
Google Gemini integration for multimodal fraud analysis
"""
import google.generativeai as genai
from typing import List, Dict, Any, Optional
import base64
from loguru import logger
from app.core.config import settings


class GeminiService:
    """Service for Google Gemini multimodal AI"""

    def __init__(self):
        if settings.GOOGLE_API_KEY:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            self.vision_model = genai.GenerativeModel('gemini-pro-vision')
        else:
            logger.warning("Google API key not configured")
            self.model = None
            self.vision_model = None

    async def analyze_transaction_pattern(
        self,
        transaction_data: Dict[str, Any],
        historical_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze transaction patterns for fraud using Gemini
        """
        if not self.model:
            return self._mock_analysis()

        try:
            prompt = f"""
            You are an expert fraud detection analyst. Analyze this transaction for potential fraud.

            Current Transaction:
            {transaction_data}

            User's Historical Transactions (last 10):
            {historical_data}

            Analyze for:
            1. Unusual spending patterns
            2. Geographic anomalies
            3. Time-based anomalies
            4. Amount anomalies
            5. Merchant type changes

            Respond in JSON format with:
            {{
                "is_suspicious": boolean,
                "confidence": float (0-1),
                "anomalies": [list of detected anomalies],
                "risk_factors": [list of risk factors],
                "explanation": "detailed explanation"
            }}
            """

            response = self.model.generate_content(prompt)
            # Parse response (in production, use structured output)
            return self._parse_gemini_response(response.text)

        except Exception as e:
            logger.error(f"Gemini analysis error: {e}")
            return self._mock_analysis()

    async def analyze_document(
        self,
        document_base64: str,
        document_type: str
    ) -> Dict[str, Any]:
        """
        Analyze documents (invoices, bank statements, IDs) for fraud
        Uses Gemini Vision for multimodal analysis
        """
        if not self.vision_model:
            return self._mock_document_analysis()

        try:
            prompt = f"""
            You are a document fraud detection expert. Analyze this {document_type} for signs of fraud.

            Look for:
            1. Document tampering or alterations
            2. Inconsistent fonts or formatting
            3. Suspicious amounts or dates
            4. Missing security features
            5. Forged signatures or stamps

            Respond in JSON format with:
            {{
                "is_fraudulent": boolean,
                "confidence": float (0-1),
                "fraud_indicators": [list of indicators],
                "authenticity_score": float (0-1),
                "recommendations": [list of recommendations]
            }}
            """

            # Decode base64 image
            image_data = base64.b64decode(document_base64)

            response = self.vision_model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_data}])
            return self._parse_gemini_response(response.text)

        except Exception as e:
            logger.error(f"Gemini document analysis error: {e}")
            return self._mock_document_analysis()

    async def generate_fraud_explanation(
        self,
        analysis_data: Dict[str, Any]
    ) -> str:
        """
        Generate human-readable explanation of fraud detection
        """
        if not self.model:
            return "Fraud detection analysis completed. API key required for detailed explanation."

        try:
            prompt = f"""
            Generate a clear, professional explanation of this fraud analysis for a compliance officer:

            Analysis Data:
            {analysis_data}

            Include:
            1. Summary of findings
            2. Key risk factors
            3. Recommended actions
            4. Regulatory considerations

            Keep it concise and actionable.
            """

            response = self.model.generate_content(prompt)
            return response.text

        except Exception as e:
            logger.error(f"Gemini explanation error: {e}")
            return "Analysis completed with detected anomalies."

    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response (simplified - use structured output in production)"""
        try:
            # Try to extract JSON from response
            import json
            import re

            # Find JSON in response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())

            # Fallback
            return {
                "raw_response": response_text,
                "parsed": False
            }
        except Exception as e:
            logger.error(f"Parse error: {e}")
            return {"error": str(e), "raw_response": response_text}

    def _mock_analysis(self) -> Dict[str, Any]:
        """Mock analysis for demo without API key"""
        return {
            "is_suspicious": True,
            "confidence": 0.82,
            "anomalies": [
                "Transaction amount 3x higher than average",
                "New geographic location detected",
                "Transaction outside normal hours"
            ],
            "risk_factors": [
                "Unusual spending pattern",
                "High-risk merchant category"
            ],
            "explanation": "Transaction shows multiple red flags requiring investigation"
        }

    def _mock_document_analysis(self) -> Dict[str, Any]:
        """Mock document analysis for demo"""
        return {
            "is_fraudulent": False,
            "confidence": 0.91,
            "fraud_indicators": [],
            "authenticity_score": 0.94,
            "recommendations": ["Document appears authentic", "No further action required"]
        }


# Singleton instance
gemini_service = GeminiService()
