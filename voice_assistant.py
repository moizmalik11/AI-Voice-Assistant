#!/usr/bin/env python3
"""
AI-Powered Voice Assistant
A voice assistant that uses speech recognition, AI processing, and text-to-speech
"""

import speech_recognition as sr
import pyttsx3
import openai
import os
import sys
from datetime import datetime
import json


class VoiceAssistant:
    """Main Voice Assistant class"""
    
    def __init__(self, api_key=None):
        """Initialize the voice assistant with necessary components"""
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Initialize OpenAI API
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
        
        # Conversation history
        self.conversation_history = []
        
        # Wake word
        self.wake_word = "assistant"
        
        print("Voice Assistant initialized successfully!")
        
    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self):
        """Listen for voice input and convert to text"""
        with self.microphone as source:
            print("Listening...")
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Processing speech...")
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return None
    
    def generate_ai_response(self, user_input):
        """Generate AI response using OpenAI API"""
        if not self.api_key:
            # Fallback responses if no API key
            return self.generate_fallback_response(user_input)
        
        try:
            # Add user message to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Generate response using OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful voice assistant. Provide concise and friendly responses."},
                    *self.conversation_history
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            assistant_message = response.choices[0].message.content.strip()
            
            # Add assistant response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Keep conversation history manageable (last 10 messages)
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return assistant_message
            
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return "I'm having trouble processing that right now. Could you try again?"
    
    def generate_fallback_response(self, user_input):
        """Generate basic responses without AI API"""
        user_input_lower = user_input.lower()
        
        # Simple pattern matching for common queries
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! How can I help you today?"
        elif any(word in user_input_lower for word in ['how are you', 'how do you do']):
            return "I'm doing well, thank you for asking! How can I assist you?"
        elif 'time' in user_input_lower:
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}"
        elif 'date' in user_input_lower:
            current_date = datetime.now().strftime("%B %d, %Y")
            return f"Today's date is {current_date}"
        elif any(word in user_input_lower for word in ['bye', 'goodbye', 'exit', 'quit']):
            return "Goodbye! Have a great day!"
        elif 'thank' in user_input_lower:
            return "You're welcome! Is there anything else I can help you with?"
        elif 'help' in user_input_lower:
            return "I can help you with various tasks. Try asking me about the time, date, or just have a conversation!"
        else:
            return "I understand you said: " + user_input + ". How can I help you with that?"
    
    def process_command(self, text):
        """Process voice command and take appropriate action"""
        if not text:
            return False
        
        text_lower = text.lower()
        
        # Check for exit commands
        if any(word in text_lower for word in ['exit', 'quit', 'stop', 'goodbye']):
            self.speak("Goodbye! Have a great day!")
            return True
        
        # Generate and speak response
        response = self.generate_ai_response(text)
        self.speak(response)
        
        return False
    
    def run(self):
        """Main loop to run the voice assistant"""
        self.speak(f"Hello! I am your AI voice assistant. Say '{self.wake_word}' followed by your command, or just start speaking.")
        
        listening_mode = True
        
        while True:
            try:
                # Listen for input
                text = self.listen()
                
                if text:
                    # Check if wake word is present or we're in continuous listening mode
                    if listening_mode or self.wake_word in text.lower():
                        # Remove wake word from text
                        text = text.replace(self.wake_word, "").replace(self.wake_word.capitalize(), "").strip()
                        
                        if text:
                            # Process the command
                            should_exit = self.process_command(text)
                            if should_exit:
                                break
                
            except KeyboardInterrupt:
                self.speak("Shutting down. Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue


def main():
    """Main entry point"""
    print("="*50)
    print("AI-Powered Voice Assistant")
    print("="*50)
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\nWarning: OPENAI_API_KEY not found in environment variables.")
        print("The assistant will work with limited functionality.")
        print("To enable AI features, set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'\n")
    
    try:
        # Create and run assistant
        assistant = VoiceAssistant(api_key=api_key)
        assistant.run()
    except Exception as e:
        print(f"Failed to start voice assistant: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
