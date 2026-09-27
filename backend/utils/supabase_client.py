"""
Supabase Database Persistence Client.
Stores anonymized UUID triage sessions and TAM empirical evaluation responses.
Includes in-memory fallback store when SUPABASE_URL / SUPABASE_KEY are not present.
"""

import os
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("supabase_client")

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

_supabase_instance = None
_in_memory_triage_store: List[Dict[str, Any]] = []

def get_supabase_client():
    global _supabase_instance
    if _supabase_instance is not None:
        return _supabase_instance

    if SUPABASE_URL and SUPABASE_KEY:
        try:
            from supabase import create_client
            _supabase_instance = create_client(SUPABASE_URL, SUPABASE_KEY)
            logger.info("Connected to Supabase PostgreSQL database.")
            return _supabase_instance
        except Exception as e:
            logger.warning(f"Could not connect to Supabase ({e}). Operating with local in-memory fallback.")

    _supabase_instance = False
    return False

def save_triage_session(session_data: Dict[str, Any]) -> bool:
    """
    Saves anonymized triage session to Supabase database or local memory store.
    """
    client = get_supabase_client()
    
    if client:
        try:
            client.table("triage_sessions").insert(session_data).execute()
            logger.info(f"Successfully persisted triage session '{session_data.get('submission_id')}' to Supabase.")
            return True
        except Exception as e:
            logger.error(f"Failed to insert record into Supabase: {e}")

    # Memory fallback
    _in_memory_triage_store.insert(0, session_data)
    if len(_in_memory_triage_store) > 100:
        _in_memory_triage_store.pop()
    logger.info(f"Persisted triage session '{session_data.get('submission_id')}' in local memory store.")
    return True

def fetch_triage_history(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Fetches recent triage sessions for BI Dashboard.
    """
    client = get_supabase_client()
    if client:
        try:
            response = client.table("triage_sessions").select("*").order("created_at", desc=True).limit(limit).execute()
            return response.data if response and response.data else []
        except Exception as e:
            logger.error(f"Error fetching from Supabase: {e}")

    return _in_memory_triage_store[:limit]
