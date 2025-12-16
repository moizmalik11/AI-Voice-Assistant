import React from 'react';
import { Mic } from 'lucide-react';

const LandingPage = ({ onStart }) => {
    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-black flex flex-col items-center justify-center text-white p-4">
            <div className="bg-white/5 backdrop-blur-xl p-10 rounded-3xl shadow-2xl border border-white/10 text-center max-w-lg w-full transform transition-all hover:scale-105 duration-500">
                <div className="mb-8 flex justify-center">
                    <div className="p-4 bg-cyan-500/20 rounded-full animate-pulse-slow">
                        <Mic className="w-16 h-16 text-cyan-400" />
                    </div>
                </div>

                <h1 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-purple-500 mb-6 pb-2">
                    Your AI Voice Assistant
                </h1>

                <p className="text-slate-400 mb-10 text-lg">
                    Experience the future of conversation. Click below to start talking.
                </p>

                <button
                    onClick={onStart}
                    className="group relative px-8 py-4 bg-gradient-to-r from-cyan-600 to-blue-600 rounded-full text-lg font-semibold shadow-lg shadow-cyan-500/30 hover:shadow-cyan-500/50 hover:scale-105 transition-all duration-300 w-full"
                >
                    <span className="relative z-10 flex items-center justify-center gap-2">
                        Get Started
                        <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                        </svg>
                    </span>
                </button>
            </div>
        </div>
    );
};

export default LandingPage;
