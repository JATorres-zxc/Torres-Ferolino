// Import necessary functions and modules from Vue
import { ref, computed } from 'vue'
// Import defineStore function from pinia for creating a store
import { defineStore } from 'pinia'

// Define and export a store named 'counter' using defineStore
export const useCounterStore = defineStore('counter', () => {
  // Define a reactive variable called count initialized with 0
  const count = ref(0)
  // Define a computed property doubleCount that doubles the value of count
  const doubleCount = computed(() => count.value * 2)
  // Define a function increment that increments the value of count
  function increment() {
    count.value++
  }

  // Return an object containing count, doubleCount, and increment function
  return { count, doubleCount, increment }
})
