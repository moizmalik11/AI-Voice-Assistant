# AI Voice Assistant Backend API

Python Flask backend for the AI Voice Assistant application. This backend handles all AI processing using OpenAI's GPT models.

## Features

- 🤖 **OpenAI Integration**: Uses GPT-3.5-turbo for intelligent responses
- 💬 **Conversation Management**: Maintains conversation history per session
- 🔒 **Secure**: API key stored in environment variables
- 🌐 **CORS Enabled**: Ready for frontend integration
- 📝 **Logging**: Comprehensive logging for debugging

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   copy .env.example .env
   
   # Edit .env and add your OpenAI API key
   ```

## Configuration

Edit the `.env` file with your settings:

```env
# Required
OPENAI_API_KEY=sk-your-actual-api-key-here

# Optional (defaults shown)
OPENAI_MODEL=gpt-3.5-turbo
MAX_TOKENS=500
TEMPERATURE=0.7
PORT=5000
FLASK_ENV=development
```

## Running the Server

### Development Mode

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Production Mode

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## API Endpoints

### Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-18T05:14:24Z",
  "ai_service": "ready"
}
```

---

### Chat
```http
POST /api/chat
Content-Type: application/json

{
  "message": "What is artificial intelligence?",
  "conversation_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "Artificial intelligence (AI) is...",
  "conversation_id": "abc-123-def",
  "model": "gpt-3.5-turbo",
  "timestamp": "2025-12-18T05:14:24Z"
}
```

---

### Reset Conversation
```http
POST /api/conversation/reset
Content-Type: application/json

{
  "conversation_id": "abc-123-def"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Conversation reset successfully"
}
```

---

### Get Conversation History
```http
POST /api/conversation/history
Content-Type: application/json

{
  "conversation_id": "abc-123-def"
}
```

**Response:**
```json
{
  "conversation_id": "abc-123-def",
  "history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help you?"}
  ],
  "message_count": 2
}
```

## Project Structure

```
backend/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .env                  # Actual environment (gitignored)
├── README.md             # This file
└── services/
    ├── __init__.py
    └── ai_service.py     # OpenAI integration
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request (missing/invalid parameters)
- `404` - Endpoint not found
- `500` - Internal Server Error
- `503` - Service Unavailable (AI service not initialized)

## Logging

Logs are output to console with the following format:
```
2025-12-18 05:14:24 - app - INFO - Processing chat request: What is AI?...
```

## Security Notes

- Never commit `.env` file to version control
- Keep your OpenAI API key secure
- Use environment variables for sensitive data
- Enable HTTPS in production

## Troubleshooting

### "AI service not initialized"
- Check that your `OPENAI_API_KEY` is set in `.env`
- Verify the API key is valid and starts with `sk-`

### CORS errors
- Add your frontend URL to `CORS_ORIGINS` in `.env`
- Default allows `http://localhost:5173` and `http://localhost:3000`

### Import errors
- Ensure you're in the virtual environment
- Run `pip install -r requirements.txt` again

## Development

To add new features:

1. Create new service in `services/` directory
2. Add routes in `app.py`
3. Update configuration in `config.py` if needed
4. Update this README with new endpoints

## License

MIT License - See main project LICENSE file
