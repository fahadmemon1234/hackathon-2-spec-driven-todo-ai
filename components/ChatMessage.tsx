// components/ChatMessage.tsx
import { ChatMessage as ChatMessageType } from "../frontend/types/chat";

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage = ({ message }: ChatMessageProps) => {
  const isUser = message.role === "user";

  return (
    <>
      <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
        <div
          className={`max-w-[80%] rounded-lg px-4 py-2 ${
            isUser
              ? "bg-blue-600 text-white rounded-br-none"
              : "bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-bl-none"
          }`}
        >
          <div className="whitespace-pre-wrap">{message.content}</div>
          <div
            className={`text-xs mt-1 ${
              isUser ? "text-blue-200" : "text-gray-500 dark:text-gray-400"
            }`}
          >
            {message.timestamp.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </div>
        </div>
      </div>
    </>
  );
};
