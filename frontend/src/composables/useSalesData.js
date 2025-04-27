import { ref } from "vue";
import axios from "axios";

export function useSalesData() {
  const salesData = ref(null);
  const periods = ref([]);
  const error = ref(null);

  const fetchSalesData = async (filters = {}) => {
    try {
      // Convert array filters to comma-separated strings if needed
      const params = {};
      if (filters.customer) params.customer = filters.customer;
      if (filters.currency) params.currency = filters.currency;
      if (filters.location) params.location = filters.location;
      if (filters.date) params.date = filters.date;
      if (filters.fromDate) params.fromDate = filters.fromDate;
      if (filters.toDate) params.toDate = filters.toDate;

      const response = await axios.get("http://localhost:8000/api/sales-data", {
        params,
        paramsSerializer: (params) => {
          return Object.entries(params)
            .map(([key, value]) => {
              if (Array.isArray(value)) {
                return value
                  .map((val) => `${key}=${encodeURIComponent(val)}`)
                  .join("&");
              }
              return `${key}=${encodeURIComponent(value)}`;
            })
            .join("&");
        },
      });
      salesData.value = response.data;
      periods.value = Object.keys(salesData.value?.periods || {});
      console.log("Fetched periods:", periods.value);
      error.value = null;
    } catch (err) {
      error.value = err.message || "Network Error";
      console.error("Error fetching sales data:", err);
    }
  };

  return { salesData, periods, error, fetchSalesData };
}
