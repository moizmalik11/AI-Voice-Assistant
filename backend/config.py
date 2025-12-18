"""
Configuration management for AI Voice Assistant Backend
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '500'))
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Flask Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    PORT = int(os.getenv('PORT', '5000'))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')
    
    # Conversation Settings
    MAX_CONVERSATION_HISTORY = int(os.getenv('MAX_CONVERSATION_HISTORY', '10'))
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required. Please set it in .env file")
        
        if not Config.OPENAI_API_KEY.startswith('sk-'):
            raise ValueError("Invalid OPENAI_API_KEY format")
        
        return True
