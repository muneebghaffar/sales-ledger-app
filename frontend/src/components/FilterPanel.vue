<template>
  <div class="w-full md:w-64 bg-white rounded-lg shadow-md p-4">
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2"
        >Select Period:</label
      >
      <Dropdown
        :options="periods"
        :modelValue="localSelectedPeriod"
        @update:modelValue="onPeriodChange"
      />
    </div>

    <div class="mb-6">
      <h3 class="text-sm font-medium text-gray-700 mb-3">Date Range</h3>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >From:</label
          >
          <DatePicker
            :modelValue="localFromDate"
            :maxDate="toDate || currentDate"
            @update:modelValue="onFromDateChange"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >To:</label
          >
          <DatePicker
            :modelValue="localToDate"
            :maxDate="currentDate"
            @update:modelValue="onToDateChange"
          />
        </div>
      </div>
    </div>

    <div class="mb-6">
      <h3 class="text-sm font-medium text-gray-700 mb-2">Customers</h3>
      <Dropdown
        :options="salesData?.meta?.customers"
        :modelValue="localSelectedCustomer"
        @update:modelValue="onCustomerChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import DatePicker from "./common/DatePicker.vue";
import Dropdown from "./common/Dropdown.vue";

const props = defineProps({
  salesData: Object,
  periods: Array,
  selectedPeriod: String,
  selectedCustomer: String,
  fromDate: String,
  toDate: String,
  currentDate: String,
});

const emit = defineEmits([
  "update:selectedPeriod",
  "update:selectedCustomer",
  "update:fromDate",
  "update:toDate",
  "applyFilters",
  "updateChart",
]);

const localSelectedPeriod = ref(props.selectedPeriod);
const localSelectedCustomer = ref(props.selectedCustomer);
const localFromDate = ref(props.fromDate);
const localToDate = ref(props.toDate);

watch(
  () => props.selectedPeriod,
  (value) => {
    localSelectedPeriod.value = value;
  }
);

watch(
  () => props.selectedCustomer,
  (value) => {
    localSelectedCustomer.value = value;
  }
);

watch(
  () => props.fromDate,
  (value) => {
    localFromDate.value = value;
  }
);

watch(
  () => props.toDate,
  (value) => {
    localToDate.value = value;
  }
);

const onPeriodChange = (value) => {
  emit("update:selectedPeriod", value);
  emit("updateChart");
};

const onCustomerChange = (value) => {
  emit("update:selectedCustomer", value);
  emit("applyFilters");
};

const onFromDateChange = (value) => {
  emit("update:fromDate", value);
  emit("applyFilters");
};

const onToDateChange = (value) => {
  emit("update:toDate", value);
  emit("applyFilters");
};
</script>
