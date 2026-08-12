"use client";

import { useEffect, useState } from "react";

export default function SplashAnimation() {
  const [show, setShow] = useState(true);
  const [fade, setFade] = useState(false);

  useEffect(() => {
    // Check if we've already shown the splash in this session
    const hasSeenSplash = sessionStorage.getItem("hasSeenSplash");
    if (hasSeenSplash) {
      setShow(false);
      return;
    }

    // Trigger the fade-out after 2.5 seconds
    const fadeTimer = setTimeout(() => {
      setFade(true);
    }, 2500);

    // Completely unmount after 3.2 seconds
    const hideTimer = setTimeout(() => {
      setShow(false);
      sessionStorage.setItem("hasSeenSplash", "true");
    }, 3200);

    return () => {
      clearTimeout(fadeTimer);
      clearTimeout(hideTimer);
    };
  }, []);

  if (!show) return null;

  return (
    <div 
      className={`fixed inset-0 z-50 flex items-center justify-center bg-black transition-opacity duration-700 ease-in-out ${fade ? 'opacity-0 pointer-events-none' : 'opacity-100'}`}
    >
      {/* Background Animated Stock Line Chart */}
      <div className="absolute inset-0 overflow-hidden opacity-30 pointer-events-none flex items-center justify-center">
        <svg 
          viewBox="0 0 1000 300" 
          preserveAspectRatio="none" 
          className="w-[150%] h-[150%] absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-[pulse_2s_ease-in-out_infinite]"
        >
          <path 
            d="M 0,200 L 100,180 L 200,220 L 300,100 L 400,150 L 500,50 L 600,80 L 700,20 L 800,90 L 900,10 L 1000,50" 
            fill="none" 
            stroke="url(#gradient)" 
            strokeWidth="3" 
            className="animate-[dash_3s_linear_forwards]"
            strokeDasharray="2500"
            strokeDashoffset="2500"
          />
          <defs>
            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#10B981" stopOpacity="0" />
              <stop offset="50%" stopColor="#10B981" />
              <stop offset="100%" stopColor="#10B981" stopOpacity="0" />
            </linearGradient>
          </defs>
        </svg>
      </div>

      {/* Netflix-style Logo Animation */}
      <div className="relative z-10 flex flex-col items-center justify-center pointer-events-none">
        <img 
          src="/logo.png" 
          alt="ASHEN-VECTOR" 
          className="w-48 h-48 animate-[netflix_1.5s_cubic-bezier(0.19,1,0.22,1)_forwards] opacity-0 drop-shadow-[0_0_30px_rgba(16,185,129,0.5)]"
        />
        <div className="mt-8 text-2xl font-mono font-bold tracking-[0.5em] text-white opacity-0 animate-[fadein_1s_ease-out_0.5s_forwards]">
          ASHEN<span className="text-[#10B981]">VECTOR</span>
        </div>
      </div>
    </div>
  );
}
