import React, { useEffect, useRef } from 'react';
import { Volume2, X } from 'lucide-react';
import useVoiceAssistant from '../hooks/useVoiceAssistant';
import { PromptInputBox } from './ui/ai-prompt-box';
import ShaderBackground from './ui/shader-background';
import { ShiningText } from './ui/shining-text';
import gsap from 'gsap';

const VoiceInterface = ({ onEndSession }) => {
    const { isListening, isThinking, messages, startListening, stopListening, handleUserMessage, speakText } = useVoiceAssistant();
    const bottomRef = useRef(null);
    const chatContainerRef = useRef(null);

    useEffect(() => {
        // Scroll to bottom smoothly
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
        
        // GSAP Animation for new messages
        if (chatContainerRef.current) {
            const newMsgs = chatContainerRef.current.querySelectorAll('.msg-bubble:not(.gsap-animated)');
            if (newMsgs.length > 0) {
                gsap.fromTo(newMsgs, 
                    { opacity: 0, y: 20 },
                    { 
                        opacity: 1, 
                        y: 0, 
                        duration: 0.4, 
                        stagger: 0.1, 
                        ease: "power2.out", 
                        onComplete: function() { 
                            this.targets().forEach(t => t.classList.add('gsap-animated', 'opacity-100')); 
                        } 
                    }
                );
            }
        }
    }, [messages]);

    const handleSend = (text, files) => {
        // Simple text processing here, files are ignored in this logic as per previous implementation
        if (text.trim() || files?.length) {
            handleUserMessage(text || "[File attached]", false);
        }
    };

    return (
        <div className="relative h-[100dvh] bg-[#050505] text-slate-100 flex flex-col font-sans overflow-hidden">
            {/* Background */}
            <div className="absolute inset-0 z-0">
                <ShaderBackground />
                <div className="absolute inset-0 bg-black/60 backdrop-blur-[2px]" />
            </div>

            {/* Header */}
            <header className="p-4 flex justify-between items-center bg-black/20 backdrop-blur-md z-20 border-b border-white/10 shrink-0">
                <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                    <span className="font-medium text-slate-300 tracking-wide text-sm uppercase">Live Session</span>
                </div>
                <button
                    onClick={onEndSession}
                    className="flex items-center gap-2 px-4 py-2 text-sm bg-red-500/10 text-red-400 hover:bg-red-500/20 rounded-full transition-colors border border-red-500/20 shadow-[0_0_15px_rgba(239,68,68,0.15)]"
                >
                    <X className="w-4 h-4" />
                    End Session
                </button>
            </header>

            {/* Chat Area */}
            <main ref={chatContainerRef} className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 max-w-4xl mx-auto w-full z-10 [&::-webkit-scrollbar]:hidden [-ms-overflow-style:'none'] [scrollbar-width:none]">
                {messages.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-full min-h-[60vh] opacity-90">
                        <h1 className="text-4xl md:text-5xl font-medium tracking-tight text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-400 drop-shadow-md">
                            How can I help today?
                        </h1>
                    </div>
                )}

                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`msg-bubble flex opacity-0 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div className={`max-w-[85%] md:max-w-[70%] text-left`}>
                            <div
                                className={`p-4 md:p-5 rounded-3xl shadow-lg backdrop-blur-md border ${msg.role === 'user'
                                        ? 'bg-white/10 border-white/20 text-white rounded-tr-sm'
                                        : 'bg-[#1F2023]/80 border-[#333333] text-gray-200 rounded-tl-sm'
                                    }`}
                            >
                                <p className="text-[15px] md:text-base leading-relaxed tracking-wide font-light">{msg.text}</p>
                            </div>

                            {/* Actions for Assistant Row */}
                            {msg.role === 'assistant' && (
                                <div className="mt-2.5 flex gap-2 ml-1">
                                    <button
                                        onClick={() => speakText(msg.text)}
                                        className="flex items-center gap-1.5 px-3 py-1.5 bg-[#1F2023]/60 hover:bg-[#2E3033] rounded-full text-xs text-gray-400 hover:text-white transition-all duration-300 border border-[#333333]"
                                    >
                                        <Volume2 className="w-3.5 h-3.5" />
                                        Listen
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                ))}

                {/* State Indicator */}
                {isListening && (
                    <div className="msg-bubble flex justify-start opacity-0">
                        <div className="bg-[#1F2023]/80 border border-[#333333] p-4 md:p-5 rounded-3xl rounded-tl-sm flex items-center gap-4 shadow-lg backdrop-blur-md">
                            <div className="flex gap-1.5 h-4 items-center">
                                <span className="w-1.5 h-3 bg-white rounded-full animate-[bounce_1s_infinite_0ms]"></span>
                                <span className="w-1.5 h-5 bg-white rounded-full animate-[bounce_1s_infinite_200ms]"></span>
                                <span className="w-1.5 h-3 bg-white rounded-full animate-[bounce_1s_infinite_400ms]"></span>
                            </div>
                            <span className="text-white/90 font-medium text-sm tracking-wider uppercase">Listening...</span>
                        </div>
                    </div>
                )}

                {/* Thinking Indicator */}
                {isThinking && !isListening && (
                    <div className="msg-bubble flex justify-start opacity-0">
                        <div className="bg-[#1F2023]/80 border border-[#333333] p-4 md:p-5 rounded-3xl rounded-tl-sm shadow-lg backdrop-blur-md">
                            <ShiningText text="AI is thinking..." />
                        </div>
                    </div>
                )}

                <div ref={bottomRef} className="h-4 shrink-0" />
            </main>

            {/* Footer / Controls */}
            <footer className="p-4 md:p-6 bg-gradient-to-t from-[#050505] via-[#050505]/90 to-transparent z-20 flex justify-center shrink-0">
                <div className="w-full max-w-4xl px-2">
                    <PromptInputBox 
                        onSend={handleSend}
                        isRecordingExt={isListening}
                        onStartRecord={startListening}
                        onStopRecord={stopListening}
                        placeholder="Type a message or use the mic..."
                    />
                </div>
            </footer>
        </div>
    );
};

export default VoiceInterface;
