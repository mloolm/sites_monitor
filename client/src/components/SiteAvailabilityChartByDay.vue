<template>
  <div class="site-chart">
    <Line :chartData="chartData" :chartOptions="chartOptions" />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale);

const props = defineProps({
  availabilityData: {
    type: Array,
    required: true,
  },
});

const formatDate = (dateString) => {
  const options = { day: '2-digit', month: '2-digit', year: '2-digit', hour12: false };
  return new Date(dateString).toLocaleString('ru-RU', options).replace(',', '');
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      min: 0,
      ticks: {
        stepSize: 10,
      },
    },
  },
  plugins: {
    tooltip: {
      callbacks: {
        label: function(tooltipItem) {
          const index = tooltipItem.dataIndex;
          const uptimeValue = tooltipItem.dataset.data[index];
          return [
            `Uptime: ${uptimeValue}%`,
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
      label: 'Uptime (%)',
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

      chartData.value.labels = newData.map(item => formatDate(item.uptime));
      chartData.value.datasets[0].data = newData.map(item => item.uptime);
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
