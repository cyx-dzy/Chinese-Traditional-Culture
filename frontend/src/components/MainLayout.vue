<template>
  <div class="layout">
    <header class="header">
      <div class="logo" @click="$router.push('/')">
        <span class="logo-main">栋宇遗风</span>
        <span class="logo-sub">中国古代建筑成就数字展</span>
      </div>
      <nav class="nav">
        <button class="nav-link" @click="$router.push('/')">首页</button>
        <button class="nav-link" @click="$router.push({ name: 'category' })">
          建筑成就
        </button>
        <button class="nav-link" @click="$router.push({ name: 'ai' })">
          AI 讲解员
        </button>
        <button class="nav-link" @click="$router.push({ name: 'about' })">
          关于
        </button>
      </nav>
    </header>

    <main class="main">
      <slot />
    </main>

    <button class="ai-float" @click="$router.push({ name: 'ai' })">
      向 AI 提问
    </button>

    <footer class="footer">
      <p>© {{ new Date().getFullYear() }} 栋宇遗风 · 中国古代建筑成就数字展</p>
    </footer>
  </div>
</template>

<script setup lang="ts"></script>

