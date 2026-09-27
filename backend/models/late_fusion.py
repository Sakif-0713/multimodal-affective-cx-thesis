"""
Multimodal Decision-Level Late Fusion & Customer Satisfaction Index (CSI) Calculator.

Formula:
  Score(e) = w_text * P_text(e) + w_audio * P_audio(e) + w_video * P_video(e)
  Defaults: w_text=0.50, w_audio=0.25, w_video=0.25

Customer Satisfaction Index (CSI):
  CSI = (P_fused('joy') + 0.5 * P_fused('neutral') + 0.5 * P_fused('surprise')) * 100

Acute Dissatisfaction Escalation Flag:
  Trigger = True if (P_fused('anger') + P_fused('disappointment')) >= 0.60
"""

from typing import Dict, Any, Optional

TARGET_CLASSES = ["anger", "disappointment", "neutral", "joy", "sadness", "surprise"]

class MultimodalLateFusion:
    def __init__(self, w_text: float = 0.50, w_audio: float = 0.25, w_video: float = 0.25):
        self.w_text = w_text
        self.w_audio = w_audio
        self.w_video = w_video
        self._normalize_weights()

    def _normalize_weights(self):
        total = self.w_text + self.w_audio + self.w_video
        if total > 0:
            self.w_text = self.w_text / total
            self.w_audio = self.w_audio / total
            self.w_video = self.w_video / total
        else:
            self.w_text, self.w_audio, self.w_video = 0.50, 0.25, 0.25

    def fuse(
        self,
        p_text: Dict[str, float],
        p_audio: Dict[str, float],
        p_video: Dict[str, float],
        custom_weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Executes decision-level late fusion over text, audio, and video probability distributions.
        """
        w_t = self.w_text
        w_a = self.w_audio
        w_v = self.w_video

        if custom_weights:
            wt = custom_weights.get("w_text", self.w_text)
            wa = custom_weights.get("w_audio", self.w_audio)
            wv = custom_weights.get("w_video", self.w_video)
            tot = wt + wa + wv
            if tot > 0:
                w_t, w_a, w_v = wt / tot, wa / tot, wv / tot

        fused_probs = {}
        for cls in TARGET_CLASSES:
            prob_t = p_text.get(cls, 0.0)
            prob_a = p_audio.get(cls, 0.0)
            prob_v = p_video.get(cls, 0.0)
            
            fused_score = (w_t * prob_t) + (w_a * prob_a) + (w_v * prob_v)
            fused_probs[cls] = round(fused_score, 4)

        # Normalize fused probabilities to sum exactly to 1.0
        tot_fused = sum(fused_probs.values())
        if tot_fused > 0:
            fused_probs = {k: round(v / tot_fused, 4) for k, v in fused_probs.items()}

        # 1. Dominant Emotion
        dominant_emotion = max(fused_probs, key=fused_probs.get)
        confidence = fused_probs[dominant_emotion]

        # 2. Customer Satisfaction Index (CSI)
        csi_score = round((
            fused_probs.get("joy", 0.0) +
            0.5 * fused_probs.get("neutral", 0.0) +
            0.5 * fused_probs.get("surprise", 0.0)
        ) * 100.0, 2)

        # 3. Acute Dissatisfaction Alert Threshold Check
        anger_disappointment_score = fused_probs.get("anger", 0.0) + fused_probs.get("disappointment", 0.0)
        acute_dissatisfaction_alert = anger_disappointment_score >= 0.60

        return {
            "fused_probabilities": fused_probs,
            "dominant_emotion": dominant_emotion,
            "confidence": confidence,
            "csi_score": csi_score,
            "acute_dissatisfaction_alert": acute_dissatisfaction_alert,
            "anger_disappointment_score": round(anger_disappointment_score, 4),
            "weights_used": {
                "w_text": round(w_t, 3),
                "w_audio": round(w_a, 3),
                "w_video": round(w_v, 3)
            }
        }


def compute_late_fusion(
    p_text: Dict[str, float],
    p_audio: Dict[str, float],
    p_video: Dict[str, float],
    w_text: float = 0.50,
    w_audio: float = 0.25,
    w_video: float = 0.25
) -> Dict[str, Any]:
    fuser = MultimodalLateFusion(w_text=w_text, w_audio=w_audio, w_video=w_video)
    return fuser.fuse(p_text, p_audio, p_video)
