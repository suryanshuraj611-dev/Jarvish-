"""
Text-to-Speech Module - Speech output
"""

import logging
import pyttsx3
from config import TTS_ENGINE, TTS_LANGUAGE, TTS_SPEED, TTS_VOLUME

logger = logging.getLogger(__name__)

class TextToSpeech:
    """Handle text-to-speech conversion"""
    
    def __init__(self):
        """Initialize TTS engine"""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', TTS_SPEED)
            self.engine.setProperty('volume', TTS_VOLUME)
            
            # Set voice
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)
            
            logger.info("✅ Text-to-Speech initialized")
        except Exception as e:
            logger.error(f"TTS initialization error: {e}")
            raise
    
    def speak(self, text: str) -> bool:
        """
        Convert text to speech and play
        
        Args:
            text: Text to speak
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not text:
                return False
            
            logger.info(f"Speaking: {text[:50]}...")
            self.engine.say(text)
            self.engine.runAndWait()
            
            return True
        
        except Exception as e:
            logger.error(f"TTS error: {e}")
            print(f"❌ Speech error: {e}")
            return False
    
    def set_speed(self, speed: int):
        """Set speech speed"""
        self.engine.setProperty('rate', speed)
    
    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0)"""
        self.engine.setProperty('volume', max(0, min(1, volume)))