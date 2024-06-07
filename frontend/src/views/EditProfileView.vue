<template>
    <div class="flex justify-center p-5 md:p-10 lg:p-20 h-full bg-[#BADFE7]">
        <div class="shadow-md w-full md:w-1/3 bg-[#C2EDCE] content-center text-center font-OpenSans">
            <h1 class="text-lg md:text-xl font-bold leading-10">Edit Profile</h1>
            <RouterLink to="/profile/edit/password" c class="underline text-txt-gray text-center text-xs">Edit password</RouterLink>
        </div>

        <div class="shadow-md w-full md:w-1/2 p-8 md:p-14 bg-white font-OpenSans">
            <form class="space-y-6 text-xs" v-on:submit.prevent="submitForm">
            <div>
                <label class="font-bold">Name</label><br>
                <input placeholder="Your Name" class="w-full mt-2 p-4 border border-gray-200 rounded-lg" v-model="form.name">
            </div>

            <div> 
                <label class="font-bold">E-mail</label><br>
                <input placeholder="Your Email Address" class="w-full mt-2 p-4 border border-gray-200 rounded-lg" v-model="form.email">
            </div>

                    <!-- for attach image shit js below -->
                    <div class="mt-10">
                        <label class="py-2 px-2 md:px-4 bg-[#388087] rounded text-white active:bg-emerald-800 custom-file-upload">
                            <input type="file" ref="file" @change="handleFileChange">
                            <span v-if="fileName" class="text-sm text-white">{{ fileName }}</span>
                            <span v-else>Change Avatar</span>
                        </label>
                    </div>


                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div class="pt-8 flex justify-center">
                        <div class="space-y-6">
                        <button class="py-2 px-3 md:py-3 md:px-5 rounded-full bg-[#BADFE7] hover:bg-sky-800 hover:text-white active:ring active:ring-sky-600">Save changes</button>
                        </div>
                    </div>
                </form>
        </div>
    </div>
</template>

<!-- style for attach image button -->
<style>
    input[type='file']{
        display: none;
    }

    .custom-file-upload{
        border: 1px solid #ccc;
        display: inline-block;
        padding: 6px 12px;
        cursor: pointer;
    }
</style>

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
            // Initialize form with user data
            form: {
                email: this.userStore.user.email,
                name: this.userStore.user.name,
                avatar:null,
            },
            errors: [],
            fileName: null
        }
    },

    // Methods for component
    methods: {
        // Method to handle form submission
        submitForm() {
            // Clear previous errors
            this.errors = []

            // Check if email is missing
            if (this.form.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            // Check if name is missing
            if (this.form.name === '') {
                this.errors.push('Your name is missing')
            }

            // If no errors, proceed with form submission
            if (this.errors.length === 0) {
                // Create form data
                let formData = new FormData()
                formData.append('avatar', this.$refs.file.files[0])
                formData.append('name', this.form.name)
                formData.append('email', this.form.email)

                // Submit form data
                axios
                    .post('/api/editprofile/', formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        // If information update is successful
                        if (response.data.message === 'information updated') {
                            // Show success toast message
                            this.toastStore.showToast(5000, 'The information was saved', 'bg-emerald-500')

                            // Update user information in user store
                            this.userStore.setUserInfo({
                                id: this.userStore.user.id,
                                name: this.form.name,
                                email: this.form.email,
                                avatar: response.data.user.get_avatar
                            })

                            // Navigate back to previous page
                            this.$router.back()
                        } else {
                            // If there are errors, show error toast message
                            this.toastStore.showToast(5000, `${response.data.message}. Please try again`, 'bg-red-300')
                        }
                    })
                    .catch(error => {
                        // Log error if request fails
                        console.log('error', error)
                    })
            }
        },
        handleFileChange(event) {
            const file = event.target.files[0];
            if (file) {
                this.fileName = file.name;
            } else {
                this.fileName = null;
            }
        },
    }
}
</script>