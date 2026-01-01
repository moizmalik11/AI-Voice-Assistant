"""
AI Voice Assistant Backend API
Flask server for handling AI chat requests
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging

from config import Config
from services import AIService

# Configure logging


# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": Config.CORS_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize AI Service
try:
    Config.validate()
    ai_service = AIService(
        api_key=Config.OPENAI_API_KEY,
        model=Config.OPENAI_MODEL,
        max_tokens=Config.MAX_TOKENS,
        temperature=Config.TEMPERATURE
    )
    logger.info("AI Service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize AI Service: {e}")
    ai_service = None


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "ai_service": "ready" if ai_service else "not initialized"
    }), 200


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat endpoint - Process user message and return AI response
    
    Request body:
    {
        "message": "User's message",
        "conversation_id": "optional-session-id"
    }
    
    Response:
    {
        "response": "AI's response",
        "conversation_id": "session-id",
        "timestamp": "ISO timestamp"
    }
    """
    try:
        # Check if AI service is available
        if not ai_service:
            return jsonify({
                "error": "AI service not initialized. Please check API key configuration."
            }), 503
        
        # Get request data
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Missing 'message' in request body"
            }), 400
        
        message = data['message'].strip()
        
        if not message:
            return jsonify({
                "error": "Message cannot be empty"
            }), 400
        
        conversation_id = data.get('conversation_id')
        
        logger.info(f"Processing chat request: {message[:50]}...")
        
        # Generate AI response
        result = ai_service.generate_response(message, conversation_id)
        
        # Return response
        return jsonify({
            "response": result['response'],
            "conversation_id": result['conversation_id'],
            "model": result['model'],
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        return jsonify({
            "error": "Failed to process request",
            "details": str(e)
        }), 500


@app.route('/api/conversation/reset', methods=['POST'])
def reset_conversation():
    """
    Reset conversation history
    
    Request body:
    {
        "conversation_id": "session-id"
    }
    """
    try:
        if not ai_service:
            return jsonify({
                "error": "AI service not initialized"
            }), 503
        
        data = request.get_json()
        
        if not data or 'conversation_id' not in data:
            return jsonify({
                "error": "Missing 'conversation_id' in request body"
            }), 400
        
        conversation_id = data['conversation_id']
        success = ai_service.reset_conversation(conversation_id)
        
        return jsonify({
            "success": success,
            "message": "Conversation reset successfully" if success else "Conversation not found"
        }), 200
        
    except Exception as e:
        logger.error(f"Error resetting conversation: {e}")
        return jsonify({
            "error": "Failed to reset conversation",
            "details": str(e)
        }), 500


@app.route('/api/conversation/history', methods=['POST'])
def get_conversation_history():
    """
    Get conversation history
    
    Request body:
    {
        "conversation_id": "session-id"
    }
    """
    try:
        if not ai_service:
            return jsonify({
                "error": "AI service not initialized"
            }), 503
        
        data = request.get_json()
        
        if not data or 'conversation_id' not in data:
            return jsonify({
                "error": "Missing 'conversation_id' in request body"
            }), 400
        
        conversation_id = data['conversation_id']
        history = ai_service.get_conversation_history(conversation_id)
        
        return jsonify({
            "conversation_id": conversation_id,
            "history": history,
            "message_count": len(history)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        return jsonify({
            "error": "Failed to get conversation history",
            "details": str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    logger.info(f"Starting AI Voice Assistant Backend on {Config.HOST}:{Config.PORT}")
    logger.info(f"Environment: {Config.FLASK_ENV}")
    logger.info(f"CORS Origins: {Config.CORS_ORIGINS}")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
