<template>
  <v-container>
    <h3>Site Details</h3>
    <p><b>{{siteInfo.url}}</b></p>

    <SiteAvailabilityChart :availabilityData="availabilityData" />
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import SiteAvailabilityChart from './SiteAvailabilityChart.vue';
import api from "../api";

const route = useRoute();
const siteId = route.params.id;
const availabilityData = ref([]);
const siteInfo = ref({})
const token = localStorage.getItem("token");

// Функция для получения данных о доступности сайта
const fetchAvailabilityData = async () => {
  try {
    const response = await api.getSiteData(token, siteId); // Добавлено await
    availabilityData.value = response.data.site_data;
    siteInfo.value = response.data.site_info
    console.log( availabilityData);
  } catch (error) {
    console.error('Error fetching availability data:', error);
  }
};

onMounted(() => {
  fetchAvailabilityData();
});
</script>

<style scoped>
/* Ваши стили для компонента */
</style>
