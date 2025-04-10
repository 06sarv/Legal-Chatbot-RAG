function ChatBubble({ role, message }) {
  const isUser = role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] px-4 py-2 rounded-lg ${
          isUser
            ? "bg-blue-500 text-white"
            : "bg-gray-200 text-gray-900"
        }`}
        dangerouslySetInnerHTML={{ __html: message }}
      />
    </div>
  );
}

export default ChatBubble;
