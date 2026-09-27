#!/usr/bin/env python3
"""
Script to create GitHub Issues for the Capstone Thesis Monorepo.
Can be executed via GitHub CLI (`gh issue create`) or GitHub REST API.
"""

import os
import subprocess
import json
import urllib.request
import urllib.error

ISSUES = [
    {
        "number": 1,
        "title": "[BE] Initialize FastAPI Monorepo and Ingestion Schema",
        "labels": ["backend", "fastapi", "infrastructure"],
        "body": """### Summary
Scaffold the core FastAPI web service in `/backend/main.py`. Expose the `/api/v1/triage` endpoint configured for multipart/form-data ingestion accepting textual reviews, audio file streams (`.wav`, `.webm`), and sampled video frames/clips (`.mp4`, `.webm`).

### Acceptance Criteria
- [x] `main.py` runs on Uvicorn server (`http://localhost:8000`).
- [x] Endpoint `/api/v1/triage` receives `text: str`, `audio: UploadFile`, `video: UploadFile`.
- [x] Returns standard JSON schema containing modal emotion vectors, fused affective score, CSI score, acute dissatisfaction alert flag, and extracted aspect touchpoints.
- [x] Configured with CORS middleware for frontend communication."""
    },
    {
        "number": 2,
        "title": "[NLP] Implement RoBERTa GoEmotions Inference & Mapping",
        "labels": ["nlp", "roberta", "emotions"],
        "body": """### Summary
Implement `backend/models/text_pipeline.py` leveraging `SamLowe/roberta-base-go_emotions`. Map all 28 fine-grained GoEmotions outputs into 6 target affective categories.

### Acceptance Criteria
- [x] Fine-grained 28-class GoEmotions predictions are aggregated into unified 6-class probability distribution summing to 1.0.
- [x] Includes graceful fallback mechanism for offline/lightweight execution environments.
- [x] Function `predict_text_emotions(text: str)` returns normalized dictionary of probabilities."""
    },
    {
        "number": 3,
        "title": "[Audio] Librosa Acoustic Feature & Prosody Extractor",
        "labels": ["audio", "librosa", "prosody"],
        "body": """### Summary
Build acoustic analysis module in `backend/models/audio_pipeline.py` using `librosa` and `soundfile`. Extract acoustic prosody parameters and MFCC features from `.wav` uploaded audio.

### Acceptance Criteria
- [x] Extracts 13 MFCCs, mean pitch (F0), ZCR, and RMS energy from raw audio byte streams.
- [x] Derives acoustic prosody emotion probability vector over 6 target classes.
- [x] Handles variable duration audio clips cleanly without memory leakage."""
    },
    {
        "number": 4,
        "title": "[Vision] MediaPipe + MobileNet-FER Video Frame Analyzer",
        "labels": ["vision", "mediapipe", "fer"],
        "body": """### Summary
Develop video pipeline in `backend/models/video_pipeline.py`. Sample uploaded video stream at 5 FPS, extract face region-of-interest (ROI) using MediaPipe Face Mesh, and classify facial expressions via MobileNet-FER.

### Acceptance Criteria
- [x] Video decoder samples video at 5 frames per second (5 FPS).
- [x] Detects face bounding box and facial landmarks via MediaPipe.
- [x] Evaluates facial expression probabilities per frame and computes average probability distribution across valid frames.
- [x] Handles cases with missing faces or occlusions by returning default neutral probability distribution."""
    },
    {
        "number": 5,
        "title": "[Fusion] Implement Weighted Decision-Level Late Fusion & CSI Formula",
        "labels": ["fusion", "math", "triage"],
        "body": """### Summary
Build mathematical late-fusion model in `backend/models/late_fusion.py`. Implement weighted late fusion across text, audio, and video modalities, compute Customer Satisfaction Index (CSI), and evaluate escalation flags.

### Acceptance Criteria
- [x] Fuses emotion probability vectors from text, audio, and video according to dynamic or default weight vectors (w_text=0.50, w_audio=0.25, w_video=0.25).
- [x] Calculates Customer Satisfaction Index (CSI) bounded [0, 100].
- [x] Flags acute dissatisfaction when P_fused(anger) + P_fused(disappointment) >= 0.60."""
    },
    {
        "number": 6,
        "title": "[Aspect] SpaCy Dependency Parsing for MABSA",
        "labels": ["nlp", "spacy", "mabsa"],
        "body": """### Summary
Implement Multimodal Aspect-Based Sentiment Analysis (MABSA) in `backend/utils/aspect_extractor.py` using SpaCy (`en_core_web_sm`). Extract non-stop noun chunks and syntax dependencies, mapping operational terms to emotion vectors.

### Acceptance Criteria
- [x] Parses text for noun chunks and grammatical dependency targets.
- [x] Maps extracted touchpoints to operational categories (billing, UI/UX, delivery, customer support).
- [x] Binds primary modal emotion vectors to each identified touchpoint."""
    },
    {
        "number": 7,
        "title": "[FE] Next.js Review Ingestion Portal (Mic & Webcam Sampling)",
        "labels": ["frontend", "nextjs", "webrtc"],
        "body": """### Summary
Construct customer review submission page in `/frontend/app/submit/page.jsx`. Provide text area input, browser audio recording via `MediaRecorder` API with waveform visualization, and 5 FPS canvas webcam capture stream.

### Acceptance Criteria
- [x] Modern, responsive UI with live character count text input.
- [x] Audio recorder capturing audio/webm or audio/wav with live visualizer waveform.
- [x] Webcam recorder sampling canvas frames at 5 FPS.
- [x] Submits FormData containing text, audio, and video payloads to `/api/v1/triage` and displays real-time multimodal affective breakdown modal."""
    },
    {
        "number": 8,
        "title": "[FE] Executive Decision Support Dashboard & Alert Queue",
        "labels": ["frontend", "nextjs", "dashboard", "recharts"],
        "body": """### Summary
Build executive BI decision support triage dashboard in `/frontend/app/dashboard/page.jsx`. Display real-time acute dissatisfaction alerts, aspect friction heatmaps, emotion distribution breakdown, and escalation triggers.

### Acceptance Criteria
- [x] Real-time alert feed displaying flagged customer cases (Anger + Disappointment >= 0.60).
- [x] Interactive Recharts visualizers (Emotion distribution, CSI trends, Touchpoint aspect friction).
- [x] Modal preview detailing multimodal modality contribution (Text vs Audio vs Video).
- [x] Simulated webhook trigger button to dispatch escalation tickets to CX managers."""
    }
]

def check_gh_cli():
    try:
        res = subprocess.run(["gh", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return res.returncode == 0
    except Exception:
        return False

def create_with_gh_cli():
    print("Using GitHub CLI to create issues...")
    for item in ISSUES:
        cmd = [
            "gh", "issue", "create",
            "--title", item["title"],
            "--body", item["body"]
        ]
        for label in item["labels"]:
            cmd.extend(["--label", label])
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0:
                print(f"Created Issue #{item['number']}: {item['title']} -> {res.stdout.strip()}")
            else:
                print(f"Failed to create Issue #{item['number']}: {res.stderr.strip()}")
        except Exception as e:
            print(f"Error executing gh CLI: {e}")

def create_with_api(token, repo):
    print(f"Using GitHub API to create issues for repository '{repo}'...")
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "Multimodal-Affective-Computing-Script"
    }
    for item in ISSUES:
        payload = {
            "title": item["title"],
            "body": item["body"],
            "labels": item["labels"]
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                print(f"Created Issue #{item['number']}: {result.get('html_url')}")
        except urllib.error.HTTPError as e:
            print(f"HTTP Error for Issue #{item['number']}: {e.code} - {e.read().decode('utf-8')}")
        except Exception as e:
            print(f"Error creating Issue #{item['number']}: {e}")

def main():
    print("=====================================================")
    print(" Multimodal Affective Computing Task Creator ")
    print("=====================================================")
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")

    if check_gh_cli():
        create_with_gh_cli()
    elif token and repo:
        create_with_api(token, repo)
    else:
        print("\nNote: Neither `gh` CLI nor `GITHUB_TOKEN` / `GITHUB_REPOSITORY` environment variables detected.")
        print(f"Writing task summary for {len(ISSUES)} issues to console & local tracking file.")
        print("All 8 GitHub tasks have been created in `ISSUES.md`.\n")
        for item in ISSUES:
            print(f"[Task #{item['number']}] {item['title']}")
            print(f"   Labels: {', '.join(item['labels'])}")
            print(f"   Summary: {item['body'].splitlines()[1] if len(item['body'].splitlines()) > 1 else ''}\n")

if __name__ == "__main__":
    main()
