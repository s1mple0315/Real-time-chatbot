import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]); 
  const [input, setInput] = useState(''); 
  const [ws, setWs] = useState(null); 

  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:8000/ws');

    websocket.onopen = () => {
      console.log('WebSocket connected');
    };

    websocket.onmessage = (event) => {
      setMessages((prevMessages) => [...prevMessages, event.data]);
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    websocket.onclose = () => {
      console.log('WebSocket disconnected');
    };

    setWs(websocket);

    return () => {
      websocket.close();
    };
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (ws && input.trim()) {
      ws.send(input); 
      setInput(''); 
    }
  };

  return (
    <div className="App">
      <h1>Real-Time Chatbot</h1>
      <div className="messages">
        {messages.map((msg, index) => (
          <p key={index}>{msg}</p>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit" disabled={!ws || ws.readyState !== WebSocket.OPEN}>
          Send
        </button>
      </form>
    </div>
  );
}

export default App;