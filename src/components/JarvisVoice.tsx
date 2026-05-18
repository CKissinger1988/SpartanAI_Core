import React, { useEffect, useRef, useState } from 'react';
import { Mic, MicOff, MessageSquare, Volume2, ShieldAlert } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

interface JarvisVoiceProps {
  onCommand?: (command: string, args: any) => void;
}

export const JarvisVoice: React.FC<JarvisVoiceProps> = ({ onCommand }) => {
  const [isListening, setIsListening] = useState(false);
  const [messages, setMessages] = useState<{ role: 'user' | 'jarvis', text: string }[]>([]);
  const [error, setError] = useState<string | null>(null);
  
  const wsRef = useRef<WebSocket | null>(null);
  const audioCtxRef = useRef<AudioContext | null>(null);
  const processorRef = useRef<ScriptProcessorNode | null>(null);
  const nextStartTimeRef = useRef<number>(0);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const startJarvis = async () => {
    try {
      setError(null);
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const ws = new WebSocket(`${protocol}//${window.location.host}/ws/jarvis`);
      wsRef.current = ws;

      const audioCtx = new AudioContext({ sampleRate: 16000 });
      audioCtxRef.current = audioCtx;
      nextStartTimeRef.current = 0;

      ws.onopen = async () => {
        setIsListening(true);
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const source = audioCtx.createMediaStreamSource(stream);
        
        // ScriptProcessor is deprecated but easier for raw PCM manipulation in this context
        // for more production apps, AudioWorklets are preferred.
        const processor = audioCtx.createScriptProcessor(4096, 1, 1);
        processorRef.current = processor;
        
        source.connect(processor);
        processor.connect(audioCtx.destination);

        processor.onaudioprocess = (e) => {
          if (ws.readyState === WebSocket.OPEN) {
            const inputData = e.inputBuffer.getChannelData(0);
            const pcmData = float32ToPcm16(inputData);
            const base64 = btoa(String.fromCharCode(...new Uint8Array(pcmData.buffer)));
            ws.send(JSON.stringify({ type: 'audio', data: base64 }));
          }
        };
      };

      ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.type === "audio") {
          playAudioChunk(msg.data);
        } else if (msg.type === "text") {
          setMessages(prev => [...prev.slice(-20), { role: 'jarvis', text: msg.data }]);
        } else if (msg.type === "command") {
          onCommand?.(msg.command, msg.args);
        } else if (msg.type === "interrupted") {
          stopPlayback();
        } else if (msg.type === "error") {
          setError(msg.message);
          stopJarvis();
        }
      };

      ws.onclose = () => {
        setIsListening(false);
        stopJarvis();
      };

      ws.onerror = () => {
        setError("WebSocket connection failed");
        stopJarvis();
      };

    } catch (err: any) {
      setError(err.message || "Failed to start JARVIS");
      setIsListening(false);
    }
  };

  const stopJarvis = () => {
    setIsListening(false);
    wsRef.current?.close();
    processorRef.current?.disconnect();
    audioCtxRef.current?.close();
    wsRef.current = null;
    audioCtxRef.current = null;
    processorRef.current = null;
  };

  const float32ToPcm16 = (buffer: Float32Array) => {
    const l = buffer.length;
    const buf = new Int16Array(l);
    for (let i = 0; i < l; i++) {
        buf[i] = Math.max(-1, Math.min(1, buffer[i])) * 0x7FFF;
    }
    return buf;
  };

  const playAudioChunk = (base64Audio: string) => {
    if (!audioCtxRef.current) return;
    const audioData = Uint8Array.from(atob(base64Audio), c => c.charCodeAt(0)).buffer;
    const pcm16 = new Int16Array(audioData);
    const float32 = new Float32Array(pcm16.length);
    for (let i = 0; i < pcm16.length; i++) {
      float32[i] = pcm16[i] / 0x7FFF;
    }

    const buffer = audioCtxRef.current.createBuffer(1, float32.length, 16000);
    buffer.getChannelData(0).set(float32);

    const source = audioCtxRef.current.createBufferSource();
    source.buffer = buffer;
    source.connect(audioCtxRef.current.destination);

    const startTime = Math.max(audioCtxRef.current.currentTime, nextStartTimeRef.current);
    source.start(startTime);
    nextStartTimeRef.current = startTime + buffer.duration;
  };

  const stopPlayback = () => {
    nextStartTimeRef.current = audioCtxRef.current?.currentTime || 0;
  };

  return (
    <div className="h-full flex flex-col bg-black overflow-hidden rounded-lg border border-cyan-900/20 relative">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(6,182,212,0.05)_0%,_transparent_70%)] pointer-events-none" />
      
      <div className="p-4 border-b border-slate-900 flex justify-between items-center bg-black/40 backdrop-blur-sm z-10">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${isListening ? 'bg-cyan-500 shadow-[0_0_8px_rgba(6,182,212,0.8)]' : 'bg-slate-700'}`} />
          <span className="text-[10px] font-mono tracking-widest text-slate-500 uppercase">System Status: {isListening ? 'Active' : 'Standby'}</span>
        </div>
        <div className="text-[10px] font-mono tracking-widest text-slate-700 uppercase italic">ENGINE: GOOGLE_AI_NEXT_GEN</div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-4 scroll-smooth relative z-10">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center space-y-6">
             <div className="w-32 h-32 rounded-full border-4 border-cyan-500/10 flex items-center justify-center relative">
               <div className={`w-24 h-24 rounded-full border-2 border-cyan-500/20 flex items-center justify-center ${isListening ? 'animate-pulse' : ''}`}>
                  <div className={`w-16 h-16 rounded-full ${isListening ? 'bg-cyan-500 shadow-[0_0_30px_rgba(6,182,212,0.6)]' : 'bg-slate-900 shadow-inner'}`}></div>
               </div>
               {/* Decorative rings */}
               <div className="absolute inset-[-10px] border border-cyan-500/5 rounded-full animate-[spin_10s_linear_infinite]" />
               <div className="absolute inset-[-20px] border border-dashed border-cyan-500/5 rounded-full animate-[spin_15s_linear_infinite_reverse]" />
             </div>
             <p className="text-[10px] font-mono tracking-[0.2em] uppercase text-cyan-500/50">JARVIS_CORE_{isListening ? 'ONLINE // SAY "JARVIS..." ' : 'OFFLINE'}</p>
          </div>
        )}

        <AnimatePresence mode="popLayout">
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[80%] p-3 rounded border ${
                msg.role === 'user' 
                ? 'bg-cyan-500/10 border-cyan-500/30 text-cyan-100' 
                : 'bg-slate-900/60 border-slate-800 text-slate-300 font-mono text-[11px]'
              }`}>
                {msg.role === 'jarvis' && (
                  <div className="text-[9px] text-cyan-500 mb-1 tracking-tighter uppercase font-bold">JARVIS INTERFACE</div>
                )}
                {msg.text}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </div>

      <div className="p-6 bg-black/80 border-t border-slate-900 z-10">
        {error && (
          <div className="mb-4 p-3 bg-red-900/20 border border-red-900/50 rounded flex items-center gap-2 text-red-500 text-[10px] font-mono">
            <ShieldAlert className="w-4 h-4" />
            {error}
          </div>
        )}
        
        <div className="flex items-center justify-between">
          <div className="flex gap-2">
             <div className="flex items-center gap-1.5 h-4">
               {[...Array(12)].map((_, i) => (
                 <motion.div
                   key={i}
                   animate={{
                     height: isListening ? [4, 16, 4] : 4,
                     backgroundColor: isListening ? '#06b6d4' : '#1e293b'
                   }}
                   transition={{
                     repeat: Infinity,
                     duration: 0.8,
                     delay: i * 0.05
                   }}
                   className="w-0.5 rounded-full shadow-[0_0_5px_rgba(6,182,212,0.3)]"
                 />
               ))}
             </div>
          </div>

          <button
            onClick={isListening ? stopJarvis : startJarvis}
            className={`flex items-center gap-2 px-8 py-3 rounded-md font-mono text-[10px] uppercase font-bold tracking-[0.2em] transition-all ${
              isListening 
              ? 'bg-red-500/10 text-red-500 border border-red-500/40 hover:bg-red-500/20' 
              : 'bg-cyan-600/20 text-cyan-400 border border-cyan-500/40 hover:bg-cyan-600/30 glow-cyan'
            }`}
          >
            {isListening ? (
              <>
                <MicOff className="w-4 h-4" />
                ABORT_LINK
              </>
            ) : (
              <>
                <Mic className="w-4 h-4" />
                INITIATE_LINK
              </>
            )}
          </button>

          <div className="flex items-center gap-4 text-slate-600">
            <Volume2 className={`w-4 h-4 ${isListening ? 'text-cyan-500' : ''}`} />
          </div>
        </div>
      </div>
    </div>
  );
};
