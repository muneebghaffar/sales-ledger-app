<!-- App.vue -->
<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto p-5">
      <header class="mb-6">
        <h1 class="text-3xl font-bold text-gray-800">
          {{ salesData?.company_name || "Loading..." }}
        </h1>
      </header>

      <div class="flex flex-col md:flex-row gap-6">
        <FilterPanel
          :salesData="salesData"
          :periods="periods"
          :selectedPeriod="selectedPeriod"
          :selectedCustomer="selectedCustomer"
          :fromDate="fromDate"
          :toDate="toDate"
          :currentDate="currentDate"
          @update:selectedPeriod="selectedPeriod = $event"
          @update:selectedCustomer="selectedCustomer = $event"
          @update:fromDate="fromDate = $event"
          @update:toDate="toDate = $event"
          @applyFilters="applyFilters"
          @updateChart="updateChart"
        />

        <div class="flex-grow bg-white rounded-lg shadow-md p-4">
          <SalesChart
            :error="error"
            :selectedPeriod="selectedPeriod"
            :chartData="chartData"
            :chartOptions="chartOptions"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from "vue";
import { useSalesData } from "./composables/useSalesData";
import FilterPanel from "./components/FilterPanel.vue";
import SalesChart from "./components/SalesChart.vue";

export default {
  name: "App",
  components: {
    FilterPanel,
    SalesChart,
  },
  setup() {
    const { salesData, periods, error, fetchSalesData } = useSalesData();

    fetchSalesData();

    const selectedPeriod = ref("");
    const selectedCustomer = ref("");
    const selectedYear = ref(null);
    const fromDate = ref("");
    const toDate = ref("");

    // Set the current date as the maximum allowed date
    const currentDate = "2025-04-26";

    const availableYears = computed(() => {
      if (!periods.value.length) return [];
      return periods.value
        .map((period) => parseInt(period.replace("F", "")) - 1)
        .sort();
    });

    watch(availableYears, (years) => {
      if (years.length && !selectedYear.value) {
        selectedYear.value = years[years.length - 1];
      }
    });

    const applyFilters = () => {
      const filters = {};
      if (selectedCustomer.value) filters.customer = [selectedCustomer.value];
      if (selectedYear.value) filters.date = selectedYear.value;
      if (fromDate.value) filters.fromDate = fromDate.value;
      if (toDate.value) filters.toDate = toDate.value;
      fetchSalesData(filters);
    };

    const chartData = ref({
      labels: [],
      datasets: [],
    });

    const chartOptions = ref({
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: "rgba(0, 0, 0, 0.05)",
          },
          ticks: {
            font: {
              size: 12,
            },
            color: "#64748b",
          },
          title: {
            display: true,
            text: "Sales Amount ($)",
            font: {
              size: 14,
              weight: "bold",
            },
            color: "#475569",
          },
        },
        x: {
          grid: {
            color: "rgba(0, 0, 0, 0.05)",
          },
          ticks: {
            font: {
              size: 12,
            },
            color: "#64748b",
          },
          title: {
            display: true,
            text: "Month",
            font: {
              size: 14,
              weight: "bold",
            },
            color: "#475569",
          },
        },
      },
      plugins: {
        legend: {
          position: "top",
          labels: {
            font: {
              size: 12,
            },
            boxWidth: 15,
            padding: 15,
          },
        },
        title: {
          display: true,
          text: "Monthly Sales by Product",
          font: {
            size: 16,
            weight: "bold",
          },
          color: "#334155",
          padding: {
            top: 10,
            bottom: 20,
          },
        },
        tooltip: {
          backgroundColor: "rgba(255, 255, 255, 0.9)",
          titleColor: "#334155",
          bodyColor: "#475569",
          borderColor: "rgba(0, 0, 0, 0.1)",
          borderWidth: 1,
          padding: 10,
          boxPadding: 5,
          usePointStyle: true,
          callbacks: {
            label: function (context) {
              let label = context.dataset.label || "";
              if (label) {
                label += ": ";
              }
              if (context.parsed.y !== null) {
                label += new Intl.NumberFormat("en-US", {
                  style: "currency",
                  currency: "USD",
                  minimumFractionDigits: 0,
                }).format(context.parsed.y);
              }
              return label;
            },
          },
        },
      },
    });

    const updateChart = () => {
      if (
        !selectedPeriod.value ||
        !salesData.value?.periods?.[selectedPeriod.value]
      ) {
        chartData.value = { labels: [], datasets: [] };
        return;
      }

      try {
        const periodData = salesData.value.periods[selectedPeriod.value];
        const months = Object.keys(periodData).sort();
        const products = [
          ...new Set(months.flatMap((month) => Object.keys(periodData[month]))),
        ];

        const datasets = products.map((product, index) => {
          const data = months.map((month) => {
            const transactions = periodData[month][product] || [];
            const total = transactions.reduce(
              (sum, tx) => sum + (tx.Amount || 0),
              0
            );
            return total;
          });

          // Default color palette if product_colors is not available
          const defaultColors = [
            "#0369a1",
            "#0891b2",
            "#0e7490",
            "#1e40af",
            "#4f46e5",
            "#7e22ce",
            "#a21caf",
            "#be185d",
            "#be123c",
            "#b91c1c",
            "#c2410c",
            "#ca8a04",
            "#65a30d",
            "#16a34a",
            "#059669",
          ];

          return {
            label: product,
            backgroundColor:
              salesData.value?.product_colors?.[product] ||
              defaultColors[index % defaultColors.length],
            borderRadius: 4,
            maxBarThickness: 50,
            data,
          };
        });

        chartData.value = {
          labels: months.map((month) => {
            const date = new Date(month + "-01");
            return date.toLocaleString("default", {
              month: "short",
              year: "numeric",
            });
          }),
          datasets,
        };
      } catch (err) {
        console.error("Error updating chart:", err);
        chartData.value = { labels: [], datasets: [] };
      }
    };

    watch([selectedPeriod, salesData], () => {
      updateChart();
    });

    watch(periods, (newPeriods) => {
      if (newPeriods.length && !selectedPeriod.value) {
        selectedPeriod.value = newPeriods[newPeriods.length - 1];
      }
    });

    return {
      salesData,
      periods,
      error,
      selectedPeriod,
      selectedCustomer,
      selectedYear,
      fromDate,
      toDate,
      currentDate,
      availableYears,
      applyFilters,
      chartData,
      chartOptions,
      updateChart,
    };
  },
};
</script>
