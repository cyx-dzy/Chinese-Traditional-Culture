<template>
  <div class="page category-page">
    <h1>建筑成就 · 分类浏览</h1>

    <div class="filters">
      <select v-model="selectedCategory">
        <option value="">全部分类</option>
        <option v-for="cat in categories" :key="cat" :value="cat">
          {{ cat }}
        </option>
      </select>

      <select v-model="selectedDynasty">
        <option value="">全部朝代</option>
        <option v-for="dyn in dynasties" :key="dyn" :value="dyn">
          {{ dyn }}
        </option>
      </select>

      <input
        v-model="keyword"
        type="text"
        placeholder="搜索建筑名称 / 朝代 / 关键词"
      />

      <button @click="loadBuildings">筛选</button>
    </div>

    <div class="card-grid">
      <div
        v-for="item in buildings"
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
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import api from "@/services/api";

interface BuildingItem {
  id: number;
  name: string;
  dynasty: string;
  category: string;
  summary?: string;
  cover_image?: string | null;
}

const categories = ["木结构", "砖石", "园林", "法式"];
const dynasties = ["先秦", "秦汉", "魏晋", "隋唐", "宋元", "明清"];
const selectedCategory = ref<string>("");
const selectedDynasty = ref<string>("");
const keyword = ref<string>("");
const buildings = ref<BuildingItem[]>([]);
const route = useRoute();

const loadBuildings = async () => {
  const params: Record<string, string> = {};
  if (selectedCategory.value) params.category = selectedCategory.value;
  if (selectedDynasty.value) params.dynasty = selectedDynasty.value;
  if (keyword.value) params.keyword = keyword.value;

  const res = await api.get("/buildings/", { params });
  buildings.value = res.data;
};

const coverStyle = (url?: string | null) => {
  if (!url) return {};
  return { backgroundImage: `url(${url})` };
};

onMounted(() => {
  if (route.query.dynasty) {
    selectedDynasty.value = route.query.dynasty as string;
  }
  loadBuildings();
});

watch(selectedCategory, () => {
  loadBuildings();
});

watch(selectedDynasty, () => {
  loadBuildings();
});
</script>

