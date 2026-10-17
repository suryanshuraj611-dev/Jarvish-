"""
Main Jarvis class - Core AI Assistant
"""

import logging
import time
from datetime import datetime
from typing import Optional

from voice_recognition_module import VoiceRecognizer
from text_to_speech import TextToSpeech
from ai_brain import AIBrain
from automation import Automation
from database.db_handler import DatabaseHandler
from config import WAKE_WORD, CONTEXT_LENGTH

logger = logging.getLogger(__name__)

class Jarvis:
    """Main Jarvis AI Assistant Class"""
    
    def __init__(self):
        """Initialize Jarvis with all components"""
        logger.info("Initializing Jarvis...")
        
        self.voice_recognizer = VoiceRecognizer()
        self.text_to_speech = TextToSpeech()
        self.ai_brain = AIBrain()
        self.automation = Automation()
        self.database = DatabaseHandler()
        
        self.conversation_history = []
        self.is_active = False
        
        logger.info("✅ Jarvis initialized successfully")
        print("✅ Jarvis Ready!")
    
    def wake_up(self, command: str) -> bool:
        """Check if wake word is detected"""
        return WAKE_WORD.lower() in command.lower()
    
    def process_command(self, command: str) -> str:
        """
        Process user command and generate response
        
        Args:
            command: User's voice command
            
        Returns:
            AI response
        """
        logger.info(f"Processing command: {command}")
        
        # Check for wake word
        if not self.wake_up(command):
            return None
        
        # Remove wake word
        command = command.replace(WAKE_WORD, "").strip()
        
        # Check for automation commands
        if self.is_automation_command(command):
            response = self.automation.execute(command)
            return response
        
        # Use AI to generate response
        response = self.ai_brain.get_response(command, self.conversation_history)
        
        # Update conversation history
        self.update_history(command, response)
        
        # Save to database
        self.database.save_interaction(command, response)
        
        return response
    
    def is_automation_command(self, command: str) -> bool:
        """Check if command is for automation"""
        automation_keywords = ['open', 'close', 'launch', 'search', 'google', 
                              'chrome', 'notepad', 'calculator', 'run', 'execute']
        return any(keyword in command.lower() for keyword in automation_keywords)
    
    def update_history(self, user_input: str, response: str):
        """Update conversation history"""
        self.conversation_history.append({
            'user': user_input,
            'assistant': response,
            'timestamp': datetime.now()
        })
        
        # Keep only last N interactions
        if len(self.conversation_history) > CONTEXT_LENGTH:
            self.conversation_history.pop(0)
    
    def listen_and_respond(self):
        """Main loop - Listen and respond to commands"""
        self.is_active = True
        
        while self.is_active:
            try:
                # Listen for command
                print("\n🎤 Listening...")
                command = self.voice_recognizer.recognize()
                
                if not command:
                    continue
                
                print(f"👤 You: {command}")
                
                # Process command
                response = self.process_command(command)
                
                if response:
                    print(f"🤖 Jarvis: {response}")
                    self.text_to_speech.speak(response)
                
                # Check for exit command
                if self.is_exit_command(command):
                    break
                
                time.sleep(0.5)
            
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                print(f"❌ Error: {e}")
    
    def is_exit_command(self, command: str) -> bool:
        """Check if user wants to exit"""
        exit_commands = ['exit', 'quit', 'goodbye', 'bye', 'stop listening']
        return any(cmd in command.lower() for cmd in exit_commands)
    
    def get_history(self) -> list:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def shutdown(self):
        """Shutdown Jarvis"""
        logger.info("Shutting down Jarvis...")
        self.is_active = False
        self.text_to_speech.speak("Goodbye!")