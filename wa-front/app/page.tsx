"use client";
import { useState } from "react";

export default function Home() {
  const [message, setMessage] = useState<string>("");
  const [messages, setMessages] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);


  const sendMessage = async () => {
    if (!message) {
      return alert('please write a message first')
    }
    const userMessage = {
      role: "user",
      content: message,
    };
    setMessages((prev: any) => [...prev, userMessage]);
    setLoading(true);
    setMessage("");
    try {
      const result = await fetch("http://localhost:8000/messages", {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage.content,
        })
      })
      const data = await result.json()
      const aiMessage = {
        role: "bot",
        content: data.response,
      };
      setMessages((prev: any) => [...prev, aiMessage]);
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false);
    }
  }
  return (
    <main className="min-h-screen bg-gray-100 flex flex-col items-center px-4 py-8">
      <h1 className="text-4xl font-bold mb-6 text-center">
        AI Sales Agent
      </h1>

      <div className="w-full max-w-4xl h-[500px] bg-white border border-gray-300 rounded-2xl shadow-md flex flex-col">

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-5">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`mb-4 flex ${msg.role === "user"
                  ? "justify-end"
                  : "justify-start"
                }`}
            >
              <div
                className={`px-4 py-3 rounded-2xl max-w-[75%]  ${msg.role === "user"
                    ? "bg-blue-500 text-white"
                    : "bg-gray-200 text-black"
                  }`}
              >
                {msg.content}
              </div>
            </div>
          ))}

          {loading && (
            <p className="text-sm text-gray-500">
              AI is typing...
            </p>
          )}
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-200 p-4 flex gap-3">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type a message..."
            className="flex-1 border border-gray-300 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-blue-400"
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
          />

          <button
            onClick={sendMessage}
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-xl transition"
          >
            Send
          </button>
        </div>
      </div>
    </main>
  );
}