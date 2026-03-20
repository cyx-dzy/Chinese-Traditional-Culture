<template>
  <div class="page home-page">
    <section class="banner">
      <div class="banner-text">
        <h1>中国古代建筑成就数字展</h1>
        <p>探寻千年的木构智慧与营造美学</p>
        <button @click="scrollToHighlights">开始探索</button>
      </div>
    </section>

    <section ref="highlightSection" class="section highlights">
      <h2>建筑成就 · 分类亮点</h2>
      <div class="card-grid">
        <div
          v-for="item in homeData?.highlights || []"
          :key="item.id"
          class="card"
          @click="$router.push({ name: 'building-detail', params: { id: item.id } })"
        >
          <div class="card-cover" :style="coverStyle(item.cover_image)"></div>
          <div class="card-body">
            <h3>{{ item.name }}</h3>
            <p class="meta">{{ item.dynasty }} · {{ item.category }}</p>
            <p class="summary">{{ item.summary }}</p>
          </div>
        </div>
      </div>
    </section>

    <Timeline />

    <section class="section stats" v-if="homeData">
      <h2>数据库概览</h2>
      <p class="total">已收录建筑：{{ homeData.stats.total_buildings }} 处</p>
      <div class="stats-grid">
        <div>
          <h3>按分类</h3>
          <ul>
            <li v-for="(count, cat) in homeData.stats.by_category" :key="cat">
              {{ cat }}：{{ count }} 处
            </li>
          </ul>
        </div>
        <div>
          <h3>按朝代</h3>
          <ul>
            <li v-for="(count, dyn) in homeData.stats.by_dynasty" :key="dyn">
              {{ dyn }}：{{ count }} 处
            </li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section faq" v-if="homeData?.faq_preview?.length">
      <h2>常见问题 · 走进古建</h2>
      <ul>
        <li v-for="item in homeData.faq_preview" :key="item.id">
          <strong>{{ formatText(item.question) }}</strong>
          <p>{{ formatText(item.answer) }}</p>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/services/api";
import Timeline from "@/components/Timeline.vue";

interface HomeData {
  highlights: any[];
  stats: {
    total_buildings: number;
    by_category: Record<string, number>;
    by_dynasty: Record<string, number>;
  };
  faq_preview: any[];
}

const router = useRouter();
const homeData = ref<HomeData | null>(null);
const highlightSection = ref<HTMLElement | null>(null);

const fetchHomeData = async () => {
  const res = await api.get("/home/");
  homeData.value = res.data;
};

const scrollToHighlights = () => {
  if (highlightSection.value) {
    highlightSection.value.scrollIntoView({ behavior: "smooth" });
  } else {
    router.push({ name: "category" });
  }
};

const coverStyle = (url?: string | null) => {
  if (!url) return {};
  return {
    backgroundImage: `url(${url})`,
  };
};

const formatText = (text: string) => {
  return text.replace(/^[""'']+|[""'']+$/g, '');
};

onMounted(() => {
  fetchHomeData();
});
</script>

