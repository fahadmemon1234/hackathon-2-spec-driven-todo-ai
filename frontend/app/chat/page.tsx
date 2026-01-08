'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

// Import the ChatMessage type
import { ChatMessage } from '@/types/chat';

// Import the API client
import { api } from '@/lib/api';

interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls?: Array<{
    name: string;
    arguments: Record<string, any>;
  }>;
}

const ChatPage = () => {
  const { user, loading } = useAuth();
  const router = useRouter();
  const [inputMessage, setInputMessage] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);

  // Check authentication
  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  // Load existing conversation if conversationId is in URL
  useEffect(() => {
    if (user && typeof window !== 'undefined') {
      const urlParams = new URLSearchParams(window.location.search);
      const convId = urlParams.get('conversationId');
      if (convId) {
        setConversationId(parseInt(convId, 10));
        // In a real implementation, you would load the conversation history here
        // Example: loadConversationHistory(parseInt(convId, 10));
      }
    }
  }, [user]);

  // Function to load conversation history (to be implemented)
  const loadConversationHistory = async (conversationId: number) => {
    try {
      const token = await api.getJwtToken();
      if (!token) {
        throw new Error('No authentication token available');
      }

      // In a real implementation, you would fetch the conversation history
      // const response = await fetch(`/api/conversations/${conversationId}/messages`, {
      //   headers: {
      //     'Authorization': `Bearer ${token}`,
      //   },
      // });
      //
      // if (!response.ok) {
      //   throw new Error(`Failed to load conversation: ${response.statusText}`);
      // }
      //
      // const messagesData = await response.json();
      // setMessages(messagesData.map((msg: any) => ({
      //   id: msg.id,
      //   role: msg.role,
      //   content: msg.content,
      //   createdAt: msg.created_at,
      // })));
    } catch (error) {
      console.error('Error loading conversation history:', error);
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !user?.id || isLoading) return;

    try {
      setIsLoading(true);

      // Add user message to UI immediately
      const userMessage: ChatMessage = {
        id: Date.now(),
        role: 'user',
        content: inputMessage,
        createdAt: new Date().toISOString(),
      };
      
      setMessages(prev => [...prev, userMessage]);
      const messageToSend = inputMessage;
      setInputMessage('');

      // Call the backend chat API using the api client
      const token = await api.getJwtToken();
      if (!token) {
        throw new Error('No authentication token available');
      }

      const response = await fetch(`/api/${user.id}/chat`, {
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

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Unauthorized: Please log in again');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();

      // Update conversation ID if it's the first message
      if (!conversationId) {
        setConversationId(data.conversation_id);
      }

      // Add assistant message to UI
      const assistantMessage: ChatMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response,
        createdAt: new Date().toISOString(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message to UI
      const errorMessage: ChatMessage = {
        id: Date.now(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        createdAt: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-800 dark:text-white">AI Task Assistant</h1>
            <p className="text-gray-600 dark:text-gray-300">
              Chat with your AI assistant to manage tasks naturally
            </p>
          </div>

          {/* Chat messages container */}
          <div className="mb-6 h-[60vh] overflow-y-auto pr-2">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-4">
                <div className="bg-gray-200 dark:bg-gray-700 border-2 border-dashed rounded-xl w-16 h-16 flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                  </svg>
                </div>
                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-1">No messages yet</h3>
                <p className="text-gray-500 dark:text-gray-400">
                  Send a message to start chatting with your AI assistant
                </p>
                <p className="text-sm text-gray-400 dark:text-gray-500 mt-4">
                  Try: "Add a task to buy groceries" or "Show my pending tasks"
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {messages.map((message: ChatMessage) => (
                  <div
                    key={message.id}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg px-4 py-2 ${
                        message.role === 'user'
                          ? 'bg-blue-500 text-white rounded-br-none'
                          : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-bl-none'
                      }`}
                    >
                      <div className="whitespace-pre-wrap">{message.content}</div>
                      <div className={`text-xs mt-1 ${message.role === 'user' ? 'text-blue-200' : 'text-gray-500 dark:text-gray-400'}`}>
                        {new Date(message.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Input area */}
          <div className="flex gap-2">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message here..."
              className="flex-1 border border-gray-300 dark:border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white resize-none"
              rows={2}
              disabled={isLoading}
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading || !inputMessage.trim()}
              className="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Sending...
                </span>
              ) : (
                'Send'
              )}
            </button>
          </div>

          {/* Conversation ID display */}
          {conversationId && (
            <div className="mt-4 text-sm text-gray-500 dark:text-gray-400">
              Conversation ID: {conversationId}
              <button 
                onClick={() => navigator.clipboard.writeText(conversationId.toString())}
                className="ml-2 text-blue-500 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300"
              >
                Copy
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatPage;