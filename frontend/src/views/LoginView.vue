<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Log in</h1>


                <p class="font-bold">
                    Don't have an account? <RouterLink :to="{'name': 'signup'}" class="underline">Click here</RouterLink> to create one!
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="form.email" placeholder="Your e-mail address" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Password</label><br>
                        <input type="password" v-model="form.password" placeholder="Your password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Log in</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

import { useUserStore } from '@/stores/user'

export default {
    // Setup function to initialize user store
    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },

    // Component data
    data() {
        return {
            // Form fields for email and password
            form: {
                email: '',
                password: '',
            },
            // Array to store form validation errors
            errors: []
        }
    },
    // Component methods
    methods: {
        // Method to handle form submission
        async submitForm() {
            // Clear previous errors
            this.errors = []

            // Check if email is missing
            if (this.form.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            // Check if password is missing
            if (this.form.password === '') {
                this.errors.push('Your password is missing')
            }

            // If no errors, proceed with form submission
            if (this.errors.length === 0) {
                // Attempt to login
                await axios
                    .post('/api/login/', this.form)
                    .then(response => {
                        // Set access and refresh tokens in user store
                        this.userStore.setToken(response.data)

                        // Set authorization header for future requests
                        axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access;
                    })
                    .catch(error => {
                        // Log error and display error message
                        console.log('error', error)
                        this.errors.push('The email or password is incorrect! Or the user is not activated!')
                    })
            }
            
            // If no errors, fetch user information
            if (this.errors.length === 0) {
                await axios
                    .get('/api/me/')
                    .then(response => {
                        // Set user information in user store
                        this.userStore.setUserInfo(response.data)

                        // Redirect to feed page
                        this.$router.push('/feed')
                    })
                    .catch(error => {
                        // Log error if user information fetch fails
                        console.log('error', error)
                    })
            }
        }
    }
}
</script>
