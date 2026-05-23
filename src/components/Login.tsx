import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Shield, Lock, ArrowRight, User, AlertCircle, Loader2 } from 'lucide-react';
import { motion } from 'motion/react';

export const Login: React.FC = () => {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('nexus2024');
  const [error, setError] = useState<string | null>(null);
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);

  useEffect(() => {
    const savedEmail = localStorage.getItem('nexus_operator_id');
    const savedRemember = localStorage.getItem('nexus_remember_me') === 'true';
    if (savedRemember && savedEmail) {
      setEmail(savedEmail);
      setRememberMe(true);
    } else if (!savedEmail) {
      setEmail('operator@nexusai.io');
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoggingIn(true);

    try {
      await login(email, password);
      if (rememberMe) {
        localStorage.setItem('nexus_operator_id', email);
        localStorage.setItem('nexus_remember_me', 'true');
      } else {
        localStorage.removeItem('nexus_operator_id');
        localStorage.setItem('nexus_remember_me', 'false');
      }
    } catch (err: any) {
      setError(err.message || 'Authentication failed. Access denied.');
    } finally {
      setIsLoggingIn(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#02040a] p-6 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(6,182,212,0.05)_0%,_transparent_70%)]" />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/5 rounded-full blur-[100px]" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-emerald-500/5 rounded-full blur-[100px]" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full relative"
      >
        <div className="bg-slate-900/40 border border-slate-800 rounded-2xl backdrop-blur-xl p-10 shadow-2xl relative">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 p-4 bg-slate-900 border border-slate-800 rounded-2xl shadow-xl">
            <Shield className="w-10 h-10 text-cyan-500" />
          </div>

          <div className="text-center mt-6 mb-10 space-y-2">
            <h1 className="text-3xl font-black tracking-tighter text-white italic">NEXUS<span className="text-cyan-500">_CORE</span></h1>
            <p className="text-[10px] font-mono text-slate-500 uppercase tracking-widest">Enterprise Security Intelligence Suite</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-4">
              <div className="space-y-1.5">
                <div className="h-12 w-full bg-black/40 border border-slate-800 rounded-lg flex items-center px-4 gap-3 text-slate-400 group focus-within:border-cyan-500/50 transition-all">
                  <User className="w-4 h-4 text-cyan-500/50" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="OPERATOR_ID (Email)"
                    className="bg-transparent border-none outline-none flex-1 text-xs font-mono text-cyan-100 placeholder:text-slate-600"
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <div className="h-12 w-full bg-black/40 border border-slate-800 rounded-lg flex items-center px-4 gap-3 text-slate-400 group focus-within:border-cyan-500/50 transition-all">
                  <Lock className="w-4 h-4 text-cyan-500/50" />
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="ACCESS_TOKEN (Password)"
                    className="bg-transparent border-none outline-none flex-1 text-xs font-mono text-cyan-100 placeholder:text-slate-600"
                  />
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between px-1">
              <div
                className="flex items-center gap-2 cursor-pointer group"
                onClick={() => setRememberMe(!rememberMe)}
              >
                <div className={`w-3.5 h-3.5 rounded border transition-all flex items-center justify-center ${rememberMe ? 'bg-cyan-500 border-cyan-500' : 'border-slate-700 group-hover:border-slate-500'
                  }`}>
                  {rememberMe && (
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className="w-1.5 h-1.5 bg-black rounded-sm"
                    />
                  )}
                </div>
                <span className="text-[10px] font-mono text-slate-500 uppercase tracking-tighter">Remember Operator ID</span>
              </div>
              <span className="text-[9px] font-mono text-cyan-500/50 uppercase cursor-pointer hover:text-cyan-500 transition-colors">Forgot Token?</span>
            </div>

            {error && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                className="p-3 bg-red-900/20 border border-red-500/30 rounded-lg flex items-center gap-3 text-red-500 text-[10px] font-mono uppercase"
              >
                <AlertCircle className="w-4 h-4 shrink-0" />
                {error}
              </motion.div>
            )}

            <button
              type="submit"
              disabled={isLoggingIn}
              className="w-full h-12 bg-cyan-600 hover:bg-cyan-500 text-white font-bold rounded-lg transition-all flex items-center justify-center gap-3 group relative overflow-hidden disabled:opacity-50"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
              {isLoggingIn ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <>
                  <span>INITIALIZE SECURE ACCESS</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </button>
          </form>

          <p className="text-[9px] text-center text-slate-600 font-mono uppercase leading-relaxed">
            By accessing this interface, you agree to the <br />
            <span className="text-cyan-500/50 underline cursor-pointer">Protocol Mastery & Data Sovereignty terms.</span>
          </p>
        </div>

        <div className="mt-10 pt-10 border-t border-slate-800/50 flex justify-between items-center text-[8px] font-mono text-slate-700">
          <span>VERSION: 2.5.0-STABLE</span>
          <span>BUILD: 2024.11.18</span>
        </div>

        {/* Decorative corner accents */}
        <div className="absolute -top-2 -left-2 w-8 h-8 border-t-2 border-l-2 border-cyan-500/20 rounded-tl-xl" />
        <div className="absolute -bottom-2 -right-2 w-8 h-8 border-b-2 border-r-2 border-cyan-500/20 rounded-br-xl" />
      </motion.div >
      );
};
