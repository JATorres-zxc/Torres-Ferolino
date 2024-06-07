
<template>
    <div class="flex justify-center p-5 md:p-20 h-full bg-[#BADFE7]">

            <div class="shadow-md w-full md:w-1/2 lg:w-1/3 bg-[#C2EDCE] content-center text-center font-OpenSans">
                <h1 class="text-lg md:text-xl lg:text-2xl font-bold leading-10">Edit password</h1>

                <p class="text-[#979797] text-center text-xs md:text-sm lg:text-base">
                    Change your password here
                </p>
            </div>

            <div class="shadow-md w-full md:w-1/2 lg:w-1/3 p-5 md:p-14 bg-white font-OpenSans">
                <form class="space-y-6 text-xs" v-on:submit.prevent="submitForm">
                    <div>
                        <label>Old password</label><br>
                        <input type="password" v-model="form.old_password" placeholder="Your old password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>New password</label><br>
                        <input type="password" v-model="form.new_password1" placeholder="Your new password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>
                    
                    <div>
                        <label>Repeat password</label><br>
                        <input type="password" v-model="form.new_password2" placeholder="Repeat password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <!-- Display errors if any -->
                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div class="flex justify-center ">
                        <button class="py-3 px-5 rounded-full bg-[#BADFE7] hover:bg-sky-800 hover:text-white active:ring active:ring-sky-600 text-xs md:text-sm lg:text-base">Save changes</button>
                    </div>
                </form>
            </div>
    </div>
</template>

<script>
import axios from 'axios'

import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'

export default {
    setup() {
        // Access toast store and user store
        const toastStore = useToastStore()
        const userStore = useUserStore()

        return {
            toastStore,
            userStore
        }
    },

    // Data for component
    data() {
        return {
            form: {
                old_password: '',
                new_password1: '',
                new_password2: '',
            },
            errors: [],
        }
    },

    // Methods for component
    methods: {
        // Method to handle form submission
        submitForm() {
            // Clear previous errors
            this.errors = []

            // Check if new passwords match
            if (this.form.new_password1 !== this.form.new_password2) {
                this.errors.push('The passwords do not match')
            }

            // If no errors, proceed with form submission
            if (this.errors.length === 0) {
                // Create form data
                let formData = new FormData()
                formData.append('old_password', this.form.old_password)
                formData.append('new_password1', this.form.new_password1)
                formData.append('new_password2', this.form.new_password2)

                // Submit form data
                axios
                    .post('/api/editpassword/', formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        // If password change is successful
                        if (response.data.message === 'success') {
                            // Show success toast message
                            this.toastStore.showToast(5000, 'The information was saved', 'bg-emerald-500')

                            // Redirect to user profile page
                            this.$router.push(`/profile/${this.userStore.user.id}`)
                        } else {
                            // If there are errors, display them
                            const data = JSON.parse(response.data.message)

                            for (const key in data){
                                this.errors.push(data[key][0].message)
                            }
                        }
                    })
                    .catch(error => {
                        // Log error if request fails
                        console.log('error', error)
                    })
            }
        }
    }
}
</script>