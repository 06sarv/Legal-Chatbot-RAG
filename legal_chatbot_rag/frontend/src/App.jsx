import { useState } from "react";
import ChatInput from "./ChatInput";
import ChatBubble from "./ChatBubble";

function App() {
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (message) => {
    if (!message.trim()) return;

    const userMessage = { role: "user", message: escapeHtml(message) };
    setChatHistory((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const res = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message })
      });

      const data = await res.json();
      const raw = data?.response || "Sorry, I didn’t get that.";

      const formattedResponse = formatBotResponse(raw);
      const botMessage = { role: "assistant", message: formattedResponse };

      setChatHistory((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error("Error fetching:", err);
      const errorMessage = {
        role: "assistant",
        message: `<p>⚠️ Something went wrong. Please try again later.</p>`
      };
      setChatHistory((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const formatBotResponse = (text) => {
    if (!text) return "<p>No response received.</p>";

    // Simple formatting: bold and new lines
    let formatted = text
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .split("\n")
      .map((line) => `<p>${line.trim()}</p>`)
      .join("");

    return formatted;
  };

  const escapeHtml = (unsafe) => {
    return unsafe
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-3xl mx-auto bg-white shadow-xl rounded-xl p-6 flex flex-col h-[90vh]">
        <h1 className="text-2xl font-bold mb-4 text-center">⚖️ Legal Chatbot</h1>
        <div className="flex-1 overflow-y-auto space-y-3 mb-4 px-2">
          {chatHistory.map((msg, index) => (
            <ChatBubble key={index} role={msg.role} message={msg.message} />
          ))}
          {loading && (
            <ChatBubble role="assistant" message={`<p>Typing...</p>`} />
          )}
        </div>
        <ChatInput onSend={sendMessage} />
      </div>
    </div>
  );
}

export default App;
