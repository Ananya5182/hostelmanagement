import os
from typing import Optional
from functools import lru_cache
from supabase import create_client, Client


from dotenv import load_dotenv

# Load local environment variables from .env if present
load_dotenv()


class DatabaseConfig:
    """Database configuration reading from environment variables."""
    
    SUPABASE_URL: str = os.getenv(
        "SUPABASE_URL", 
        "https://uyiybnpeiwkfedihmnrl.supabase.co"
    )
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")


_client_instance: Optional[Client] = None


def get_supabase() -> Client:
    """
    Returns a singleton instance of the Supabase Client.
    Initializes the client if not already instantiated.
    """
    global _client_instance
    if _client_instance is None:
        if not DatabaseConfig.SUPABASE_URL or not DatabaseConfig.SUPABASE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be configured in environment.")
        _client_instance = create_client(
            DatabaseConfig.SUPABASE_URL, 
            DatabaseConfig.SUPABASE_KEY
        )
    return _client_instance


def check_db_health() -> bool:
    """
    Pings the Supabase database to verify end-to-end connectivity.
    Returns True if healthy, False otherwise.
    """
    try:
        client = get_supabase()
        response = client.table("rooms").select("id").limit(1).execute()
        return response is not None
    except Exception:
        return False
