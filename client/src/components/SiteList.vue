<template>
  <div class="site-list">
    <h2>Список сайтов</h2>
    <ul>
      <li v-for="site in sites" :key="site.id">
        {{ site.url }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const sites = ref([]);

onMounted(async () => {
  try {
  const response = await axios.get('/api/sites/'); // Без полного URL!
  sites.value = response.data;
} catch (error) {
  console.error('Ошибка при загрузке сайтов:', error);
}
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