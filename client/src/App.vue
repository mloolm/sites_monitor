<template>
  <div id="app">
    <h1>Мониторинг сайтов</h1>
    <AddSiteForm />
    <SiteList />
  </div>
</template>

<script setup>
import AddSiteForm from './components/AddSiteForm.vue';
import SiteList from './components/SiteList.vue';
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