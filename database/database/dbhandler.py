"""
Database Handler - Store and retrieve conversation history
"""

import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from config import DATABASE_PATH

logger = logging.getLogger(__name__)

class DatabaseHandler:
    """Handle database operations"""
    
    def __init__(self):
        """Initialize database"""
        self.db_path = DATABASE_PATH
        Path(self.db_path).parent.mkdir(exist_ok=True)
        self.create_tables()
        logger.info("✅ Database initialized")
    
    def create_tables(self):
        """Create necessary tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create interactions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_input TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create preferences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    key TEXT NOT NULL,
                    value TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database tables created successfully")
        
        except Exception as e:
            logger.error(f"Database creation error: {e}")
    
    def save_interaction(self, user_input: str, ai_response: str) -> bool:
        """Save interaction to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO interactions (user_input, ai_response)
                VALUES (?, ?)
            ''', (user_input, ai_response))
            
            conn.commit()
            conn.close()
            
            logger.info("Interaction saved to database")
            return True
        
        except Exception as e:
            logger.error(f"Error saving interaction: {e}")
            return False
    
    def get_interactions(self, limit: int = 10) -> list:
        """Get recent interactions"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_input, ai_response, timestamp 
                FROM interactions 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            interactions = cursor.fetchall()
            conn.close()
            
            return interactions
        
        except Exception as e:
            logger.error(f"Error fetching interactions: {e}")
            return []
    
    def clear_interactions(self) -> bool:
        """Clear all interactions"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM interactions')
            conn.commit()
            conn.close()
            
            logger.info("Interactions cleared")
            return True
        
        except Exception as e:
            logger.error(f"Error clearing interactions: {e}")
            return False