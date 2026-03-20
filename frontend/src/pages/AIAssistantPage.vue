<template>
  <div class="page ai-page">
    <div class="ai-layout">
      <aside class="ai-sidebar">
        <h2>常见问题</h2>
        <ul>
          <li
            v-for="item in faq"
            :key="item.id"
            @click="fillQuestion(item.question)"
          >
            {{ item.question }}
          </li>
        </ul>
      </aside>

      <section class="ai-chat">
        <header class="ai-header">
          <h1>AI 讲解员</h1>
          <p>可以向我提问关于中国古建筑的任何问题。</p>
        </header>

        <div class="chat-window">
          <div v-for="(msg, index) in messages" :key="index" class="chat-row">
            <div :class="['bubble', msg.role]">
              <div v-if="msg.role === 'ai'" class="markdown-content" v-html="renderMarkdown(msg.content)"></div>
              <p v-else>{{ msg.content }}</p>
            </div>
          </div>
        </div>

        <form class="input-area" @submit.prevent="sendMessage">
          <input
            v-model="currentQuestion"
            type="text"
            placeholder="例如：为什么中国古建筑不用钉子？"
            :disabled="isLoading"
          />
          <button type="submit" :disabled="isLoading">
            {{ isLoading ? "发送中..." : "发送" }}
          </button>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import api from "@/services/api";
import { chatWithAI } from "@/services/ai";
import { marked } from "marked";
import DOMPurify from "dompurify";

interface FAQItem {
  id: number;
  question: string;
  answer: string;
}

interface ChatMessage {
  role: "user" | "ai";
  content: string;
}

const faq = ref<FAQItem[]>([]);
const messages = ref<ChatMessage[]>([
  {
    role: "ai",
    content: "你好，我是你的古建 AI 讲解员，可以问我任何关于中国传统建筑的问题。",
  },
]);
const currentQuestion = ref("");
const isLoading = ref(false);

const loadFAQ = async () => {
  const res = await api.get("/faq/");
  faq.value = res.data;
};

const fillQuestion = (q: string) => {
  currentQuestion.value = q;
};

const purify = DOMPurify();

const renderMarkdown = (content: string) => {
  const rawHtml = marked(content);
  return purify.sanitize(rawHtml as string);
};

const sendMessage = async () => {
  if (!currentQuestion.value.trim()) return;
  const q = currentQuestion.value.trim();
  
  messages.value.push({ role: "user", content: q });
  isLoading.value = true;
  
  try {
    const res = await chatWithAI(q);
    messages.value.push({ role: "ai", content: res });
  } catch (error) {
    console.error("AI对话失败:", error);
    messages.value.push({
      role: "ai",
      content: "抱歉，AI服务暂时不可用，请稍后再试。",
    });
  } finally {
    isLoading.value = false;
  }
  
  currentQuestion.value = "";
};

onMounted(() => {
  loadFAQ();
});
</script>

