<template>
  <div class="site-chart">
    <Line :chartData="chartData" :chartOptions="chartOptions"/>
  </div>
</template>

<script setup>
import {ref, watch} from 'vue';
import {Line} from 'vue-chartjs';
import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale);

const props = defineProps({
  availabilityData: {
    type: Array,
    required: true,
  },
});

const formatDate = (dateString) => {
  const options = {day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false};
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
        stepSize: 100,
      },
    },
  },
  plugins: {
    tooltip: {
      callbacks: {
        label: function (tooltipItem) {
          const index = tooltipItem.dataIndex;
          const availabilityValue = tooltipItem.dataset.data[index];
          const availability = availabilityValue > 0 ? 'online' : 'offline';

          const responseCode_val = props.availabilityData[index].code;
          const responseCode = ((typeof responseCode_val == 'undefined') || (responseCode_val === null)) ? '-' : responseCode_val

          const RespTime_val = props.availabilityData[index].response_time_ms;
          const RespTime = ((RespTime_val === null) || (RespTime_val === 0)) ? '-' : RespTime_val + 'ms'
          return [
            `Status: ${availability}`,
            `Response Code: ${responseCode}`,
            `Response Time: ${RespTime}`
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
      label: 'Availability',
      data: [],
      borderColor: 'rgba(75, 192, 192, 1)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      fill: true,
    },
    {
      label: 'Response Time (ms)',
      data: [],
      borderColor: 'rgba(255, 99, 132, 1)',
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      fill: false,
      yAxisID: 'y1', // Binding to the second Y axis.
    },
  ],
});

watch(
    () => props.availabilityData,
    (newData) => {
      if (newData && newData.length > 0) {

        chartData.value.labels = newData.map(item => formatDate(item.check_dt));
        chartData.value.datasets[0].data = newData.map(item => item.is_ok ? 100 : 0);
        chartData.value.datasets[1].data = newData.map(item => item.response_time_ms || null); // Время ответа
      } else {
        chartData.value.labels = [];
        chartData.value.datasets[0].data = [];
        chartData.value.datasets[1].data = [];
      }
    },
    {immediate: true}
);
</script>

<style scoped>

</style>