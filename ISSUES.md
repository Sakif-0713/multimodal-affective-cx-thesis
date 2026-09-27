# GitHub Issues & Task Backlog

This document tracks the scaffolded engineering tasks for the Capstone Thesis:
**"An Empirical Investigation into Multimodal Affective Computing for Enterprise Customer Experience (CX) Decision Support Systems"**.

---

### Issue #1: `[BE] Initialize FastAPI Monorepo and Ingestion Schema`
- **Labels**: `backend`, `fastapi`, `infrastructure`
- **Description**: Scaffold the core FastAPI web service in `/backend/main.py`. Expose the `/api/v1/triage` endpoint configured for multipart/form-data ingestion accepting textual reviews, audio file streams (`.wav`, `.webm`), and sampled video frames/clips (`.mp4`, `.webm`).
- **Acceptance Criteria**:
  - [x] `main.py` runs on Uvicorn server (`http://localhost:8000`).
  - [x] Endpoint `/api/v1/triage` receives `text: str`, `audio: UploadFile`, `video: UploadFile`.
  - [x] Returns standard JSON schema containing modal emotion vectors, fused affective score, CSI score, acute dissatisfaction alert flag, and extracted aspect touchpoints.
  - [x] Configured with CORS middleware for frontend communication.

---

### Issue #2: `[NLP] Implement RoBERTa GoEmotions Inference & Mapping`
- **Labels**: `nlp`, `roberta`, `emotions`
- **Description**: Implement `backend/models/text_pipeline.py` leveraging `SamLowe/roberta-base-go_emotions`. Map all 28 fine-grained GoEmotions outputs into 6 target affective categories.
- **Target Classes**: `anger`, `disappointment`, `neutral`, `joy`, `sadness`, `surprise`.
- **Acceptance Criteria**:
  - [x] Fine-grained 28-class GoEmotions predictions are aggregated into unified 6-class probability distribution summing to 1.0.
  - [x] Includes graceful fallback mechanism for offline/lightweight execution environments.
  - [x] Function `predict_text_emotions(text: str)` returns normalized dictionary of probabilities.

---

### Issue #3: `[Audio] Librosa Acoustic Feature & Prosody Extractor`
- **Labels**: `audio`, `librosa`, `prosody`
- **Description**: Build acoustic analysis module in `backend/models/audio_pipeline.py` using `librosa` and `soundfile`. Extract acoustic prosody parameters and MFCC features from `.wav` uploaded audio.
- **Extracted Metrics**:
  - 13 Mel-Frequency Cepstral Coefficients (MFCCs) mean & std dev.
  - Fundamental Pitch ($F_0$) via `librosa.pyin`.
  - Zero-Crossing Rate (ZCR).
  - Root Mean Square (RMS) energy.
- **Acceptance Criteria**:
  - [x] Extracts 13 MFCCs, mean pitch ($F_0$), ZCR, and RMS energy from raw audio byte streams.
  - [x] Derives acoustic prosody emotion probability vector over 6 target classes.
  - [x] Handles variable duration audio clips cleanly without memory leakage.

---

### Issue #4: `[Vision] MediaPipe + MobileNet-FER Video Frame Analyzer`
- **Labels**: `vision`, `mediapipe`, `fer`
- **Description**: Develop video pipeline in `backend/models/video_pipeline.py`. Sample uploaded video stream at 5 FPS, extract face region-of-interest (ROI) using MediaPipe Face Mesh, and classify facial expressions via MobileNet-FER.
- **Acceptance Criteria**:
  - [x] Video decoder samples video at 5 frames per second (5 FPS).
  - [x] Detects face bounding box and facial landmarks via MediaPipe.
  - [x] Evaluates facial expression probabilities per frame and computes average probability distribution across valid frames.
  - [x] Handles cases with missing faces or occlusions by returning default neutral probability distribution.

---

### Issue #5: `[Fusion] Implement Weighted Decision-Level Late Fusion & CSI Formula`
- **Labels**: `fusion`, `math`, `triage`
- **Description**: Build mathematical late-fusion model in `backend/models/late_fusion.py`. Implement weighted late fusion across text, audio, and video modalities, compute Customer Satisfaction Index (CSI), and evaluate escalation flags.
- **Mathematical Formula**:
  $$\text{Score}(e) = w_{\text{text}} \cdot P_{\text{text}}(e) + w_{\text{audio}} \cdot P_{\text{audio}}(e) + w_{\text{video}} \cdot P_{\text{video}}(e)$$
  *(Defaults: $w_{\text{text}}=0.50, w_{\text{audio}}=0.25, w_{\text{video}}=0.25$)*
- **Acceptance Criteria**:
  - [x] Fuses emotion probability vectors from text, audio, and video according to dynamic or default weight vectors.
  - [x] Calculates Customer Satisfaction Index (CSI) bounded $[0, 100]$.
  - [x] Flags acute dissatisfaction when $P_{\text{fused}}(\text{anger}) + P_{\text{fused}}(\text{disappointment}) \ge 0.60$.

---

### Issue #6: `[Aspect] SpaCy Dependency Parsing for MABSA`
- **Labels**: `nlp`, `spacy`, `mabsa`
- **Description**: Implement Multimodal Aspect-Based Sentiment Analysis (MABSA) in `backend/utils/aspect_extractor.py` using SpaCy (`en_core_web_sm`). Extract non-stop noun chunks and syntax dependencies, mapping operational terms to emotion vectors.
- **Target Touchpoints**: `billing`, `ui_ux`, `delivery`, `customer_support`, `pricing`, `product_quality`.
- **Acceptance Criteria**:
  - [x] Parses text for noun chunks and grammatical dependency targets.
  - [x] Maps extracted touchpoints to operational categories.
  - [x] Binds primary modal emotion vectors to each identified touchpoint.

---

### Issue #7: `[FE] Next.js Review Ingestion Portal (Mic & Webcam Sampling)`
- **Labels**: `frontend`, `nextjs`, `webrtc`
- **Description**: Construct customer review submission page in `/frontend/app/submit/page.jsx`. Provide text area input, browser audio recording via `MediaRecorder` API with waveform visualization, and 5 FPS canvas webcam capture stream.
- **Acceptance Criteria**:
  - [x] Modern, responsive UI with live character count text input.
  - [x] Audio recorder capturing `.webm`/`.wav` with live visualizer waveform.
  - [x] Webcam recorder sampling canvas frames at 5 FPS.
  - [x] Submits `FormData` containing text, audio, and video payloads to `/api/v1/triage` and displays real-time multimodal affective breakdown modal.

---

### Issue #8: `[FE] Executive Decision Support Dashboard & Alert Queue`
- **Labels**: `frontend`, `nextjs`, `dashboard`, `recharts`
- **Description**: Build executive BI decision support triage dashboard in `/frontend/app/dashboard/page.jsx`. Display real-time acute dissatisfaction alerts, aspect friction heatmaps, emotion distribution breakdown, and escalation triggers.
- **Acceptance Criteria**:
  - [x] Real-time alert feed displaying flagged customer cases ($\text{Anger} + \text{Disappointment} \ge 0.60$).
  - [x] Interactive Recharts visualizers (Emotion distribution, CSI trends, Touchpoint aspect friction).
  - [x] Modal preview detailing multimodal modality contribution (Text vs Audio vs Video).
  - [x] Simulated webhook trigger button to dispatch escalation tickets to CX managers.
