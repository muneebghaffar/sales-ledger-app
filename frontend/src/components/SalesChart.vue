<template>
  <div class="h-full">
    <div
      v-if="error"
      class="p-4 bg-red-50 rounded-md text-red-600 border border-red-200"
    >
      <p class="font-medium">Error: {{ error }}</p>
    </div>
    <div v-else-if="selectedPeriod && chartData.datasets?.length" class="h-96">
      <Bar :data="chartData" :options="chartOptions" :height="400" />
    </div>
    <div
      v-else
      class="flex items-center justify-center h-96 bg-gray-50 rounded-md"
    >
      <div class="text-center text-gray-500">
        <svg
          class="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
          ></path>
        </svg>
        <p class="mt-2 font-medium">
          No data available for the selected period
        </p>
        <p class="mt-1 text-sm">
          Please select a different period or adjust filters
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

export default {
  name: "SalesChart",
  components: {
    Bar,
  },
  props: {
    error: String,
    selectedPeriod: String,
    chartData: Object,
    chartOptions: Object,
  },
};
</script>

<style>
input[type="date"] {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}
</style>
