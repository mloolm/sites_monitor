<template>
  <v-container>
    <h4>Chart</h4>
    <Line :chartData="chartData" :chartOptions="chartOptions" />

  </v-container>
</template>

<script setup>
import { ref, watch } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale } from 'chart.js';

// Регистрация компонентов Chart.js
ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale);

const props = defineProps({
  availabilityData: {
    type: Array,
    required: true,
  },
});

const formatDate = (dateString) => {
  const options = { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false };
  return new Date(dateString).toLocaleString('ru-RU', options).replace(',', '');
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      min: 0,
      max: 100,
      ticks: {
        stepSize: 50,
      },
    },
  },
  plugins: {
    tooltip: {
      callbacks: {
        label: function(tooltipItem) {
          const index = tooltipItem.dataIndex;
          const availability = tooltipItem.dataset.data[index];
          const responseCode = props.availabilityData[index].code;
          const RespTime =  props.availabilityData[index].response_time_ms;
          return [
            `Availability: ${availability}%`,
            `Response Code: ${responseCode}`,
            `Response Time: ${RespTime}ms`
          ];
        }
      }
    }
  }
};


const chartData = ref({
  labels: [],
  datasets: [
    {
      label: 'Availability (%)',
      data: [],
      borderColor: 'rgba(75, 192, 192, 1)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      fill: true,
    },
  ],
});

watch(
  () => props.availabilityData,
  (newData) => {
    if (newData && newData.length > 0) {

      chartData.value.labels = newData.map(item => formatDate(item.check_dt));
      chartData.value.datasets[0].data = newData.map(item => item.is_ok ? 100 : 0);
    } else {

      chartData.value.labels = [];
      chartData.value.datasets[0].data = [];
    }
  },
  { immediate: true }
);


</script>

<style scoped>
/* Ваши стили для графика */
</style>
