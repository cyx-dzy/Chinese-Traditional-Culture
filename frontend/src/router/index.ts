import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import HomePage from "@/pages/HomePage.vue";
import CategoryPage from "@/pages/CategoryPage.vue";
import BuildingDetailPage from "@/pages/BuildingDetailPage.vue";
import AIAssistantPage from "@/pages/AIAssistantPage.vue";
import AboutPage from "@/pages/AboutPage.vue";

const routes: RouteRecordRaw[] = [
  { path: "/", name: "home", component: HomePage },
  { path: "/category", name: "category", component: CategoryPage },
  {
    path: "/building/:id",
    name: "building-detail",
    component: BuildingDetailPage,
    props: true,
  },
  { path: "/ai", name: "ai", component: AIAssistantPage },
  { path: "/about", name: "about", component: AboutPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

export default router;

