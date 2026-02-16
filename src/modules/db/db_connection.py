# src/modules/db/db_connection.py
"""
Database Connection Manager - Isolated & Protected
Gravity Rule 2: Connection logic separated from business logic.

This module handles:
- Environment loading
- Client initialization
- Session management
- Reconnection logic
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Import from configs (centralized)
from configs.supabase_config import SUPABASE_URL, SUPABASE_KEY


class DatabaseConnection:
    """
    Singleton-like connection manager.
    Handles all connection concerns separately from data operations.
    """
    
    _instance = None
    _client: Client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._load_environment()
        self._connect()
    
    def _load_environment(self):
        """Load .env from project root with robust path resolution."""
        # Strategy: Find project root by looking for .env
        possible_paths = [
            os.path.join(os.getcwd(), ".env"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), ".env"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"// DB: Loading .env from {path}")
                load_dotenv(path, override=True)
                self._env_path = path
                return
        
        print("// DB WARNING: No .env file found!")
        self._env_path = None
    
    def _connect(self):
        """Initialize Supabase client."""
        self.url = os.getenv("SUPABASE_URL") or SUPABASE_URL
        self.key = os.getenv("SUPABASE_KEY") or SUPABASE_KEY
        
        if not self.url or not self.key:
            print("// DB ERROR: Missing SUPABASE_URL or SUPABASE_KEY")
            self._client = None
            return
        
        try:
            print(f"// DB: Connecting to {self.url[:25]}...")
            self._client = create_client(self.url, self.key)
            
            if self._client:
                print("// DB: Connected successfully.")
            else:
                print("// DB ERROR: Client creation returned None")
                
        except Exception as e:
            print(f"// DB ERROR: Connection failed - {e}")
            self._client = None
    
    @property
    def client(self) -> Client:
        """Get the Supabase client instance."""
        return self._client
    
    @property
    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._client is not None
    
    def reconnect(self):
        """Force reconnection (useful after token refresh)."""
        self._initialized = False
        self._client = None
        self.__init__()
    
    def get_session_info(self) -> dict:
        """Get current auth session information."""
        if not self._client:
            return {"status": "disconnected", "user_id": None}
        
        try:
            session = self._client.auth.get_session()
            if session and session.user:
                return {
                    "status": "active",
                    "user_id": session.user.id,
                    "email": session.user.email
                }
            else:
                # Fallback to .env
                user_id = os.getenv("USER_AUTH_ID", "").strip().strip("'").strip('"')
                return {
                    "status": "fallback",
                    "user_id": user_id or "anonymous",
                    "email": os.getenv("USER_EMAIL", "anonymous")
                }
        except Exception as e:
            print(f"// DB: Session check error - {e}")
            return {"status": "error", "user_id": "anonymous"}


# Global singleton instance
_db_connection = None

def get_db_connection() -> DatabaseConnection:
    """Get or create the database connection singleton."""
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection()
    return _db_connection

def get_client() -> Client:
    """Shortcut to get the Supabase client."""
    return get_db_connection().client
