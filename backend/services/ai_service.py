"""
AI Service for handling OpenAI API interactions
"""
from openai import OpenAI
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class AIService:
    """Service class for AI-powered responses using OpenAI"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", 
                 max_tokens: int = 500, temperature: float = 0.7):
        """
        Initialize AI Service
        
        Args:
            api_key: OpenAI API key
            model: OpenAI model to use
            max_tokens: Maximum tokens in response
            temperature: Response creativity (0.0 to 1.0)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
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
        
        # Store conversation histories by session
        self.conversations: Dict[str, List[Dict]] = {}
        
        logger.info(f"AI Service initialized with model: {model}")
    
    def generate_response(self, message: str, conversation_id: Optional[str] = None) -> Dict:
        """
        Generate AI response for user message
        
        Args:
            message: User's message
            conversation_id: Optional conversation ID for maintaining history
            
        Returns:
            Dict containing response and conversation_id
        """
        try:
            # Get or create conversation history
            if conversation_id and conversation_id in self.conversations:
                conversation_history = self.conversations[conversation_id]
            else:
                conversation_history = []
                if not conversation_id:
                    conversation_id = self._generate_conversation_id()
            
            # Add user message to history
            conversation_history.append({
                "role": "user",
                "content": message
            })
            
            # Prepare messages for API
            messages = [
                {"role": "system", "content": self.system_prompt},
                *conversation_history
            ]
            
            # Call OpenAI API
            logger.info(f"Generating response for conversation: {conversation_id}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Extract assistant's response
            assistant_message = response.choices[0].message.content.strip()
            
            # Add assistant response to history
            conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Store updated conversation (keep last 10 messages)
            self.conversations[conversation_id] = conversation_history[-10:]
            
            logger.info(f"Response generated successfully for conversation: {conversation_id}")
            
            return {
                "response": assistant_message,
                "conversation_id": conversation_id,
                "model": self.model
            }
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            raise Exception(f"Failed to generate AI response: {str(e)}")
    
    def reset_conversation(self, conversation_id: str) -> bool:
        """
        Reset conversation history for a given ID
        
        Args:
            conversation_id: Conversation ID to reset
            
        Returns:
            True if reset successful
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info(f"Conversation reset: {conversation_id}")
            return True
        return False
    
    def get_conversation_history(self, conversation_id: str) -> List[Dict]:
        """
        Get conversation history for a given ID
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            List of conversation messages
        """
        return self.conversations.get(conversation_id, [])
    
    @staticmethod
    def _generate_conversation_id() -> str:
        """Generate unique conversation ID"""
        import uuid
        return str(uuid.uuid4())
