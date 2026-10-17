"""
AI Brain Module - Intelligent responses using OpenAI
"""

import logging
import openai
from typing import List, Dict
from config import OPENAI_API_KEY, AI_MODEL, AI_TEMPERATURE, MAX_TOKENS, SYSTEM_PROMPT

logger = logging.getLogger(__name__)

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

class AIBrain:
    """Handle AI logic and responses"""
    
    def __init__(self):
        """Initialize AI Brain"""
        self.model = AI_MODEL
        self.temperature = AI_TEMPERATURE
        self.max_tokens = MAX_TOKENS
        self.system_prompt = SYSTEM_PROMPT
        
        logger.info("✅ AI Brain initialized")
    
    def get_response(self, user_input: str, conversation_history: List[Dict] = None) -> str:
        """
        Get AI response to user input
        
        Args:
            user_input: User's message
            conversation_history: Previous conversation for context
            
        Returns:
            AI response
        """
        try:
            # Build messages list
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add conversation history
            if conversation_history:
                for interaction in conversation_history[-3:]:  # Last 3 interactions
                    messages.append({"role": "user", "content": interaction.get('user', '')})
                    messages.append({"role": "assistant", "content": interaction.get('assistant', '')})
            
            # Add current user input
            messages.append({"role": "user", "content": user_input})
            
            # Get response from OpenAI
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            assistant_message = response.choices[0].message['content'].strip()
            logger.info(f"AI Response: {assistant_message[:50]}...")
            
            return assistant_message
        
        except openai.error.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            return "I'm having trouble connecting to my AI brain. Please check your API key."
        
        except openai.error.RateLimitError:
            logger.warning("OpenAI rate limit exceeded")
            return "I'm receiving too many requests. Please wait a moment."
        
        except Exception as e:
            logger.error(f"AI error: {e}")
            return f"I encountered an error: {str(e)}"
    
    def get_simple_response(self, user_input: str) -> str:
        """Get simple response without conversation history"""
        return self.get_response(user_input)