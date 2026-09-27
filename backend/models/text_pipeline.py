"""
RoBERTa GoEmotions Text Emotion Classification Pipeline.
Uses 'SamLowe/roberta-base-go_emotions' to infer 28 fine-grained emotion probabilities,
mapping them down to 6 unified target classes:
  - anger
  - disappointment
  - neutral
  - joy
  - sadness
  - surprise
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger("text_pipeline")

# 28 GoEmotions to Unified 6 Target Classes Mapping Schema
GO_EMOTIONS_MAPPING = {
    "anger": ["anger", "annoyance", "disapproval", "disgust"],
    "disappointment": ["disappointment", "embarrassment", "remorse", "grief"],
    "sadness": ["sadness", "fear", "nervousness"],
    "joy": ["joy", "admiration", "amusement", "approval", "caring", "desire", "excitement", "gratitude", "love", "optimism", "pride", "relief"],
    "surprise": ["surprise", "realization", "confusion", "curiosity"],
    "neutral": ["neutral"]
}

TARGET_CLASSES = ["anger", "disappointment", "neutral", "joy", "sadness", "surprise"]

class RoBERTaEmotionClassifier:
    def __init__(self, model_name: str = "SamLowe/roberta-base-go_emotions"):
        self.model_name = model_name
        self.pipeline = None
        self._init_model()

    def _init_model(self):
        try:
            from transformers import pipeline
            self.pipeline = pipeline(
                "text-classification",
                model=self.model_name,
                top_k=None,
                tokenizer=self.model_name
            )
            logger.info(f"Successfully loaded RoBERTa model: {self.model_name}")
        except Exception as e:
            logger.warning(f"Could not load HuggingFace pipeline ({e}). Operating in heuristic/rule mode.")
            self.pipeline = None

    def predict(self, text: str) -> Dict[str, float]:
        """
        Classifies input text and maps GoEmotions probabilities to 6 target classes.
        Returns a dictionary of normalized emotion probabilities.
        """
        if not text or not text.strip():
            return {cls: (1.0 if cls == "neutral" else 0.0) for cls in TARGET_CLASSES}

        if self.pipeline:
            try:
                results = self.pipeline(text)
                # results is a list of dicts: [{'label': 'admiration', 'score': 0.85}, ...]
                predictions = results[0] if isinstance(results, list) and isinstance(results[0], list) else results
                raw_probs = {item["label"]: float(item["score"]) for item in predictions}
                return self._map_goemotions_to_target(raw_probs)
            except Exception as e:
                logger.error(f"Error during transformer inference: {e}")

        # Rule-based fallback heuristic for offline/mock environments
        return self._heuristic_fallback(text)

    def _map_goemotions_to_target(self, raw_probs: Dict[str, float]) -> Dict[str, float]:
        mapped = {cls: 0.0 for cls in TARGET_CLASSES}
        
        for target_cls, source_labels in GO_EMOTIONS_MAPPING.items():
            sum_prob = sum(raw_probs.get(lbl, 0.0) for lbl in source_labels)
            mapped[target_cls] = sum_prob

        total = sum(mapped.values())
        if total > 0:
            return {k: round(v / total, 4) for k, v in mapped.items()}
        return {cls: (1.0 if cls == "neutral" else 0.0) for cls in TARGET_CLASSES}

    def _heuristic_fallback(self, text: str) -> Dict[str, float]:
        """Keyword heuristic estimator when heavy ML model isn't pre-loaded."""
        text_lower = text.lower()
        
        scores = {cls: 0.05 for cls in TARGET_CLASSES}
        
        anger_keywords = ["angry", "furious", "terrible", "outraged", "horrible", "hate", "worst", "unacceptable", "scam"]
        disappointment_keywords = ["disappointed", "poor", "broken", "failed", "regret", "useless", "flawed", "mistake", "cancel", "refund"]
        joy_keywords = ["love", "great", "excellent", "amazing", "happy", "wonderful", "perfect", "good", "helpful", "thanks"]
        sadness_keywords = ["sad", "depressed", "upset", "sorry", "unfortunate", "unhappy"]
        surprise_keywords = ["surprised", "unexpected", "wow", "unbelievable", "shocked"]

        for kw in anger_keywords:
            if kw in text_lower:
                scores["anger"] += 0.35
        for kw in disappointment_keywords:
            if kw in text_lower:
                scores["disappointment"] += 0.35
        for kw in joy_keywords:
            if kw in text_lower:
                scores["joy"] += 0.35
        for kw in sadness_keywords:
            if kw in text_lower:
                scores["sadness"] += 0.35
        for kw in surprise_keywords:
            if kw in text_lower:
                scores["surprise"] += 0.30

        total = sum(scores.values())
        return {k: round(v / total, 4) for k, v in scores.items()}


_text_classifier_instance = None

def get_text_classifier() -> RoBERTaEmotionClassifier:
    global _text_classifier_instance
    if _text_classifier_instance is None:
        _text_classifier_instance = RoBERTaEmotionClassifier()
    return _text_classifier_instance

def predict_text_emotions(text: str) -> Dict[str, float]:
    classifier = get_text_classifier()
    return classifier.predict(text)
