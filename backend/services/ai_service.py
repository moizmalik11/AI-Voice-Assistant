"""
AI Service for handling Google Gemini API interactions
"""
from google import genai
from google.genai import types
from google.genai.errors import APIError
from typing import List, Dict, Optional
import logging
import time
import uuid

logger = logging.getLogger(__name__)

class AIService:
    """Service class for AI-powered responses using Gemini with Round-Robin Keys"""
    
    def __init__(self, api_keys: List[str], model: str = "gemini-2.0-flash", 
                 max_tokens: int = 500, temperature: float = 0.7):
        """
        Initialize AI Service with a list of API keys for round-robin usage.
        """
        self.api_keys = api_keys
        self.current_key_index = 0
        
        # Initialize a client for each API key
        self.clients = [genai.Client(api_key=key) for key in api_keys]
        
        self.model_name = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        # System prompt for the assistant
        self.system_prompt = """You are a helpful and friendly AI voice assistant. 
Your responses should be:
- Concise and clear (suitable for voice output)
- Helpful and informative
- Natural and conversational
- Appropriate for general audiences

Keep responses brief unless the user asks for detailed information."""
        
        # Store raw history for the stateless API calls
        self.history_logs: Dict[str, List[Dict]] = {}
        
        logger.info(f"AI Service initialized with model: {model} and {len(api_keys)} keys.")
    
    def _rotate_key(self):
        """Rotate to the next API key in the list."""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        logger.info(f"Rotated to API key index: {self.current_key_index}")
        
    def _get_client(self):
        return self.clients[self.current_key_index]

    def warmup(self) -> bool:
        """Ping the API to warm it up without saving history."""
        try:
            client = self._get_client()
            client.models.generate_content(
                model=self.model_name,
                contents="ping"
            )
            return True
        except Exception as e:
            logger.warning(f"Warmup failed: {e}")
            self._rotate_key()
            return False
    
    def generate_response(self, message: str, conversation_id: Optional[str] = None) -> Dict:
        """
        Generate AI response for user message with round-robin retry logic.
        """
        if not conversation_id:
            conversation_id = self._generate_conversation_id()
            
        if conversation_id not in self.history_logs:
            self.history_logs[conversation_id] = []
            
        # Log user message
        self.history_logs[conversation_id].append({
            "role": "user",
            "content": message
        })
        
        # Prepare content payload for the API
        contents = []
        for msg in self.history_logs[conversation_id]:
            contents.append(
                types.Content(role=msg["role"], parts=[types.Part.from_text(text=msg["content"])])
            )
            
        # Retry logic: Try each key exactly once per request if there's an error
        attempts = 0
        max_attempts = len(self.clients)
        
        last_error = None
        
        while attempts < max_attempts:
            client = self._get_client()
            logger.info(f"Generating response for {conversation_id} using key index {self.current_key_index}")
            
            try:
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_prompt,
                        temperature=self.temperature,
                        max_output_tokens=self.max_tokens,
                    )
                )
                
                assistant_message = response.text.strip()
                
                # Log assistant response
                self.history_logs[conversation_id].append({
                    "role": "model",  # Gemini uses 'model' instead of 'assistant' in contents
                    "content": assistant_message
                })
                
                logger.info(f"Response generated successfully for conversation: {conversation_id}")
                
                # Rotate key for the next request to balance load across all keys
                self._rotate_key()
                
                return {
                    "response": assistant_message,
                    "conversation_id": conversation_id,
                    "model": self.model_name
                }
                
            except APIError as e:
                # e.g., 429 Resource Exhausted, 403 Forbidden, etc.
                logger.warning(f"API Error with key index {self.current_key_index}: {e}")
                last_error = e
                self._rotate_key()
                attempts += 1
                if "503" in str(e) or "429" in str(e):
                    time.sleep(1.5)
            except Exception as e:
                logger.error(f"Unexpected error with key index {self.current_key_index}: {e}")
                last_error = e
                self._rotate_key()
                attempts += 1
                
        # If we exhausted all keys
        logger.error(f"All API keys failed. Last error: {last_error}")
        raise Exception(f"Failed to generate AI response after trying all keys: {str(last_error)}")
    
    def reset_conversation(self, conversation_id: str) -> bool:
        """Reset conversation history for a given ID"""
        if conversation_id in self.history_logs:
            del self.history_logs[conversation_id]
            logger.info(f"Conversation reset: {conversation_id}")
            return True
        return False
    
    def get_conversation_history(self, conversation_id: str) -> List[Dict]:
        """Get conversation history for a given ID"""
        return self.history_logs.get(conversation_id, [])
    
    @staticmethod
    def _generate_conversation_id() -> str:
        """Generate unique conversation ID"""
        return str(uuid.uuid4())
