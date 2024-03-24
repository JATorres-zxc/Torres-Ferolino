<template>
    <div>
        <main class="px-8 py-6 bg-gray-100">
            <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
                <div class="main-left col-span-1">
                    <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                        <img :src="user.get_avatar" class="mb-6 rounded-full">
                        <p><strong>{{user.name}}</strong></p>
                        <div class="mt-6 flex space-x-8 justify-around">
                            <p class="text-xs text-gray-500">{{user.posts_count}} posts</p>
                        </div>
                        

                        <RouterLink 
                            class="inline-block mr-2 py-4 px-3 bg-purple-600 text-xs text-white rounded-lg" 
                            to="/profile/edit"
                            v-if="userStore.user.id === user.id"
                        >
                            Edit profile
                        </RouterLink>


                        
                        <button 
                            class="inline-block py-4 px-3 bg-red-600 text-xs text-white rounded-lg" 
                            @click="logout"
                            v-if="userStore.user.id === user.id"
                        >
                            Log out
                        </button>
                    </div>
                </div>

                <div class="main-center col-span-3 space-y-4">
                    <div class="bg-white border border-gray-200 rounded-lg" v-if="userStore.user.id === user.id">
                        <form action="" method="post" v-on:submit.prevent="submitForm">
                            <div class="p-4">
                                <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
                            </div>
                            <div class="p-4 border-t border-gray-100 flex justify-between">

                                <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                                    <input type="file" ref="file" @change="handleFileChange">
                                    <span v-if="fileName" class="text-sm text-gray-300">{{ fileName }}</span>
                                    <span v-else>Attach image</span>
                                </label>
                                
                                <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                            </div>
                        </form>
                    </div>

                    <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" v-bind:key="post.id">
                        <div class="mb-6 flex items-center justify-between">
                            <div class="flex items-center space-x-6">
                                <router-link :to="{name: 'profile', params: {id: post.created_by.id}}">
                                    <img :src="user.get_avatar" class="w-[40px] rounded-full">
                                </router-link>
                                <p><strong><router-link :to="{name: 'profile', params:{'id': post.created_by.id}}">{{ post.created_by.name }}</router-link></strong></p>
                            </div>
                            <p class="text-gray-600">{{ post.created_at_formatted}}</p>
                        </div>

                        <template v-if="post.attachments.length">
                            <img v-for="image in post.attachments" v-bind:key="image.id" :src="image.get_image" class="w-full mb-4 rounded-xl">
                        </template>
                        
                        <p>{{ post.body }}</p>
                        <div class="my-6 flex justify-between">
                            <div class="flex space-x-6">
                                <div class="flex items-center space-x-2" @click="likePost(post.id)">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                                    </svg>
                                    <span class="text-gray-500 text-xs">{{ post.likes_count }} {{ post.likes_count === 1 || post.likes_count === 0 ? 'like' : 'likes' }}</span>
                                </div>
                                <div class="flex items-center space-x-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z" />
                                    </svg>
                                    <router-link :to="{name: 'postview', params: {id: post.id}}" class="text-gray-500 text-xs">{{ post.comments_count }} comments</router-link>
                                </div>
                            </div>


                            <div>
                                <div @click="toggleExtraModal">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z" />
                                    </svg>
                                </div>
                            </div>
                        </div>


                        <div v-if="showExtraModal">
                            <div class="flex items-center space-x-6 justify-end">
                                <div 
                                class="flex items-center space-x-2" 
                                @click="deletePost(post.id)"
                                v-if="userStore.user.id == post.created_by.id"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-red-500">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                                    </svg>
                                </div>
                                    <span class="text-red-500 text-xs">Delete post</span>
                            </div>
                        </div>


                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

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
import { useUserStore } from '@/stores/user'
import { mapState } from 'pinia'
import { useCounterStore } from '../stores/counter'

export default {
    // Component name
    name: 'FeedView',

    // Computed properties
    computed: {
        ...mapState(useCounterStore, ['posts_count']), // Map posts_count from useCounterStore
        ...mapState(useCounterStore, {
            myOwnName: 'posts_count', // Define an alias for posts_count
        }),
    },

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
            posts: [], // Array to store posts
            body: '', // Text content of new post
            user: {}, // Object to store user data
            fileName: null, // Name of selected file
            showExtraModal: false, // Flag to control visibility of extra modal
        }
    },

    // Lifecycle hook: Called when component is mounted
    mounted() {
        this.getFeed() // Fetch feed when component is mounted
    },
    
    // Watcher for changes in route parameters
    watch: {
        '$route.params.id': {
            handler: function() {
                this.getFeed() // Fetch feed when route parameter changes
            },
            deep: true,
            immediate: true
        }
    },

    // Component methods
    methods: {
        // Method to fetch feed from the server
        getFeed() {
            axios
                .get(`/api/posts/profile/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)

                    // Update posts and user data with fetched data
                    this.posts = response.data.posts
                    this.user = response.data.user
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        // Method to handle file input change
        handleFileChange(event) {
            const file = event.target.files[0];
            if (file) {
                this.fileName = file.name;
            } else {
                this.fileName = null;
            }
        },

        // Method to submit new post
        submitForm() {
            console.log('submitForm:', this.body);

            // Create form data
            let formData = new FormData()
            formData.append('image', this.$refs.file.files[0])
            formData.append('body', this.body)

            // Submit form data to create new post
            axios
                .post('/api/posts/create/', formData, {
                    headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                .then(response => {
                    console.log('data',response.data)

                    // Add new post to the beginning of posts array
                    this.posts.unshift(response.data)
                    this.body = ''
                    this.posts_count +=1
                    location.reload();
                })
                .catch(error =>{
                    console.log('error',error)
                })
        },

        // Method to delete a post
        deletePost(id) {
            console.log('deletepost', id)

            // Send request to delete the post
            axios
                .delete(`/api/posts/${id}/delete/`)
                .then(response => {
                    console.log(response.data)
                    location.reload();
                })
                .catch(error => {
                    console.log("error", error);
                })
        },

        // Method to like a post
        likePost(id){
            console.log('likepost',id)
            
            // Send request to like the post
            axios
                .post(`/api/posts/${id}/like/`)
                .then(response =>{
                    console.log(response.data);
                    // Reload the page after the like is added
                    location.reload();
                })
                .catch(error =>{
                    console.log('error',error)
                });
        },

        // Method to logout user
        logout(){
            console.log('logout')

            // Remove user token and redirect to login page
            this.userStore.removeToken()
            this.$router.push('/login')
        },

        // Method to toggle visibility of extra modal
        toggleExtraModal(){
            console.log('extramodal')

            // Toggle value of showExtraModal flag
            this.showExtraModal = !this.showExtraModal
        }
    }
}
</script>
