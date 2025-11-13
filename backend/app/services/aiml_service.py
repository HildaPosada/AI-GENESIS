"""
AI/ML API integration for accessing 100+ models
(OpenAI, Anthropic, LLama, Qwen, etc.)
"""
import httpx
from typing import Dict, Any, List, Optional
from loguru import logger
from app.core.config import settings
import json


class AIMLService:
    """Service for AI/ML API - unified access to multiple AI models"""

    def __init__(self):
        self.api_key = settings.AIML_API_KEY
        self.base_url = "https://api.aimlapi.com/v1"  # Hypothetical
        self.client = httpx.AsyncClient(timeout=60.0)

    async def analyze_with_multiple_models(
        self,
        transaction_data: Dict[str, Any],
        models: List[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze transaction using multiple AI models for ensemble detection

        Available models via AI/ML API:
        - GPT-4, GPT-3.5 (OpenAI)
        - Claude 3 (Anthropic)
        - LLama 2, LLama 3 (Meta)
        - Qwen (Alibaba)
        - And 100+ more
        """
        if models is None:
            models = ["gpt-4", "claude-3-opus", "llama-3"]

        if not self.api_key:
            return self._mock_multi_model_analysis(transaction_data, models)

        try:
            results = {}

            for model in models:
                analysis = await self._analyze_with_model(transaction_data, model)
                results[model] = analysis

            # Ensemble decision
            ensemble_result = self._ensemble_decision(results)
            return ensemble_result

        except Exception as e:
            logger.error(f"Multi-model analysis error: {e}")
            return self._mock_multi_model_analysis(transaction_data, models)

    async def _analyze_with_model(
        self,
        transaction_data: Dict[str, Any],
        model: str
    ) -> Dict[str, Any]:
        """Analyze with a specific model"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        prompt = f"""
        Analyze this financial transaction for fraud:

        {json.dumps(transaction_data, indent=2)}

        Provide:
        1. Fraud probability (0-1)
        2. Key risk factors
        3. Confidence level

        Respond in JSON format.
        """

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are an expert fraud detection AI."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }

        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                return self._parse_model_response(data, model)
            else:
                return {"model": model, "error": "API error"}

        except Exception as e:
            logger.error(f"Model {model} error: {e}")
            return {"model": model, "error": str(e)}

    def _parse_model_response(
        self,
        response_data: Dict[str, Any],
        model: str
    ) -> Dict[str, Any]:
        """Parse model response"""
        try:
            content = response_data["choices"][0]["message"]["content"]
            # Parse JSON from content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                parsed["model"] = model
                return parsed
            return {"model": model, "raw_response": content}
        except Exception as e:
            return {"model": model, "error": f"Parse error: {e}"}

    def _ensemble_decision(
        self,
        model_results: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Combine multiple model predictions into ensemble decision
        """
        fraud_probs = []
        confidence_scores = []
        all_risk_factors = []

        for model, result in model_results.items():
            if "error" not in result:
                fraud_probs.append(result.get("fraud_probability", 0.5))
                confidence_scores.append(result.get("confidence", 0.7))
                all_risk_factors.extend(result.get("risk_factors", []))

        if not fraud_probs:
            return {"error": "All models failed"}

        avg_fraud_prob = sum(fraud_probs) / len(fraud_probs)
        avg_confidence = sum(confidence_scores) / len(confidence_scores)

        # Unique risk factors
        unique_risk_factors = list(set(all_risk_factors))

        return {
            "ensemble_decision": {
                "fraud_probability": avg_fraud_prob,
                "confidence": avg_confidence,
                "is_fraudulent": avg_fraud_prob > 0.7,
                "risk_factors": unique_risk_factors,
                "models_used": list(model_results.keys()),
                "agreement_level": self._calculate_agreement(fraud_probs)
            },
            "individual_models": model_results
        }

    def _calculate_agreement(self, probabilities: List[float]) -> str:
        """Calculate model agreement level"""
        if not probabilities:
            return "unknown"

        variance = sum((p - sum(probabilities) / len(probabilities)) ** 2 for p in probabilities) / len(probabilities)

        if variance < 0.01:
            return "high"
        elif variance < 0.05:
            return "medium"
        else:
            return "low"

    async def generate_embedding(
        self,
        text: str,
        model: str = "text-embedding-3-large"
    ) -> List[float]:
        """
        Generate embeddings for vector storage
        """
        if not self.api_key:
            return self._mock_embedding(text)

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": model,
                "input": text
            }

            response = await self.client.post(
                f"{self.base_url}/embeddings",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                return data["data"][0]["embedding"]
            else:
                return self._mock_embedding(text)

        except Exception as e:
            logger.error(f"Embedding generation error: {e}")
            return self._mock_embedding(text)

    def _mock_multi_model_analysis(
        self,
        transaction_data: Dict[str, Any],
        models: List[str]
    ) -> Dict[str, Any]:
        """Mock multi-model analysis for demo"""
        return {
            "ensemble_decision": {
                "fraud_probability": 0.82,
                "confidence": 0.89,
                "is_fraudulent": True,
                "risk_factors": [
                    "Unusual transaction amount",
                    "New geographic location",
                    "Irregular timing pattern",
                    "High-risk merchant category"
                ],
                "models_used": models,
                "agreement_level": "high"
            },
            "individual_models": {
                "gpt-4": {
                    "fraud_probability": 0.85,
                    "confidence": 0.92,
                    "risk_factors": ["Unusual amount", "Geographic anomaly"]
                },
                "claude-3-opus": {
                    "fraud_probability": 0.81,
                    "confidence": 0.88,
                    "risk_factors": ["Timing pattern", "Merchant risk"]
                },
                "llama-3": {
                    "fraud_probability": 0.80,
                    "confidence": 0.87,
                    "risk_factors": ["Amount deviation", "Location change"]
                }
            }
        }

    def _mock_embedding(self, text: str) -> List[float]:
        """Mock embedding for demo"""
        import numpy as np
        np.random.seed(hash(text) % (2**32))
        return np.random.rand(384).tolist()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup"""
        await self.client.aclose()


# Singleton instance
aiml_service = AIMLService()
