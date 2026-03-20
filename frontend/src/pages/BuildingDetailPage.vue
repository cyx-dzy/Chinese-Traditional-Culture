<template>
  <div class="page detail-page" v-if="building">
    <section class="hero">
      <div class="hero-text">
        <h1>{{ building.name }}</h1>
        <p class="subtitle">
          {{ building.dynasty }} · {{ building.location }} ·
          {{ building.category }}
        </p>
        <p class="summary">{{ building.summary }}</p>
      </div>
      <div class="hero-cover" :style="coverStyle(building.cover_image)"></div>
    </section>

    <section class="section core-stats">
      <h2>核心数据速览</h2>
      <div class="stats-grid">
        <div v-if="building.height">
          <h3>高度</h3>
          <p>{{ building.height }} 米</p>
        </div>
        <div v-if="building.bay_count">
          <h3>面阔间数</h3>
          <p>{{ building.bay_count }}</p>
        </div>
        <div v-if="building.dougong_types">
          <h3>斗拱种类</h3>
          <p>{{ building.dougong_types }}</p>
        </div>
        <div v-if="building.earthquake_resistance">
          <h3>抗震记录</h3>
          <p>{{ building.earthquake_resistance }}</p>
        </div>
        <div v-if="building.material">
          <h3>主要材料</h3>
          <p>{{ building.material }}</p>
        </div>
        <div v-if="building.preservation_status">
          <h3>保存状况</h3>
          <p>{{ building.preservation_status }}</p>
        </div>
      </div>
    </section>

    <section class="section details-tabs">
      <h2>详细介绍</h2>
      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          :class="['tab', { active: activeTab === tab.key }]"
          @click="activeTab = tab.key"
        >
          {{ tab.label }}
        </button>
      </div>

      <div class="tab-content">
        <article
          v-for="d in filteredDetails"
          :key="d.id"
          class="detail-section"
        >
          <h3>{{ formatText(d.title) }}</h3>
          <p class="content">{{ formatText(d.content) }}</p>
        </article>
      </div>
    </section>

    <section class="section gallery" v-if="building.images.length">
      <h2>图像赏析</h2>
      <div class="image-grid">
        <figure v-for="img in building.images" :key="img.id">
          <div class="image" :style="imgStyle(img.image_path)"></div>
          <figcaption>{{ img.caption }}</figcaption>
        </figure>
      </div>
    </section>

    <section class="section related" v-if="building.related_buildings.length">
      <h2>相关建筑推荐</h2>
      <div class="card-grid">
        <div
          v-for="item in building.related_buildings"
          :key="item.id"
          class="card"
          @click="
            $router.push({ name: 'building-detail', params: { id: item.id } })
          "
        >
          <div class="card-cover" :style="coverStyle(item.cover_image)"></div>
          <div class="card-body">
            <h3>{{ item.name }}</h3>
            <p class="meta">{{ item.dynasty }} · {{ item.category }}</p>
          </div>
        </div>
      </div>
    </section>

    <button class="ai-float-inner" @click="$router.push({ name: 'ai' })">
      就这座建筑问 AI
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import api from "@/services/api";

interface Detail {
  id: number;
  section_type: string;
  title: string;
  content?: string;
}

interface ImageItem {
  id: number;
  image_path: string;
  image_type: string;
  caption?: string;
}

interface BuildingDetail {
  id: number;
  name: string;
  dynasty: string;
  location?: string;
  category: string;
  summary?: string;
  cover_image?: string | null;
  height?: number | null;
  bay_count?: string | null;
  dougong_types?: string | null;
  earthquake_resistance?: string | null;
  material?: string | null;
  preservation_status?: string | null;
  images: ImageItem[];
  details: Detail[];
  related_buildings: any[];
}

const route = useRoute();
const building = ref<BuildingDetail | null>(null);

const tabs = [
  { key: "history", label: "历史沿革" },
  { key: "structure", label: "结构成就" },
  { key: "material", label: "材料与工艺" },
  { key: "culture", label: "文化价值" },
];

const activeTab = ref<string>("history");

const filteredDetails = computed(() => {
  if (!building.value) return [];
  return building.value.details.filter(
    (d) => d.section_type === activeTab.value,
  );
});

const loadDetail = async () => {
  const id = Number(route.params.id);
  if (!id) return;
  const res = await api.get(`/buildings/${id}`);
  building.value = res.data;
};

const coverStyle = (url?: string | null) => {
  if (!url) return {};
  return { backgroundImage: `url(${url})` };
};

const imgStyle = (url: string) => ({ backgroundImage: `url(${url})` });

const formatText = (text?: string) => {
  if (!text) return '';
  return text.replace(/^[""'']+|[""'']+$/g, '');
};

onMounted(() => {
  loadDetail();
});
</script>

