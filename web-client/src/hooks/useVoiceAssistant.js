import { useState, useEffect, useRef } from 'react';
import apiService from '../services/api';

const useVoiceAssistant = () => {
    const [isListening, setIsListening] = useState(false);
    const [messages, setMessages] = useState([]); // Array of { role: 'user'|'assistant', text: string }
    const [recognition, setRecognition] = useState(null);

    // Initialize Speech Recognition
    useEffect(() => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (SpeechRecognition) {
            const recognitionInstance = new SpeechRecognition();
            recognitionInstance.continuous = false; // Stop after one phrase
            recognitionInstance.lang = 'en-US';
            recognitionInstance.interimResults = false;

            recognitionInstance.onstart = () => setIsListening(true);
            recognitionInstance.onend = () => setIsListening(false);

            recognitionInstance.onresult = (event) => {
                const text = event.results[0][0].transcript;
                if (text) {
                    handleUserMessage(text);
                }
            };

            setRecognition(recognitionInstance);
        } else {
            console.error("Speech Recognition not supported in this browser.");
        }
    }, []);

    const startListening = () => {
        if (recognition) {
            try {
                recognition.start();
            } catch (e) {
                console.error("Recognition already started", e);
            }
        }
    };

    const stopListening = () => {
        if (recognition) {
            recognition.stop();
        }
    };

    const handleUserMessage = async (text) => {
        // Add User Message
        const userMsg = { role: 'user', text };
        setMessages(prev => [...prev, userMsg]);

        // Call Backend API for AI Response
        try {
            const result = await apiService.sendMessage(text);

            if (result.success) {
                const aiMsg = { role: 'assistant', text: result.response };
                setMessages(prev => [...prev, aiMsg]);
            } else {
                // Show error message
                const errorMsg = {
                    role: 'assistant',
                    text: `Error: ${result.error || 'Failed to get response from AI'}`
                };
                setMessages(prev => [...prev, errorMsg]);
            }
        } catch (error) {
            console.error('Error calling API:', error);
            const errorMsg = {
                role: 'assistant',
                text: 'Sorry, I encountered an error. Please make sure the backend server is running.'
            };
            setMessages(prev => [...prev, errorMsg]);
        }
    };

    const speakText = (text) => {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1;
            utterance.pitch = 1;
            window.speechSynthesis.speak(utterance);
        }
    };

    return {
        isListening,
        messages,
        startListening,
        stopListening,
        speakText
    };
};

export default useVoiceAssistant;
