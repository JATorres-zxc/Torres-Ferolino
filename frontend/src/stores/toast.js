// Import defineStore function from pinia for creating a store
import { defineStore } from 'pinia'

// Define and export a store named 'useToastStore'
export const useToastStore = defineStore({
    // Unique identifier for the store
    id: 'toast',

    // Define the state of the store
    state: () => ({
        ms: 0, // Duration of the toast message
        message: '', // Content of the toast message
        classes: '', // Additional classes for styling
        isVisible: false // Flag to control the visibility of the toast message
    }),

    // Define actions (methods) that can be performed on the store
    actions: {
        // Action to show a toast message
        showToast(ms, message, classes) {
            // Set the duration, message content, classes, and visibility flag
            this.ms = parseInt(ms) // Convert duration to integer
            this.message = message // Set the message content
            this.classes = classes // Set additional classes for styling
            this.isVisible = true // Set visibility to true

            // Slide the toast message up after a short delay
            setTimeout(() => {
                this.classes += ' -translate-y-28' // Apply CSS class for animation
            }, 10)

            // Remove the slide-up animation class after a delay
            setTimeout(() => {
                this.classes = this.classes.replace('-translate-y-28', '') // Remove animation class
            }, this.ms - 500)

            // Hide the toast message after the specified duration
            setTimeout(() => {
                this.isVisible = false // Set visibility to false
            }, this.ms)
        }
    }
})
