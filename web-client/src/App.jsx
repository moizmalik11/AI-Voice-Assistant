import React, { useState } from 'react';
import LandingPage from './components/LandingPage';
import VoiceInterface from './components/VoiceInterface';

function App() {
  const [isSessionActive, setIsSessionActive] = useState(false);

  return (
    <div className="antialiased text-slate-900 dark:text-slate-100">
      {isSessionActive ? (
        <VoiceInterface onEndSession={() => setIsSessionActive(false)} />
      ) : (
        <LandingPage onStart={() => setIsSessionActive(true)} />
      )}
    </div>
  );
}

export default App;
