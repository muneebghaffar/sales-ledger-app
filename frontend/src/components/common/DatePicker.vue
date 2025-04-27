<template>
  <div class="relative">
    <input
      type="date"
      v-model="selectedDate"
      @focus="isOpen = true"
      :max="maxDate"
      class="block w-full rounded-md border border-gray-300 py-2 px-3 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
    />
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
  modelValue: String,
  maxDate: String,
});

const emit = defineEmits(["update:modelValue"]);

const selectedDate = ref(props.modelValue);
const isOpen = ref(false);

watch(
  () => props.modelValue,
  (newValue) => {
    selectedDate.value = newValue;
  }
);

watch(selectedDate, (newValue) => {
  emit("update:modelValue", newValue);
});

document.addEventListener("click", (event) => {
  if (!event.target.closest(".relative")) {
    isOpen.value = false;
  }
});
</script>
