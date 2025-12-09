import React, { useState, useRef, useEffect } from 'react';
import clsx from 'clsx';
import './Chatbot.css';

interface Message {
    role: 'user' | 'bot';
    text: string;
    context?: any[];
}

export default function Chatbot() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([
        { role: 'bot', text: 'Hi! I am the AI Native assistant. Ask me anything about the book.' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isOpen]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMsg = input;
        setInput('');
        setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
        setIsLoading(true);

        try {
            // TODO: Replace with your production backend URL
            const response = await fetch('https://your-production-backend-url/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: userMsg }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            setMessages(prev => [...prev, { role: 'bot', text: data.answer, context: data.context }]);
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, { role: 'bot', text: 'Sorry, I encountered an error. Please ensure the backend is running.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className={clsx('chatbot-widget', { 'chatbot-open': isOpen })}>
            {!isOpen && (
                <button className="chatbot-toggle" onClick={() => setIsOpen(true)}>
                    💬 Ask AI
                </button>
            )}

            {isOpen && (
                <div className="chatbot-window glass-panel">
                    <div className="chatbot-header">
                        <h3>AI Assistant</h3>
                        <button className="chatbot-close" onClick={() => setIsOpen(false)}>×</button>
                    </div>
                    <div className="chatbot-messages">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={clsx('message', `message-${msg.role}`)}>
                                <div className="message-content">{msg.text}</div>
                            </div>
                        ))}
                        {isLoading && <div className="message message-bot"><div className="typing-indicator">...</div></div>}
                        <div ref={messagesEndRef} />
                    </div>
                    <form className="chatbot-input-form" onSubmit={handleSubmit}>
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Ask a question..."
                            className="chatbot-input"
                        />
                        <button type="submit" className="chatbot-send" disabled={isLoading}>
                            ➤
                        </button>
                    </form>
                </div>
            )}
        </div>
    );
}
