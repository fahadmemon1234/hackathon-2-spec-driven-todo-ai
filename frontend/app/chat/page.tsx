'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { ChatMessage } from '@/types/chat';
import { api } from '@/lib/api';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, 
  Bot, 
  User, 
  Copy, 
  Loader2, 
  Sparkles, 
  ArrowLeft, 
  RefreshCcw,
  Trash2
} from 'lucide-react';

interface ChatResponse {
  conversation_id: number;
  response: string;
}

const ChatPage = () => {
  const { user, loading } = useAuth();
  const router = useRouter();
  const [inputMessage, setInputMessage] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    if (!loading && !user) router.push('/login');
  }, [user, loading, router]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !user?.id || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now(),
      role: 'user',
      content: inputMessage,
      createdAt: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    const messageToSend = inputMessage;
    setInputMessage('');
    setIsLoading(true);

    try {
      const token = await api.getJwtToken();
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/${user.id}/chat`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conversation_id: conversationId || undefined,
          message: messageToSend,
        }),
      });

      if (!response.ok) throw new Error('Failed to fetch');

      const data: ChatResponse = await response.json();
      if (!conversationId) setConversationId(data.conversation_id);

      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response,
        createdAt: new Date().toISOString(),
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        id: Date.now(),
        role: 'assistant',
        content: '⚠️ Error: Connection lost. Please try again.',
        createdAt: new Date().toISOString(),
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setConversationId(null);
  };

  return (
    <div className="flex h-screen bg-[#F8FAFC] dark:bg-[#0F172A] overflow-hidden font-sans text-gray-900 dark:text-slate-200">
      
      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col relative">
        
        {/* Header - Refined & Premium */}
        <header className="h-16 border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-[#1E293B]/80 backdrop-blur-md flex items-center justify-between px-4 md:px-8 z-20">
          <div className="flex items-center gap-4">
            {/* Back Button */}
            <button 
              onClick={() => router.push('/tasks')}
              className="group p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-xl transition-all duration-200"
              title="Back to Dashboard"
            >
              <ArrowLeft className="w-5 h-5 text-gray-500 group-hover:text-blue-600 transition-colors" />
            </button>

            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-blue-500 to-indigo-600 p-2 rounded-xl shadow-lg shadow-blue-500/20">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="hidden sm:block">
                <h1 className="text-sm font-bold text-gray-900 dark:text-white leading-none">Task AI</h1>
                <span className="text-[10px] text-green-500 font-semibold flex items-center gap-1 mt-1 uppercase tracking-wider">
                  <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse" /> Live System
                </span>
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            {messages.length > 0 && (
              <button 
                onClick={clearChat}
                className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/20 rounded-lg transition-all"
                title="Clear Chat"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            )}
            
            {conversationId && (
              <div className="flex items-center gap-2 px-3 py-1.5 bg-gray-100 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-full">
                <span className="text-[10px] font-mono text-gray-500">ID: {conversationId}</span>
                <button 
                  onClick={() => navigator.clipboard.writeText(conversationId.toString())}
                  className="hover:scale-110 transition-transform"
                >
                  <Copy className="w-3 h-3 text-gray-400 hover:text-blue-500" />
                </button>
              </div>
            )}
          </div>
        </header>

        {/* Messages List */}
        <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 scroll-smooth custom-scrollbar">
          {messages.length === 0 ? (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="h-full flex flex-col items-center justify-center text-center max-w-lg mx-auto"
            >
              <div className="relative mb-6">
                <div className="absolute inset-0 bg-blue-500 blur-3xl opacity-10 rounded-full"></div>
                <div className="relative w-20 h-20 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-3xl flex items-center justify-center shadow-2xl">
                  <Sparkles className="w-10 h-10 text-blue-600" />
                </div>
              </div>
              <h2 className="text-2xl font-extrabold text-gray-900 dark:text-white tracking-tight">Intelligence at your service</h2>
              <p className="text-gray-500 dark:text-gray-400 mt-3 text-sm leading-relaxed">
                I can help you streamline your workflow, manage complex tasks, and organize your day with simple natural language.
              </p>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-10 w-full">
                {['Create a task', 'List my tasks', 'Schedule a meeting', 'Delete completed'].map((suggestion) => (
                  <button 
                    key={suggestion}
                    onClick={() => setInputMessage(suggestion)}
                    className="group p-4 text-left text-sm bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-2xl hover:border-blue-500 dark:hover:border-blue-500 transition-all duration-200 hover:shadow-md hover:-translate-y-0.5"
                  >
                    <span className="text-gray-400 group-hover:text-blue-500 transition-colors mr-2">✦</span>
                    <span className="text-gray-700 dark:text-gray-300 font-medium">"{suggestion}"</span>
                  </button>
                ))}
              </div>
            </motion.div>
          ) : (
            <div className="max-w-4xl mx-auto w-full space-y-6">
              <AnimatePresence initial={false}>
                {messages.map((message) => (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    key={message.id}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`flex gap-4 max-w-[85%] ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                      <div className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 shadow-sm ${
                        message.role === 'user' 
                          ? 'bg-blue-600' 
                          : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700'
                      }`}>
                        {message.role === 'user' ? <User className="w-5 h-5 text-white" /> : <Bot className="w-5 h-5 text-blue-600" />}
                      </div>
                      
                      <div className={`relative p-4 rounded-2xl shadow-sm ${
                        message.role === 'user' 
                          ? 'bg-blue-600 text-white rounded-tr-none' 
                          : 'bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 rounded-tl-none border border-gray-100 dark:border-gray-700'
                      }`}>
                        <p className="text-[15px] leading-relaxed whitespace-pre-wrap">{message.content}</p>
                        <div className={`text-[10px] mt-2 font-medium opacity-50 ${message.role === 'user' ? 'text-right' : 'text-left'}`}>
                          {new Date(message.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          )}
          
          {isLoading && (
            <div className="max-w-4xl mx-auto w-full flex justify-start items-center gap-4">
              <div className="w-9 h-9 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 flex items-center justify-center">
                <RefreshCcw className="w-5 h-5 text-blue-600 animate-spin" />
              </div>
              <div className="px-5 py-4 bg-white dark:bg-gray-800 rounded-2xl rounded-tl-none border border-gray-100 dark:border-gray-700 shadow-sm">
                <span className="flex gap-1.5">
                  <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                  <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                  <span className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></span>
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Input Area - Floating Style */}
        <div className="px-4 pb-6 pt-2 bg-transparent">
          <div className="max-w-4xl mx-auto relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-600/20 to-indigo-600/20 rounded-[22px] blur-lg opacity-0 group-focus-within:opacity-100 transition duration-500"></div>
            
            <div className="relative flex items-end gap-3 bg-white dark:bg-[#1E293B] border border-gray-200 dark:border-gray-700 rounded-3xl p-3 shadow-2xl focus-within:border-blue-500/50 transition-all">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSendMessage())}
                placeholder="Type your command..."
                rows={1}
                className="flex-1 bg-transparent border-none focus:ring-0 text-gray-800 dark:text-gray-100 py-3 px-4 resize-none max-h-48 text-[15px] placeholder:text-gray-400"
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading || !inputMessage.trim()}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 dark:disabled:bg-gray-800 text-white w-12 h-12 rounded-2xl disabled:opacity-50 transition-all flex items-center justify-center shrink-0 shadow-lg shadow-blue-500/20 active:scale-95"
              >
                {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5 fill-current" />}
              </button>
            </div>
          </div>
          <p className="text-center text-[10px] text-gray-400 mt-4 font-medium uppercase tracking-widest opacity-70">
            Shift + Enter for new line • AI Assistant v2.0
          </p>
        </div>
      </main>

      {/* Global CSS for scrollbar (Aap layout.tsx ya global.css mein bhi daal sakte hain) */}
      <style jsx global>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 5px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(156, 163, 175, 0.2);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(156, 163, 175, 0.4);
        }
      `}</style>
    </div>
  );
};

export default ChatPage;