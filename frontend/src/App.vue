<template>
  <div class="app-root">
    <MainLayout>
      <RouterView />
    </MainLayout>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
import MainLayout from "./components/MainLayout.vue";
</script>

