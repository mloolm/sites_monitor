<template>
  <v-app>
    <v-main>
      <v-container>
        <v-card>
          <v-card-title>Список сайтов</v-card-title>
          <v-list>
            <v-list-item v-for="site in siteStore.sites" :key="site.id">
              <v-list-item-title>{{ site.url }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
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