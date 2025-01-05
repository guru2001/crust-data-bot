import React, { useState } from "react";
import ReactMarkdown from "react-markdown";

function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! How can I assist you today?" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("https://bitter-glynda-guru22-fabbb125.koyeb.app/apidocs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input }),
      });
      const data = await response.json();

      const botMessage = { sender: "bot", text: data.message };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Error: Could not reach the server." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1>Crust Data Chatbot</h1>
      <div
        style={{
          width: "400px",
          height: "500px",
          border: "1px solid #ccc",
          borderRadius: "8px",
          overflowY: "auto",
          padding: "10px",
          display: "flex",
          flexDirection: "column",
          backgroundColor: "#f9f9f9",
        }}
      >
        {messages.map((message, index) => (
          <div
            key={index}
            style={{
              alignSelf: message.sender === "bot" ? "flex-start" : "flex-end",
              backgroundColor:
                message.sender === "bot" ? "#e1f5fe" : "#c8e6c9",
              color: "#333",
              padding: "8px 12px",
              borderRadius: "16px",
              margin: "5px 0",
              maxWidth: "75%", // Limits the width of the bubble
              wordWrap: "break-word", // Ensures words wrap within the bubble
              overflowWrap: "break-word", // Handles long strings or URLs
            }}
          >
            <ReactMarkdown>{message.text}</ReactMarkdown>
          </div>
        ))}
      </div>
      <div style={{ marginTop: "10px", display: "flex", gap: "10px" }}>
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          placeholder="Type your message"
          style={{
            padding: "10px",
            width: "300px",
            border: "1px solid #ccc",
            borderRadius: "8px",
          }}
        />
        <button
          onClick={handleSendMessage}
          style={{
            padding: "10px 15px",
            backgroundColor: loading ? "#c8c8c8" : "#4caf50",
            color: "#fff",
            border: "none",
            borderRadius: "8px",
            cursor: loading ? "not-allowed" : "pointer",
          }}
          disabled={loading}
        >
          {loading ? "Loading..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;
