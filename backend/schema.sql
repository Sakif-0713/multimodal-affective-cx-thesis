-- Database Schema for Multimodal Affective Computing CX Decision Support System
-- Supabase PostgreSQL Table Definitions

CREATE TABLE IF NOT EXISTS triage_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    text_input TEXT,
    modalities_processed TEXT[],
    p_text JSONB,
    p_audio JSONB,
    p_video JSONB,
    audio_features JSONB,
    video_metadata JSONB,
    fused_probabilities JSONB NOT NULL,
    dominant_emotion VARCHAR(32) NOT NULL,
    confidence FLOAT NOT NULL,
    csi_score FLOAT NOT NULL,
    acute_dissatisfaction_alert BOOLEAN NOT NULL DEFAULT FALSE,
    anger_disappointment_score FLOAT NOT NULL,
    weights_used JSONB NOT NULL,
    aspect_touchpoints JSONB,
    processing_time_ms FLOAT,
    consent_given BOOLEAN NOT NULL DEFAULT TRUE,
    anonymized_participant_uuid UUID DEFAULT gen_random_uuid()
);

CREATE TABLE IF NOT EXISTS tam_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    cohort VARCHAR(16) NOT NULL, -- 'Cohort_A' (Students) or 'Cohort_B' (Managers)
    participant_id VARCHAR(64) NOT NULL,
    perceived_usefulness_score FLOAT NOT NULL, -- PU (1-5 scale)
    perceived_ease_of_use_score FLOAT NOT NULL, -- PEOU (1-5 scale)
    intention_to_adopt_score FLOAT NOT NULL, -- ITA (1-5 scale)
    perceived_triage_latency_reduction_pct FLOAT, -- Latency reduction % estimate
    qualitative_feedback TEXT
);

-- Indexing for fast BI Triage Queries
CREATE INDEX IF NOT EXISTS idx_triage_acute_alert ON triage_sessions(acute_dissatisfaction_alert);
CREATE INDEX IF NOT EXISTS idx_triage_created_at ON triage_sessions(created_at DESC);
