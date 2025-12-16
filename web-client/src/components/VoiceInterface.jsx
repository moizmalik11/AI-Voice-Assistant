import React, { useEffect, useRef } from 'react';
import { Mic, MicOff, Volume2, X, Circle } from 'lucide-react';
import useVoiceAssistant from '../hooks/useVoiceAssistant';

const VoiceInterface = ({ onEndSession }) => {
    const { isListening, messages, startListening, stopListening, speakText } = useVoiceAssistant();
    const bottomRef = useRef(null);

    // Auto-start listening on mount (optional - strictly per user flow, maybe user clicks manual mic)
    // User asked: "jab user boly samne likha aye listening", implies immediate or trigger. 
    // Let's create a prominent mic button to trigger listening for each turn to avoid permissions spam 
    // or implement continuous loop. The hook is single-turn. Let's auto-start for first turn?
    // Or just have the button.

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">

            {/* Header */}
            <header className="p-4 flex justify-between items-center bg-slate-900/50 backdrop-blur-md sticky top-0 z-10 border-b border-slate-800">
                <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                    <span className="font-medium text-slate-300">Live Session</span>
                </div>
                <button
                    onClick={onEndSession}
                    className="flex items-center gap-2 px-4 py-2 text-sm bg-red-500/10 text-red-400 hover:bg-red-500/20 rounded-full transition-colors border border-red-500/20"
                >
                    <X className="w-4 h-4" />
                    End Session
                </button>
            </header>

            {/* Chat Area */}
            <main className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 max-w-4xl mx-auto w-full">
                {messages.length === 0 && (
                    <div className="h-full flex flex-col items-center justify-center text-slate-500 mt-20 opacity-50">
                        <Mic className="w-12 h-12 mb-4" />
                        <p>Tap the microphone to start speaking...</p>
                    </div>
                )}

                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in-up`}
                    >
                        <div className={`max-w-[85%] md:max-w-[70%] text-left`}>
                            <div
                                className={`p-4 rounded-2xl shadow-sm ${msg.role === 'user'
                                        ? 'bg-gradient-to-br from-blue-600 to-blue-700 text-white rounded-tr-none'
                                        : 'bg-slate-800 border border-slate-700 text-slate-100 rounded-tl-none'
                                    }`}
                            >
                                <p className="text-lg leading-relaxed">{msg.text}</p>
                            </div>

                            {/* Actions for Assistant Row */}
                            {msg.role === 'assistant' && (
                                <div className="mt-2 flex gap-2">
                                    <button
                                        onClick={() => speakText(msg.text)}
                                        className="flex items-center gap-2 px-3 py-1.5 bg-slate-800/50 hover:bg-slate-700 rounded-full text-xs text-slate-300 transition-colors border border-slate-700/50"
                                    >
                                        <Volume2 className="w-3 h-3" />
                                        Speak
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                ))}

                {/* State Indicator */}
                {isListening && (
                    <div className="flex justify-start animate-fade-in-up">
                        <div className="bg-slate-800/80 border border-slate-700 p-4 rounded-2xl rounded-tl-none flex items-center gap-3">
                            <div className="flex gap-1 h-3 items-center">
                                <span className="w-1.5 h-3 bg-cyan-400 rounded-full animate-wave-1"></span>
                                <span className="w-1.5 h-5 bg-cyan-400 rounded-full animate-wave-2"></span>
                                <span className="w-1.5 h-3 bg-cyan-400 rounded-full animate-wave-3"></span>
                            </div>
                            <span className="text-cyan-400 font-medium italic">Listening...</span>
                        </div>
                    </div>
                )}

                <div ref={bottomRef} />
            </main>

            {/* Footer / Controls */}
            <footer className="p-6 bg-slate-900/80 backdrop-blur-lg border-t border-slate-800 flex justify-center sticky bottom-0">
                <button
                    onClick={isListening ? stopListening : startListening}
                    className={`
            relative flex items-center justify-center w-16 h-16 rounded-full shadow-2xl transition-all duration-300
            ${isListening
                            ? 'bg-red-500 hover:bg-red-600 scale-110 shadow-red-500/50'
                            : 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:scale-105 shadow-cyan-500/40'}
          `}
                >
                    {isListening ? (
                        <MicOff className="w-8 h-8 text-white animate-pulse" />
                    ) : (
                        <Mic className="w-8 h-8 text-white" />
                    )}

                    {/* Ripple effect when listening */}
                    {isListening && (
                        <span className="absolute w-full h-full rounded-full bg-red-500 opacity-20 animate-ping"></span>
                    )}
                </button>
            </footer>
        </div>
    );
};

export default VoiceInterface;
