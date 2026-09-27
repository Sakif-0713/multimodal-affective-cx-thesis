"""
Multimodal Aspect-Based Sentiment Analysis (MABSA) Aspect Extractor.
Uses SpaCy dependency parsing and noun chunk extraction to isolate operational touchpoints
(e.g., billing, UI/UX, delivery, customer support) and link them to emotion vectors.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger("aspect_extractor")

# Standard CX Touchpoints and associated lexicon patterns
TOUCHPOINT_CATEGORIES = {
    "billing": ["billing", "invoice", "charge", "payment", "fee", "card", "subscription", "price", "overcharge"],
    "ui_ux": ["ui", "ux", "website", "app", "interface", "button", "screen", "navigation", "checkout", "page", "mobile"],
    "delivery": ["delivery", "shipping", "courier", "package", "driver", "arrival", "transit", "delay", "late"],
    "customer_support": ["support", "agent", "representative", "helpdesk", "service", "phone", "chat", "email", "ticket"],
    "product_quality": ["product", "quality", "item", "material", "feature", "hardware", "software", "bug", "defect"]
}

class AspectExtractor:
    def __init__(self):
        self.nlp = None
        self._load_spacy()

    def _load_spacy(self):
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("Successfully loaded SpaCy en_core_web_sm model.")
        except Exception as e:
            logger.warning(f"Could not load SpaCy model ({e}). Using regex/noun heuristic parser.")
            self.nlp = None

    def extract_aspects(self, text: str, emotion_vector: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Parses text for noun chunks and dependency targets, mapping them to touchpoints and emotion vectors.
        """
        if not text or not text.strip():
            return []

        extracted_aspects = []

        if self.nlp:
            try:
                doc = self.nlp(text)
                noun_chunks = [chunk.text.strip().lower() for chunk in doc.noun_chunks if not chunk.root.is_stop]

                for chunk in noun_chunks:
                    category = self._match_touchpoint_category(chunk)
                    if category:
                        extracted_aspects.append({
                            "term": chunk,
                            "touchpoint": category,
                            "bound_emotion_vector": emotion_vector,
                            "dominant_emotion": max(emotion_vector, key=emotion_vector.get) if emotion_vector else "neutral"
                        })
            except Exception as e:
                logger.error(f"Error running SpaCy parser: {e}")

        # Fallback / complementary heuristic matching if spaCy didn't catch specific keywords
        if not extracted_aspects:
            text_lower = text.lower()
            for category, keywords in TOUCHPOINT_CATEGORIES.items():
                for kw in keywords:
                    if kw in text_lower:
                        extracted_aspects.append({
                            "term": kw,
                            "touchpoint": category,
                            "bound_emotion_vector": emotion_vector,
                            "dominant_emotion": max(emotion_vector, key=emotion_vector.get) if emotion_vector else "neutral"
                        })
                        break

        # Deduplicate by touchpoint
        unique_aspects = {}
        for item in extracted_aspects:
            tp = item["touchpoint"]
            if tp not in unique_aspects:
                unique_aspects[tp] = item

        return list(unique_aspects.values())

    def _match_touchpoint_category(self, chunk: str) -> str:
        for category, keywords in TOUCHPOINT_CATEGORIES.items():
            for kw in keywords:
                if kw in chunk:
                    return category
        return "general_service"


_aspect_extractor_instance = None

def get_aspect_extractor() -> AspectExtractor:
    global _aspect_extractor_instance
    if _aspect_extractor_instance is None:
        _aspect_extractor_instance = AspectExtractor()
    return _aspect_extractor_instance

def extract_aspect_touchpoints(text: str, emotion_vector: Dict[str, float]) -> List[Dict[str, Any]]:
    extractor = get_aspect_extractor()
    return extractor.extract_aspects(text, emotion_vector)
