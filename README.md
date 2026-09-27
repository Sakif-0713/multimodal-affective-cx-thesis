# Capstone Thesis Monorepo

> **An Empirical Investigation into Multimodal Affective Computing for Enterprise Customer Experience (CX) Decision Support Systems**

![Multimodal Affective Computing Architecture](https://img.shields.io/badge/FastAPI-v0.110.0-009688?style=flat-square&logo=fastapi)
![Next.js 14](https://img.shields.io/badge/Next.js-v14.2.0-000000?style=flat-square&logo=next.js)
![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-v3.4-38B2AC?style=flat-square&logo=tailwindcss)

---

## 📌 Executive Summary

Enterprise Customer Experience (CX) decision-making has traditionally relied on post-interaction textual feedback or manual quality auditing. This research introduces a real-time **Multimodal Affective Computing framework** combining:
1. **NLP Text Sentiment & Emotion**: RoBERTa (`SamLowe/roberta-base-go_emotions`) mapped to 6 target affective states.
2. **Audio Prosody & Acoustic Features**: Librosa MFCCs (13 coefficients), fundamental pitch ($F_0$), Zero-Crossing Rate (ZCR), and Root Mean Square (RMS) energy.
3. **Facial Emotion Recognition (FER)**: MediaPipe Face Mesh landmark extraction with 5 FPS frame sampling and MobileNet-FER probability classification.
4. **Decision-Level Late Fusion**: Mathematical score fusion model:
   $$\text{Score}(e) = w_{\text{text}} \cdot P_{\text{text}}(e) + w_{\text{audio}} \cdot P_{\text{audio}}(e) + w_{\text{video}} \cdot P_{\text{video}}(e)$$
   *(Default weights: $w_{\text{text}} = 0.50$, $w_{\text{audio}} = 0.25$, $w_{\text{video}} = 0.25$)*
5. **Multimodal Aspect-Based Sentiment Analysis (MABSA)**: SpaCy noun-chunk dependency parsing binding emotional vectors to specific operational touchpoints (e.g., *Billing*, *UI/UX*, *Delivery*, *Customer Support*).
6. **Executive BI Triage & Escalation Engine**: Real-time Customer Satisfaction Index ($\text{CSI}$) computation and automated acute dissatisfaction triggers ($\text{Anger} + \text{Disappointment} \ge 0.60$).

---

## 🏗️ Repository Architecture

```
thesis/
├── .github/
│   └── workflows/
│       └── ci.yml               # Automated CI for Python & Next.js linting/building
├── backend/                     # Python FastAPI Multimodal Inference Server
│   ├── models/
│   │   ├── text_pipeline.py     # RoBERTa GoEmotions inference & 6-class mapping
│   │   ├── audio_pipeline.py    # Librosa acoustic prosody & MFCC feature extractor
│   │   ├── video_pipeline.py    # MediaPipe Face Mesh & MobileNet-FER frame analyzer
│   │   └── late_fusion.py       # Mathematical decision-level late fusion & CSI formula
│   ├── utils/
│   │   └── aspect_extractor.py  # SpaCy dependency parsing for MABSA touchpoint binding
│   ├── main.py                  # FastAPI application entry point with /api/v1/triage
│   └── requirements.txt         # Backend Python dependencies
├── frontend/                    # Next.js 14 Executive Dashboard & Ingestion Portal
│   ├── app/
│   │   ├── submit/page.jsx      # Customer review ingestion portal (mic & webcam 5 FPS stream)
│   │   ├── dashboard/page.jsx   # Executive BI triage dashboard & real-time alert feed
│   │   ├── globals.css          # Design system, glassmorphism tokens, Tailwind CSS
│   │   ├── layout.jsx           # Master layout wrapper with header navigation
│   │   └── page.jsx             # Project landing page & quick start portal
│   ├── package.json             # Frontend Node.js dependencies
│   ├── tailwind.config.js       # Tailwind CSS theme configuration
│   ├── postcss.config.js        # PostCSS configuration
│   └── jsconfig.json            # Module resolution configuration
├── scripts/
│   └── create_github_issues.py  # GitHub issue generator for project task tracking
└── ISSUES.md                    # Trackable capstone task list with acceptance criteria
```

---

## 🚀 Quick Start Guide

### 1. Backend Service Setup (Python FastAPI)

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn main:app --reload --port 8000
```

The FastAPI server will start at `http://localhost:8000`. 
API Documentation will be accessible at `http://localhost:8000/docs`.

### 2. Frontend Application Setup (Next.js 14)

```bash
cd frontend
npm install
npm run dev
```

The Next.js application will start at `http://localhost:3000`.
- Customer Ingestion Portal: `http://localhost:3000/submit`
- Executive BI Dashboard: `http://localhost:3000/dashboard`

---

## 📊 Core Mathematical Formulation

### Late Fusion Probability Equation
$$P_{\text{fused}}(e) = \sum_{m \in \{\text{text}, \text{audio}, \text{video}\}} w_m \cdot P_m(e)$$
Subject to:
$$\sum_{m} w_m = 1.0, \quad w_m \ge 0$$

### Customer Satisfaction Index ($\text{CSI}$)
$$\text{CSI} = \left( P_{\text{fused}}(\text{joy}) + 0.5 \cdot P_{\text{fused}}(\text{neutral}) + 0.5 \cdot P_{\text{fused}}(\text{surprise}) \right) \times 100$$

### Acute Dissatisfaction Alert Condition
$$\text{Trigger Escalation} = \mathbb{I}\left( P_{\text{fused}}(\text{anger}) + P_{\text{fused}}(\text{disappointment}) \ge 0.60 \right)$$

---

## 📝 GitHub Project Tasks & Trackable Issues

See [ISSUES.md](file:///c:/Users/Admin/Downloads/thesis/ISSUES.md) or execute `python scripts/create_github_issues.py` to create the 8 task issues on GitHub.
