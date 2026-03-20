import api from "./api";

export const chatWithAI = async (message: string): Promise<string> => {
  try {
    const res = await api.post<{ response: string }>("/ai/chat", { message });
    return res.data.response;
  } catch (error) {
    console.error("AI对话失败:", error);
    throw error;
  }
};
