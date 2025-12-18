# AI Voice Assistant

An intelligent voice assistant powered by AI that can listen to your voice commands, process them using artificial intelligence, and respond back with natural speech.

## 🏗️ Architecture

This project consists of two main components:

- **Backend (Python Flask)**: Handles all AI processing using OpenAI's GPT models
- **Frontend (React)**: Provides a modern web interface for voice interaction

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐
│  React Frontend │ ──────▶ │  Flask Backend   │ ──────▶ │  OpenAI API │
│  (Web Client)   │ ◀────── │  (Python)        │ ◀────── │  (GPT-3.5)  │
└─────────────────┘         └──────────────────┘         └─────────────┘
      Voice Input                AI Processing              AI Response
```

## ✨ Features

- 🎤 **Browser-based Speech Recognition**: Uses Web Speech API for voice input
- 🤖 **AI-Powered Responses**: OpenAI GPT-3.5-turbo generates intelligent, contextual responses
- 🔊 **Text-to-Speech**: Browser-based speech synthesis for voice output
- 💬 **Conversation History**: Maintains context across multiple interactions
- 🌐 **Modern Web Interface**: Beautiful, responsive React UI
- 🔒 **Secure**: API keys stored in environment variables
- ⚡ **Real-time Processing**: Fast response times for seamless interaction

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Modern web browser (Chrome, Edge, or Safari recommended for best voice support)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/moizmalik11/AI-Voice-Assistant.git
cd AI-Voice-Assistant
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
copy .env.example .env
# Edit .env and add your OpenAI API key

# Start the backend server
python app.py
```

The backend will start on `http://localhost:5000`

### 3. Frontend Setup

Open a new terminal:

```bash
# Navigate to web client directory
cd web-client

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start on `http://localhost:5173`

### 4. Open in Browser

Visit `http://localhost:5173` and start talking to your AI assistant!

## 📁 Project Structure

```
AI-Voice-Assistant/
├── backend/                    # Python Flask backend
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration management
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment template
│   ├── README.md             # Backend documentation
│   └── services/
│       ├── __init__.py
│       └── ai_service.py     # OpenAI integration
│
├── web-client/                # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── services/        # API service layer
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Entry point
│   ├── package.json
│   └── README.md
│
├── gui_app.py                 # Desktop GUI (separate app)
├── voice_assistant.py         # CLI voice assistant (legacy)
├── .gitignore
└── README.md                  # This file
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env`:

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

### Frontend Configuration

Edit `web-client/.env`:

```env
VITE_API_URL=http://localhost:5000
```

## 🎯 Usage

1. **Start Backend**: Make sure the Flask backend is running
2. **Start Frontend**: Open the React app in your browser
3. **Click Microphone**: Click the microphone button to start listening
4. **Speak**: Say your question or command
5. **Get Response**: The AI will respond with text and voice

### Example Interactions

- "What is artificial intelligence?"
- "Tell me a joke"
- "What's the weather like?" (AI will explain it can't access real-time data)
- "Explain quantum computing in simple terms"
- "Write a short poem about coding"

## 🛠️ API Endpoints

The backend provides the following REST API endpoints:

- `GET /api/health` - Health check
- `POST /api/chat` - Send message and get AI response
- `POST /api/conversation/reset` - Reset conversation history
- `POST /api/conversation/history` - Get conversation history

See [backend/README.md](backend/README.md) for detailed API documentation.

## 🎨 Additional Applications

### Desktop GUI Application

A standalone desktop application is also available:

```bash
python gui_app.py
```

This uses CustomTkinter for a native desktop experience.

### CLI Voice Assistant

For command-line usage:

```bash
python voice_assistant.py
```

## 🔍 Troubleshooting

### Backend Issues

**"AI service not initialized"**
- Check that `OPENAI_API_KEY` is set in `backend/.env`
- Verify the API key is valid

**CORS errors**
- Ensure `CORS_ORIGINS` in `backend/.env` includes your frontend URL

### Frontend Issues

**"Cannot connect to server"**
- Make sure the backend is running on `http://localhost:5000`
- Check `VITE_API_URL` in `web-client/.env`

**Voice input not working**
- Use Chrome, Edge, or Safari (best browser support)
- Grant microphone permissions when prompted
- Check browser console for errors

## 🔒 Security Notes

- Never commit `.env` files to version control
- Keep your OpenAI API key secure
- Use HTTPS in production
- The `.env.example` files are safe templates without real keys

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for GPT-3.5 API
- [Flask](https://flask.palletsprojects.com/) for the backend framework
- [React](https://react.dev/) for the frontend framework
- [Vite](https://vitejs.dev/) for fast development
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) for browser-based speech recognition

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ by [Moiz Malik](https://github.com/moizmalik11)**