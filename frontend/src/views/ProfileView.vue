<template>
    <div>
        <main class="px-10 mb:px-15 lg:px-20 py-6 bg-[#BADFE7] font-OpenSans">
            <div class="max-w-7xl px-3 md:px-8 lg:px-10 grid grid-cols-1 lg:grid-cols-4 gap-2 lg:gap-4">
                <!-- left side - pfp, name, number of post, edit profile and logout button start-->
                <div class="col-span-1">
                    <div class="bg-white shadow-md p-4 text-center rounded">
                        <!-- pfp -->
                        <div class="mb-6 flex justify-center">
                            <img :src="user.get_avatar" class="shadow-md w-[100px] h-[100px] md:w-[150px] md:h-[150px] lg:w-[200px] lg:h-[200px] rounded-full">
                        </div>  
                        <!-- name -->
                        <div class="pt-4">
                            <p class="font-bold text-sm md:text-base lg:text-lg">{{user.name}}</p>
                            <p class="text-[#979797] text-[10px] lg:text-xs mb-4">{{user.posts_count}} posts</p>
                        </div>
                        <!-- edit profile routerlink since it will go to ediprofileview.vue -->
                        <RouterLink 
                            class="inline-block mr-3 py-2 px-3 xl:px-4 
                            bg-[#C2EDCE] text-[10px] xl:text-xs rounded
                            hover:bg-emerald-700 hover:text-white" 
                            to="/profile/edit"
                            v-if="userStore.user.id === user.id"
                        >
                            Edit Profile
                        </RouterLink>
                        <!-- logout button -->
                        <button 
                            class="inline-block py-2 px-3 xl:px-4
                            bg-[#FCD19C] text-[10px] xl:text-xs rounded
                            hover:bg-amber-700 hover:text-white" 
                            @click="logout"
                            v-if="userStore.user.id === user.id"
                        >
                            Log out
                        </button>
                    </div>
                </div>
                <!-- left side - pfp, name, number of post, edit profile and logout button end-->

                <!-- main center - posting and posts start -->
                <div class="main-center col-span-3 ">
                    <!-- posting start -->
                    <div class="bg-white shadow-md p-6 mb-4 text-center rounded" v-if="userStore.user.id === user.id">
                        <form action="" method="post" v-on:submit.prevent="submitForm">
                            <!-- textfield -->
                            <div class="pb-2 lg:pb-4">
                                <textarea v-model="body" class="p-3 lg:p-4 w-full bg-[#F6F6F2] rounded-lg text-sm md:text-base lg:text-lg" placeholder="What are you thinking about?"></textarea>
                            </div>
                            <!-- attachimage and post -->
                            <div class="p-4 border-t border-gray-100 flex justify-between">
                                <!-- for attach image shit js below -->
                                <label class="inline-block py-4 px-6 bg-[#388087] text-white rounded-lg">
                                    <input type="file" ref="file" @change="handleFileChange">
                                    <!-- fileName sa js below -->
                                    <span v-if="fileName" class="text-sm text-gray-300">{{ fileName }}</span>
                                    <span v-else>Attach image</span>
                                </label>
                                <button class="inline-block py-4 px-6 bg-[#c2edce] text-black rounded-lg">Post</button>
                                </div>
                        </form>
                    </div>
                    <!-- posting end -->

                    <!-- posts start -->
                    <div class="bg-white shadow-md p-8 rounded mb-3" v-for="post in posts" v-bind:key="post.id">
                        <!--pfp name and time starts -->
                        <div class="flex items-center justify-between mb-6">
                            <div class="flex items-center">
                                <router-link :to="{name: 'profile', params: {id: post.created_by.id}}">
                                    <img :src="user.get_avatar" class="w-[40px] rounded-full mr-2">
                                </router-link>

                                <p><strong><router-link :to="{name: 'profile', params:{'id': post.created_by.id}}">{{ post.created_by.name }}</router-link></strong></p>
                            </div>
                            <div class="flex items-center">
                                <p class="text-[#979797] mr-1 text-xs md:text-sm lg:text-base">{{ post.created_at_formatted }}</p>
                                <div @click="toggleExtraModal">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3 h-3 md:w-4 md:h-4 lg:w-6 lg:h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z" />
                                    </svg>
                                </div>
                            </div>
                        </div>
                        <!--pfp name and time end -->

                        <!-- mismong post start -->
                        <template v-if="post.attachments.length">
                            <img v-for="image in post.attachments" v-bind:key="image.id" :src="image.get_image" class="w-full mb-4 rounded-xl">
                        </template>
                        
                        <p class="text-xs md:text-sm lg:text-base">{{ post.body }}</p>
                        <!-- mismong post start -->

                        <!-- comment and like and yung dotdotdot start-->
                        <div class="flex justify-between">
                            <div class="flex space-x-6 pt-6">
                                <!-- like -->
                                <div class="flex items-center space-x-2" @click="likePost(post.id)">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                                    </svg>
                                    <span class="text-gray-500 text-xs hover:cursor-pointer">{{ post.likes_count }} {{ post.likes_count === 1 || post.likes_count === 0 ? 'like' : 'likes' }}</span>
                                </div>
                                <!-- comment -->
                                <div class="flex items-center space-x-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z" />
                                    </svg>
                                    <router-link :to="{name: 'postview', params: {id: post.id}}" class="text-gray-500 text-xs hover:cursor-pointer">{{ post.comments_count }} comments</router-link>
                                </div>
                            </div>
                        </div>
                        <!-- comment and like and yung dotdotdot end-->

                        <!-- delete post dotdotdot start -->
                        <div v-if="showExtraModal">
                            <div class="flex items-center space-x-6 justify-end">
                                <div 
                                    class="flex items-center space-x-2 hover:cursor-pointer" 
                                    @click="deletePost(post.id)"
                                    v-if="userStore.user.id == post.created_by.id"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-red-500">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 6.75l-1.5 14.25h-12L4.5 6.75M7.5 6.75v-.75a2.25 2.25 0 012.25-2.25h4.5A2.25 2.25 0 0116.5 6v.75M7.5 6.75h9M9.75 10.5v6.75M14.25 10.5v6.75" />
                                    </svg>
                                    <p class="text-red-500">Delete Post</p>
                                </div>
                            </div>
                        </div>
                        <!-- delete post dotdotdot end -->
                    </div>
                    <!-- posts end -->
                </div>
                <!-- main center - posting and posts end -->
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
