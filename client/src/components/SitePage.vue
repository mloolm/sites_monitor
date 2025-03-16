<template>
  <v-container>
    <h3>Site Details</h3>
    <p><b>{{ siteInfo.url }}</b></p>

    <!-- Кнопки выбора периода -->
    <v-btn-toggle v-model="period" mandatory class="mb-4">
      <v-btn value="day" @click="updatePeriod('day')">Day</v-btn>
      <v-btn value="week" @click="updatePeriod('week')">Week</v-btn>
      <v-btn value="month" @click="updatePeriod('month')">Month</v-btn>
      <v-btn value="year" @click="updatePeriod('year')">Year</v-btn>
    </v-btn-toggle>

    <SiteAvailabilityChart :availabilityData="availabilityData" />
  </v-container>
</template>

<script setup>
import {ref, onMounted} from 'vue';
import {useRoute} from 'vue-router';
import SiteAvailabilityChart from './SiteAvailabilityChart.vue';
import api from "../api";

const route = useRoute();
const siteId = route.params.id;
const availabilityData = ref([]);
const siteInfo = ref({});
const token = localStorage.getItem("token");
const period = ref("week"); // Значение по умолчанию

// Функция для получения данных о доступности сайта
const fetchAvailabilityData = async () => {
  try {
    const response = await api.getSiteData(token, siteId, period.value);
    availabilityData.value = response.data.site_data;
    siteInfo.value = response.data.site_info;
  } catch (error) {
    console.error('Error fetching availability data:', error);
  }
};

// Обновление периода и повторный запрос данных
const updatePeriod = (newPeriod) => {
  period.value = newPeriod;
  fetchAvailabilityData();
};

onMounted(fetchAvailabilityData);
</script>

<style scoped>
/* Ваши стили для компонента */
.v-btn-toggle {
  display: flex;
  gap: 8px;
}
</style>
