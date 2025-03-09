<template>
  <div class="site-list">
    <h2>Список сайтов</h2>
    <ul>
      <li v-for="site in siteStore.sites" :key="site.id">
        {{ site.url }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import {onMounted} from 'vue';
import {useSiteStore} from '../stores/siteStore';

const siteStore = useSiteStore(); // Получаем доступ к хранилищу
const token = localStorage.getItem("token");

onMounted(async () => {
  await siteStore.fetchSites(token); // Загружаем список сайтов при монтировании
});
</script>

<style scoped>
.site-list {
  padding: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 5px 0;
}
</style>