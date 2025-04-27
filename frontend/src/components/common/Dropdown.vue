<template>
  <div class="relative">
    <select
      v-model="selectedOption"
      @focus="isOpen = true"
      class="block w-full rounded-md border border-gray-300 bg-white py-2 pl-3 pr-10 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 appearance-none"
    >
      <option disabled value="">Select Option</option>
      <option v-for="option in options" :key="option" :value="option">
        {{ option }}
      </option>
    </select>
    <div
      class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-500"
    >
      <svg
        class="h-4 w-4"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M19 9l-7 7-7-7"
        ></path>
      </svg>
    </div>
    <div
      v-if="isOpen"
      class="absolute z-10 w-full bg-white border border-gray-300 rounded-b-md shadow-lg"
    >
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  modelValue: [String, Number],
  options: Array,
});

const emit = defineEmits(["update:modelValue"]);

const selectedOption = ref(props.modelValue);
const isOpen = ref(false);

watch(
  () => props.modelValue,
  (newValue) => {
    selectedOption.value = newValue;
  }
);

watch(selectedOption, (newValue) => {
  emit("update:modelValue", newValue);
});

document.addEventListener("click", (event) => {
  if (!event.target.closest(".relative")) {
    isOpen.value = false;
  }
});
</script>
