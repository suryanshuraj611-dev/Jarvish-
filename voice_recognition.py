"""
Voice Recognition Module - Speech to Text
"""

import logging
import speech_recognition as sr
from config import VOICE_RECOGNITION_LANGUAGE, SPEECH_RECOGNITION_TIMEOUT, SPEECH_RECOGNITION_PHRASE_LIMIT

logger = logging.getLogger(__name__)

class VoiceRecognizer:
    """Handle voice recognition and speech-to-text"""
    
    def __init__(self):
        """Initialize recognizer"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
        
        logger.info("✅ Voice Recognizer initialized")
    
    def recognize(self) -> str:
        """
        Recognize speech from microphone
        
        Returns:
            Recognized text or empty string if failed
        """
        try:
            with self.microphone as source:
                # Listen with timeout
                audio = self.recognizer.listen(
                    source, 
                    timeout=SPEECH_RECOGNITION_TIMEOUT,
                    phrase_time_limit=SPEECH_RECOGNITION_PHRASE_LIMIT
                )
            
            # Try to recognize using Google Speech Recognition
            text = self.recognizer.recognize_google(
                audio, 
                language=VOICE_RECOGNITION_LANGUAGE
            )
            
            logger.info(f"Recognized: {text}")
            return text
        
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            print("🤷 Sorry, I didn't catch that. Please repeat.")
            return ""
        
        except sr.RequestError as e:
            logger.error(f"Could not request results; {e}")
            print("❌ Network error. Please check your internet connection.")
            return ""
        
        except sr.Timeout:
            logger.warning("No speech detected")
            print("⏱️ Timeout - no speech detected")
            return ""
        
        except Exception as e:
            logger.error(f"Recognition error: {e}")
            print(f"❌ Error: {e}")
            return ""