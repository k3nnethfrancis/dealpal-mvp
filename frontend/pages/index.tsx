import { Chat } from "@/components/Chat/Chat";
import { Footer } from "@/components/Layout/Footer";
import { Navbar } from "@/components/Layout/Navbar";
import { Message } from "@/types";
import Head from "next/head";
import { useEffect, useRef, useState } from "react";

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [file, setFile] = useState<File | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleFileChange = (selectedFile: File) => {
    setFile(selectedFile);
  };

  const handleSend = async (message: Message) => {
    console.log("Sending message:", message);
    const updatedMessages = [...messages, message];
  
    setMessages(updatedMessages);
    setLoading(true);
  
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_message: message.content })  // Send a JSON object
    });
  
    if (!response.ok) {
      setLoading(false);
      throw new Error(response.statusText);
    }
  
    const data = await response.json();
  
    if (!data) {
      return;
    }
  
    setLoading(false);
  
    setMessages((messages) => [
      ...messages,
      {
        role: "assistant",
        content: data.bot_response  // Use the correct field name
      }
    ]);
  };

  const handleReset = () => {
    setMessages([
      {
        role: "assistant",
        content: `Yoyo! I'm Ari, your talent management AI assistant. I can help you write copy, respond to RFPs, lookup information, and help you close deals by matching creators to brands. Where would u like to start?`
      }
    ]);
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    setMessages([
      {
        role: "assistant",
        content: `Yoyo! I'm Ari, your talent agent AI assistant. I can help you with things generating persuasive copy, and answering questions about creators you've uploaded. How can I help you?`
      }
    ]);
  }, []);

  return (
    <>
      <Head>
        <title>Chatbot UI</title>
        <meta
          name="description"
          content="A simple chatbot starter kit for OpenAI's chat model using Next.js, TypeScript, and Tailwind CSS."
        />
        <meta
          name="viewport"
          content="width=device-width, initial-scale=1"
        />
        <link
          rel="icon"
          href="/favicon.ico"
        />
      </Head>

      <div className="flex flex-col h-screen">
        <Navbar />

        <div className="flex-1 overflow-auto sm:px-10 pb-4 sm:pb-10">
          <div className="max-w-[800px] mx-auto mt-4 sm:mt-12">
          <input type="file" onChange={(e) => e.target.files && handleFileChange(e.target.files[0])} />            <Chat
              messages={messages}
              loading={loading}
              onSend={handleSend}
              onReset={handleReset}
            />
            <div ref={messagesEndRef} />
          </div>
        </div>
        <Footer />
      </div>
    </>
  );
}