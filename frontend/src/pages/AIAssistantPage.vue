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
              <p>{{ msg.content }}</p>
            </div>
          </div>
        </div>

        <form class="input-area" @submit.prevent="sendMessage">
          <input
            v-model="currentQuestion"
            type="text"
            placeholder="例如：为什么中国古建筑不用钉子？"
          />
          <button type="submit">发送</button>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import api from "@/services/api";

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

const loadFAQ = async () => {
  const res = await api.get("/faq/");
  faq.value = res.data;
};

const fillQuestion = (q: string) => {
  currentQuestion.value = q;
};

const sendMessage = () => {
  if (!currentQuestion.value.trim()) return;
  const q = currentQuestion.value.trim();
  messages.value.push({ role: "user", content: q });

  // 暂无真正 AI 接口，这里简单用 FAQ 中的匹配答案或占位回复
  const matched = faq.value.find((f) => q.includes(f.question.slice(0, 4)));
  if (matched) {
    messages.value.push({ role: "ai", content: matched.answer });
  } else {
    messages.value.push({
      role: "ai",
      content: "这是一个很好的问题，目前示例版暂未接入真实大模型，我会在正式版中为你详细解答。",
    });
  }

  currentQuestion.value = "";
};

onMounted(() => {
  loadFAQ();
});
</script>

