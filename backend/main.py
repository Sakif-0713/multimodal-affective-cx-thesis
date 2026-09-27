"""
FastAPI Server for Multimodal Affective Computing CX Decision Support System.
Endpoint `/api/v1/triage` accepts multipart FormData (text, audio, video) and returns:
  - Individual modal emotion vectors (Text, Audio, Video)
  - Mathematical late fusion score breakdown
  - Customer Satisfaction Index (CSI)
  - Acute dissatisfaction alert flag (Anger + Disappointment >= 0.60)
  - Multimodal Aspect-Based Touchpoint mapping
"""

import time
import logging
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTask
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import pipeline modules
from models.text_pipeline import predict_text_emotions
from models.audio_pipeline import process_audio_file
from models.video_pipeline import process_video_file
from models.late_fusion import compute_late_fusion
from utils.aspect_extractor import extract_aspect_touchpoints

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("main_triage_api")

app = FastAPI(
    title="Multimodal Affective Computing Triage API",
    description="Backend Service for Enterprise CX Decision Support Systems",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Output Schema Pydantic models
class TriageResponse(BaseModel):
    submission_id: str
    timestamp: float
    text_input: str
    modalities_processed: List[str]
    p_text: Dict[str, float]
    p_audio: Dict[str, float]
    p_video: Dict[str, float]
    audio_features: Dict[str, Any]
    video_metadata: Dict[str, Any]
    fused_probabilities: Dict[str, float]
    dominant_emotion: str
    confidence: float
    csi_score: float
    acute_dissatisfaction_alert: bool
    anger_disappointment_score: float
    weights_used: Dict[str, float]
    aspect_touchpoints: List[Dict[str, Any]]
    processing_time_ms: float

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Multimodal Affective Computing Triage Engine",
        "version": "1.0.0",
        "endpoints": {
            "triage": "/api/v1/triage",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/api/v1/triage", response_model=TriageResponse)
async def triage_feedback(
    text: str = Form(default=""),
    w_text: float = Form(default=0.50),
    w_audio: float = Form(default=0.25),
    w_video: float = Form(default=0.25),
    audio: Optional[UploadFile] = File(default=None),
    video: Optional[UploadFile] = File(default=None)
):
    start_time = time.time()
    submission_id = f"sub_{int(time.time() * 1000)}"
    modalities_processed = []

    # 1. Process NLP Text Pipeline
    p_text = predict_text_emotions(text)
    if text and text.strip():
        modalities_processed.append("text")

    # 2. Process Audio Acoustic Prosody Pipeline
    audio_bytes = b""
    if audio is not None:
        try:
            audio_bytes = await audio.read()
            if len(audio_bytes) > 0:
                modalities_processed.append("audio")
        except Exception as e:
            logger.error(f"Error reading audio stream: {e}")

    audio_features, p_audio = process_audio_file(audio_bytes)

    # 3. Process Video Frame Sampling Pipeline (5 FPS)
    video_bytes = b""
    if video is not None:
        try:
            video_bytes = await video.read()
            if len(video_bytes) > 0:
                modalities_processed.append("video")
        except Exception as e:
            logger.error(f"Error reading video stream: {e}")

    video_metadata, p_video = process_video_file(video_bytes)

    # Default to text modality if no files uploaded
    if not modalities_processed:
        modalities_processed.append("text_fallback")

    # 4. Perform Multimodal Late Fusion & CSI Calculation
    fusion_result = compute_late_fusion(
        p_text=p_text,
        p_audio=p_audio,
        p_video=p_video,
        w_text=w_text,
        w_audio=w_audio,
        w_video=w_video
    )

    # 5. Extract Touchpoint Aspects (MABSA)
    aspect_touchpoints = extract_aspect_touchpoints(text, fusion_result["fused_probabilities"])

    processing_time = round((time.time() - start_time) * 1000, 2)

    return TriageResponse(
        submission_id=submission_id,
        timestamp=time.time(),
        text_input=text,
        modalities_processed=modalities_processed,
        p_text=p_text,
        p_audio=p_audio,
        p_video=p_video,
        audio_features=audio_features,
        video_metadata=video_metadata,
        fused_probabilities=fusion_result["fused_probabilities"],
        dominant_emotion=fusion_result["dominant_emotion"],
        confidence=fusion_result["confidence"],
        csi_score=fusion_result["csi_score"],
        acute_dissatisfaction_alert=fusion_result["acute_dissatisfaction_alert"],
        anger_disappointment_score=fusion_result["anger_disappointment_score"],
        weights_used=fusion_result["weights_used"],
        aspect_touchpoints=aspect_touchpoints,
        processing_time_ms=processing_time
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
