import api from "./api";

interface ChatResponse {
  response: string;
}

export const chatWithAI = async (message: string): Promise<ChatResponse> => {
  try {
    const res = await api.post<ChatResponse>("/ai/chat", { message });
    return res.data;
  } catch (error) {
    console.error("AI对话失败:", error);
    throw error;
  }
};
