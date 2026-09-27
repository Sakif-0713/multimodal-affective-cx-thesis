"""
Audio Pipeline: Librosa Acoustic Prosody & MFCC Feature Extractor.
Extracts 13 MFCCs, mean pitch (F0), Zero-Crossing Rate (ZCR), and RMS energy from .wav uploads,
mapping acoustic prosody markers to a unified 6-class emotion distribution.
"""

import io
import logging
import numpy as np
from typing import Dict, Any, Tuple

logger = logging.getLogger("audio_pipeline")

TARGET_CLASSES = ["anger", "disappointment", "neutral", "joy", "sadness", "surprise"]

class AudioProsodyExtractor:
    def __init__(self, sample_rate: int = 16000, n_mfcc: int = 13):
        self.sample_rate = sample_rate
        self.n_mfcc = n_mfcc

    def extract_features(self, audio_bytes: bytes) -> Tuple[Dict[str, Any], Dict[str, float]]:
        """
        Extracts acoustic features (13 MFCCs, pitch F0, ZCR, RMS) and computes emotion probabilities.
        """
        if not audio_bytes or len(audio_bytes) == 0:
            return self._empty_response()

        try:
            import librosa
            import soundfile as sf
            
            # Load audio from byte stream
            audio_io = io.BytesIO(audio_bytes)
            y, sr = librosa.load(audio_io, sr=self.sample_rate)

            if len(y) == 0:
                return self._empty_response()

            # 1. 13 MFCCs
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=self.n_mfcc)
            mfcc_means = np.mean(mfccs, axis=1).tolist()
            mfcc_stds = np.std(mfccs, axis=1).tolist()

            # 2. RMS Energy
            rms = librosa.feature.rms(y=y)
            mean_rms = float(np.mean(rms))

            # 3. Zero Crossing Rate
            zcr = librosa.feature.zero_crossing_rate(y=y)
            mean_zcr = float(np.mean(zcr))

            # 4. Fundamental Pitch (F0) using pyin
            try:
                f0, _, _ = librosa.pyin(y, fmin=float(librosa.note_to_hz('C2')), fmax=float(librosa.note_to_hz('C7')))
                f0_clean = f0[~np.isnan(f0)] if f0 is not None else np.array([])
                mean_f0 = float(np.mean(f0_clean)) if len(f0_clean) > 0 else 0.0
            except Exception:
                mean_f0 = 0.0

            raw_features = {
                "mfcc_means": [round(val, 4) for val in mfcc_means],
                "mfcc_stds": [round(val, 4) for val in mfcc_stds],
                "mean_pitch_f0": round(mean_f0, 2),
                "zero_crossing_rate": round(mean_zcr, 4),
                "rms_energy": round(mean_rms, 4),
                "duration_seconds": round(len(y) / sr, 2)
            }

            probs = self._map_prosody_to_emotions(mean_f0, mean_zcr, mean_rms, mfcc_means)
            return raw_features, probs

        except Exception as e:
            logger.warning(f"Error parsing audio with librosa ({e}). Returning fallback features.")
            return self._empty_response()

    def _map_prosody_to_emotions(self, pitch: float, zcr: float, rms: float, mfccs: list) -> Dict[str, float]:
        """
        Prosodic acoustic rule mapping:
        - High RMS + High Pitch + High ZCR -> Anger / Surprise
        - Low RMS + Low Pitch -> Sadness / Disappointment
        - Moderate RMS + Moderate Pitch -> Neutral / Joy
        """
        probs = {cls: 0.10 for cls in TARGET_CLASSES}

        # Energy & Pitch thresholds
        high_energy = rms > 0.08
        high_pitch = pitch > 200.0
        high_zcr = zcr > 0.08
        low_energy = rms < 0.03
        low_pitch = pitch > 0 and pitch < 130.0

        if high_energy and high_pitch and high_zcr:
            probs["anger"] += 0.45
            probs["surprise"] += 0.25
        elif high_energy and not high_pitch:
            probs["anger"] += 0.30
            probs["disappointment"] += 0.20
        elif low_energy or low_pitch:
            probs["sadness"] += 0.35
            probs["disappointment"] += 0.35
        else:
            probs["neutral"] += 0.40
            probs["joy"] += 0.20

        total = sum(probs.values())
        return {k: round(v / total, 4) for k, v in probs.items()}

    def _empty_response(self) -> Tuple[Dict[str, Any], Dict[str, float]]:
        features = {
            "mfcc_means": [0.0] * self.n_mfcc,
            "mfcc_stds": [0.0] * self.n_mfcc,
            "mean_pitch_f0": 0.0,
            "zero_crossing_rate": 0.0,
            "rms_energy": 0.0,
            "duration_seconds": 0.0
        }
        probs = {cls: (1.0 if cls == "neutral" else 0.0) for cls in TARGET_CLASSES}
        return features, probs


_audio_extractor_instance = None

def get_audio_extractor() -> AudioProsodyExtractor:
    global _audio_extractor_instance
    if _audio_extractor_instance is None:
        _audio_extractor_instance = AudioProsodyExtractor()
    return _audio_extractor_instance

def process_audio_file(audio_bytes: bytes) -> Tuple[Dict[str, Any], Dict[str, float]]:
    extractor = get_audio_extractor()
    return extractor.extract_features(audio_bytes)
