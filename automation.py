"""
Automation Module - Execute system commands and automate tasks
"""

import logging
import os
import subprocess
import webbrowser
from config import APPS_PATH, COMMON_WEBSITES, DANGEROUS_COMMANDS_ENABLED

logger = logging.getLogger(__name__)

class Automation:
    """Handle system automation and command execution"""
    
    def __init__(self):
        """Initialize automation"""
        self.apps_path = APPS_PATH
        self.websites = COMMON_WEBSITES
        logger.info("✅ Automation initialized")
    
    def execute(self, command: str) -> str:
        """
        Execute automation command
        
        Args:
            command: Command to execute
            
        Returns:
            Response message
        """
        command_lower = command.lower()
        
        # Open application
        if 'open' in command_lower:
            return self.open_application(command)
        
        # Search web
        elif 'search' in command_lower or 'google' in command_lower:
            return self.search_web(command)
        
        # Open website
        elif any(site in command_lower for site in self.websites):
            return self.open_website(command)
        
        else:
            return "I'm not sure how to do that."
    
    def open_application(self, command: str) -> str:
        """Open an application"""
        try:
            for app_name, app_path in self.apps_path.items():
                if app_name in command.lower():
                    subprocess.Popen(app_path)
                    logger.info(f"Opened: {app_name}")
                    return f"Opening {app_name}..."
            
            return "Application not found in my database."
        
        except Exception as e:
            logger.error(f"Error opening application: {e}")
            return f"Could not open application: {e}"
    
    def search_web(self, query: str) -> str:
        """Search on Google"""
        try:
            # Remove search keywords
            query = query.replace('search', '').replace('google', '').strip()
            
            search_url = f"https://www.google.com/search?q={query}"
            webbrowser.open(search_url)
            
            logger.info(f"Searched for: {query}")
            return f"Searching for {query}..."
        
        except Exception as e:
            logger.error(f"Search error: {e}")
            return "Could not perform search."
    
    def open_website(self, command: str) -> str:
        """Open website"""
        try:
            for site_name, site_url in self.websites.items():
                if site_name in command.lower():
                    webbrowser.open(site_url)
                    logger.info(f"Opened: {site_name}")
                    return f"Opening {site_name}..."
            
            return "Website not found."
        
        except Exception as e:
            logger.error(f"Error opening website: {e}")
            return "Could not open website."
    
    def get_system_info(self) -> str:
        """Get system information"""
        try:
            import platform
            system = platform.platform()
            return f"Running {system}"
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return "Could not retrieve system information."