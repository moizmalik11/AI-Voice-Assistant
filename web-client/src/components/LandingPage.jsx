import React, { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { TextPlugin } from 'gsap/TextPlugin';
import { Mic, ArrowRight } from 'lucide-react';
import ShaderBackground from '@/components/ui/shader-background';
import apiService from '@/services/api';

gsap.registerPlugin(TextPlugin);

const LandingPage = ({ onStart }) => {
    const line1Ref = useRef(null);
    const line2Ref = useRef(null);
    const containerRef = useRef(null);
    const buttonRef = useRef(null);
    const micRef = useRef(null);

    useEffect(() => {
        // Fast fade in for the main container
        gsap.to(containerRef.current, { opacity: 1, duration: 0.3 });

        // Coordinated animation timeline
        const tl = gsap.timeline();

        // 1. Show Mic and Button quickly
        tl.fromTo([micRef.current, buttonRef.current], 
            { opacity: 0, y: 20 },
            { opacity: 1, y: 0, duration: 0.7, stagger: 0.1, ease: 'power3.out' }
        );

        // 2. Swipe reveal animation for text lines
        tl.fromTo([line1Ref.current, line2Ref.current],
            { y: 60, opacity: 0 },
            { y: 0, opacity: 1, duration: 0.8, stagger: 0.15, ease: 'power4.out' },
            "-=0.5" // Start slightly before mic/button finish
        );

        // Pre-warm the AI API so it's ready when user clicks start
        apiService.warmup();
    }, []);

    return (
        <div className="min-h-screen relative overflow-hidden flex flex-col items-center justify-center font-sans">
            <ShaderBackground />
            
            <div ref={containerRef} className="relative z-10 flex flex-col items-center text-center p-8 max-w-2xl opacity-0">
                <div ref={micRef} className="mb-8 p-5 rounded-[2rem] bg-white/5 backdrop-blur-xl border border-white/10 shadow-[0_8px_32px_rgba(0,0,0,0.3)] group hover:scale-105 transition-transform duration-500 opacity-0">
                    <Mic className="w-12 h-12 text-white/70 group-hover:text-white transition-colors" />
                </div>
                
                {/* Text: Modern font, no bold, Swipe reveal style */}
                <div className="text-4xl md:text-5xl font-light text-white/90 tracking-wide mb-12 flex flex-col gap-2">
                    <div className="overflow-hidden pt-2">
                        <div ref={line1Ref} className="opacity-0">Your AI Voice assistant</div>
                    </div>
                    <div className="overflow-hidden pb-2">
                        <div ref={line2Ref} className="opacity-0">is here_</div>
                    </div>
                </div>
                
                <button
                    ref={buttonRef}
                    onClick={onStart}
                    className="group relative px-10 py-4 bg-white/5 hover:bg-white/10 backdrop-blur-2xl border border-white/20 hover:border-white/40 rounded-full text-lg font-light text-white tracking-wide transition-all duration-500 flex items-center gap-4 overflow-hidden opacity-0 shadow-[0_0_40px_rgba(255,255,255,0.05)] hover:shadow-[0_0_60px_rgba(255,255,255,0.15)]"
                >
                    <span className="relative z-10">Initialize Session</span>
                    <ArrowRight className="w-5 h-5 relative z-10 group-hover:translate-x-2 transition-transform duration-300" />
                    
                    {/* Subtle glow effect inside button */}
                    <div className="absolute inset-0 bg-gradient-to-r from-white/10 via-transparent to-gray-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                </button>
            </div>
            
            {/* Ambient overlay to ensure text is readable over the shader */}
            <div className="absolute inset-0 bg-black/20 pointer-events-none z-0" />
        </div>
    );
};

export default LandingPage;
