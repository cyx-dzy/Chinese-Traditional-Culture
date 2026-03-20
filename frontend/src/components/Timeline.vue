<template>
  <section class="timeline-section">
    <h2>历史沿革时间轴</h2>
    <div class="timeline-container">
      <div class="timeline-line"></div>
      <div
        v-for="(era, index) in eras"
        :key="era.id"
        class="timeline-node"
        :class="{ active: activeEra === era.id }"
        @mouseenter="handleHover(era.id)"
        @mouseleave="handleLeave"
        @click="handleClick(era)"
      >
        <div class="node-dot"></div>
        <div class="node-label">{{ era.name }}</div>
        
        <div class="node-tooltip" :class="{ show: activeEra === era.id }">
          <div class="tooltip-image" :style="imageStyle(era.image)"></div>
          <div class="tooltip-content">
            <h4>{{ era.buildingName }}</h4>
            <p>{{ era.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const activeEra = ref<string | null>(null);

interface Era {
  id: string;
  name: string;
  dynasty: string;
  buildingName: string;
  description: string;
  image: string;
}

const eras: Era[] = [
  {
    id: 'pre-qin',
    name: '先秦',
    dynasty: '先秦',
    buildingName: '半坡遗址',
    description: '新石器时代仰韶文化聚落遗址，展现早期建筑雏形',
    image: '/image/22/22.1.jpg'
  },
  {
    id: 'qin-han',
    name: '秦汉',
    dynasty: '汉代',
    buildingName: '都江堰',
    description: '世界现存最古老的水利工程，体现古代工程智慧',
    image: '/image/22/22.1.jpg'
  },
  {
    id: 'wei-jin',
    name: '魏晋',
    dynasty: '北魏',
    buildingName: '悬空寺',
    description: '悬挂于悬崖峭壁间的三教合一寺庙',
    image: '/image/14/14.1.jpg'
  },
  {
    id: 'sui-tang',
    name: '隋唐',
    dynasty: '唐代',
    buildingName: '佛光寺东大殿',
    description: '中国现存最古老的木构殿堂，梁思成称"中国第一国宝"',
    image: '/image/1/1.1.jpg'
  },
  {
    id: 'song-yuan',
    name: '宋元',
    dynasty: '宋代',
    buildingName: '晋祠圣母殿',
    description: '宋代建筑典范，采用减柱法等先进技术',
    image: '/image/10/10.1.jpg'
  },
  {
    id: 'ming-qing',
    name: '明清',
    dynasty: '明清',
    buildingName: '故宫',
    description: '世界最大最完整的古代木结构宫殿建筑群',
    image: '/image/6/6.1.jpg'
  }
];

const handleHover = (id: string) => {
  activeEra.value = id;
};

const handleLeave = () => {
  activeEra.value = null;
};

const handleClick = (era: Era) => {
  router.push({ 
    name: 'category',
    query: { dynasty: era.dynasty }
  });
};

const imageStyle = (url?: string) => {
  if (!url) return {};
  return {
    backgroundImage: `url(${url})`,
  };
};
</script>

<style scoped>
.timeline-section {
  margin: 2.5rem 0;
  padding: 2rem;
  background: linear-gradient(135deg, #fff8f0 0%, #f5ebe0 100%);
  border-radius: 1.2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.timeline-section h2 {
  margin: 0 0 2rem 0;
  text-align: center;
  font-size: 1.8rem;
  color: #5c2d20;
}

.timeline-container {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  max-width: 1000px;
  margin: 0 auto;
}

.timeline-line {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #d4a574 0%, #c96f3a 50%, #d4a574 100%);
  transform: translateY(-50%);
  z-index: 1;
}

.timeline-node {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.timeline-node:hover {
  transform: translateY(-5px);
}

.node-dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #c96f3a;
  border: 3px solid #fff;
  box-shadow: 0 2px 8px rgba(201, 111, 58, 0.4);
  transition: all 0.3s ease;
  margin-bottom: 0.5rem;
}

.timeline-node:hover .node-dot,
.timeline-node.active .node-dot {
  transform: scale(1.3);
  background: #e05038;
  box-shadow: 0 4px 12px rgba(224, 80, 56, 0.5);
}

.node-label {
  font-size: 1rem;
  font-weight: 600;
  color: #5c2d20;
  transition: color 0.3s ease;
}

.timeline-node:hover .node-label,
.timeline-node.active .node-label {
  color: #c96f3a;
}

.node-tooltip {
  position: absolute;
  bottom: calc(100% + 15px);
  left: 50%;
  transform: translateX(-50%) translateY(10px);
  width: 280px;
  background: #fff;
  border-radius: 0.8rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  pointer-events: none;
  overflow: hidden;
}

.node-tooltip.show {
  opacity: 1;
  visibility: visible;
  transform: translateX(-50%) translateY(0);
}

.tooltip-image {
  height: 140px;
  background-size: cover;
  background-position: center;
  background-color: #d7c4a4;
}

.tooltip-content {
  padding: 1rem;
}

.tooltip-content h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  color: #5c2d20;
}

.tooltip-content p {
  margin: 0;
  font-size: 0.9rem;
  color: #7a5b4c;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .timeline-section {
    padding: 1.5rem 1rem;
  }

  .timeline-section h2 {
    font-size: 1.4rem;
  }

  .timeline-container {
    flex-wrap: wrap;
    gap: 1rem;
  }

  .timeline-line {
    display: none;
  }

  .timeline-node {
    flex: 0 0 calc(33.333% - 0.67rem);
  }

  .node-tooltip {
    width: 220px;
    bottom: calc(100% + 10px);
  }

  .tooltip-image {
    height: 100px;
  }

  .tooltip-content h4 {
    font-size: 1rem;
  }

  .tooltip-content p {
    font-size: 0.85rem;
  }
}
</style>
