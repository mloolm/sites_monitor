<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
// Убираем импорт AddSiteForm и SiteList, так как они теперь будут загружаться через маршрутизацию
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  padding: 20px;
}
h1 {
  margin-bottom: 20px;
}
</style>