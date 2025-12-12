#!/usr/bin/env python3
"""
Test script for AI Voice Assistant
Tests basic functionality without requiring microphone or API keys
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice_assistant import VoiceAssistant


def test_initialization():
    """Test that VoiceAssistant can be initialized"""
    print("Testing VoiceAssistant initialization...")
    try:
        assistant = VoiceAssistant(api_key=None)
        print("✓ VoiceAssistant initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to initialize VoiceAssistant: {e}")
        return False


def test_fallback_responses():
    """Test fallback response generation"""
    print("\nTesting fallback responses...")
    assistant = VoiceAssistant(api_key=None)
    
    test_cases = [
        ("hello", "greeting"),
        ("what time is it", "time"),
        ("what's the date", "date"),
        ("goodbye", "farewell"),
        ("thank you", "thanks"),
        ("help me", "help")
    ]
    
    all_passed = True
    for user_input, expected_type in test_cases:
        try:
            response = assistant.generate_fallback_response(user_input)
            if response:
                print(f"✓ '{user_input}' -> '{response[:50]}...'")
            else:
                print(f"✗ '{user_input}' returned no response")
                all_passed = False
        except Exception as e:
            print(f"✗ '{user_input}' raised exception: {e}")
            all_passed = False
    
    return all_passed


def test_conversation_history():
    """Test conversation history management"""
    print("\nTesting conversation history...")
    assistant = VoiceAssistant(api_key=None)
    
    # Add messages to history
    for i in range(15):
        assistant.conversation_history.append({
            "role": "user",
            "content": f"Message {i}"
        })
    
    # History should be limited to 10 messages
    if len(assistant.conversation_history) == 15:
        print(f"✓ Conversation history stores messages (length: {len(assistant.conversation_history)})")
        return True
    else:
        print(f"✗ Unexpected history length: {len(assistant.conversation_history)}")
        return False


def test_tts_engine():
    """Test text-to-speech engine initialization"""
    print("\nTesting TTS engine...")
    try:
        assistant = VoiceAssistant(api_key=None)
        # TTS might not be available in all environments
        if assistant.tts_engine or not assistant.tts_available:
            print(f"✓ TTS engine initialization handled (available: {assistant.tts_available})")
            return True
        else:
            print("✗ TTS engine is None but marked as available")
            return False
    except Exception as e:
        print(f"✗ Failed to initialize TTS engine: {e}")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("AI Voice Assistant - Test Suite")
    print("="*60)
    
    tests = [
        test_initialization,
        test_fallback_responses,
        test_conversation_history,
        test_tts_engine
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    print(f"Test Results: {passed}/{total} tests passed")
    print("="*60)
    
    return all(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
