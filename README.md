# AI-Voice-Assistant

An intelligent voice assistant powered by AI that can listen to your voice commands, process them using artificial intelligence, and respond back with natural speech.

## Features

- 🎤 **Speech Recognition**: Converts your voice into text using Google Speech Recognition
- 🤖 **AI-Powered Responses**: Uses OpenAI's GPT-3.5 to generate intelligent and contextual responses
- 🔊 **Text-to-Speech**: Converts AI responses back to natural-sounding speech
- 💬 **Conversation History**: Maintains context across multiple interactions
- 🔄 **Fallback Mode**: Works with basic functionality even without OpenAI API key
- ⚡ **Real-time Processing**: Fast response times for seamless interaction

## Prerequisites

- Python 3.7 or higher
- Microphone for voice input
- Speakers or headphones for audio output
- OpenAI API key (optional, but recommended for full AI features)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/moizmalik11/AI-Voice-Assistant.git
   cd AI-Voice-Assistant
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

## Configuration

### OpenAI API Key

To enable full AI-powered features, you need an OpenAI API key:

1. Sign up at [OpenAI](https://platform.openai.com/)
2. Generate an API key from the [API Keys page](https://platform.openai.com/api-keys)
3. Add the key to your `.env` file:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

Alternatively, you can set it as an environment variable:
```bash
export OPENAI_API_KEY='your_actual_api_key_here'
```

### Without OpenAI API Key

The assistant will still work without an API key but with limited functionality:
- Basic pattern matching for common queries
- Time and date information
- Simple conversational responses

## Usage

Run the voice assistant:

```bash
python voice_assistant.py
```

### How to Interact

1. **Start the assistant**: Run the script and wait for the initialization message
2. **Speak your command**: Simply start speaking when you see "Listening..."
3. **Wait for response**: The assistant will process your input and respond
4. **Continue conversation**: Keep talking - the assistant maintains conversation context
5. **Exit**: Say "exit", "quit", or "goodbye" to stop the assistant

### Example Interactions

```
You: "Hello, how are you?"
Assistant: "Hello! I'm doing well, thank you for asking! How can I assist you?"

You: "What's the current time?"
Assistant: "The current time is 3:45 PM"

You: "Tell me a joke"
Assistant: "Why did the programmer quit his job? Because he didn't get arrays!"

You: "Goodbye"
Assistant: "Goodbye! Have a great day!"
```

## Troubleshooting

### Microphone Issues

If the assistant can't hear you:
- Check your microphone is properly connected
- Verify microphone permissions are granted
- Test your microphone with other applications

### Installation Issues

**PyAudio installation fails:**
- On Ubuntu/Debian: `sudo apt-get install portaudio19-dev python3-pyaudio`
- On macOS: `brew install portaudio`
- On Windows: Download the appropriate `.whl` file from [PyAudio wheels](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

**Speech recognition errors:**
- Ensure you have an active internet connection (Google Speech Recognition requires internet)
- Check your microphone is working properly

### API Issues

If AI responses aren't working:
- Verify your OpenAI API key is correct
- Check you have available credits in your OpenAI account
- Ensure the API key is properly set in your environment

## Project Structure

```
AI-Voice-Assistant/
├── voice_assistant.py   # Main application file
├── requirements.txt     # Python dependencies
├── .env.example        # Example environment configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## How It Works

1. **Speech Recognition**: The assistant uses the `speech_recognition` library to capture audio from your microphone and convert it to text using Google's Speech Recognition API.

2. **AI Processing**: The text is sent to OpenAI's GPT-3.5 model, which generates an intelligent, contextual response based on the conversation history.

3. **Text-to-Speech**: The AI's response is converted back to speech using the `pyttsx3` library, which uses the system's built-in text-to-speech engine.

4. **Conversation Management**: The assistant maintains a conversation history to provide context-aware responses across multiple interactions.

## Privacy & Security

- Voice data is processed using Google's Speech Recognition API
- Conversation data is sent to OpenAI's API (when enabled)
- API keys are stored in environment variables, not in code
- The `.env` file is excluded from version control

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- [SpeechRecognition](https://github.com/Uberi/speech_recognition) for voice input
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) for text-to-speech
- [OpenAI](https://openai.com/) for AI-powered responses

## Support

If you encounter any issues or have questions, please open an issue on GitHub.