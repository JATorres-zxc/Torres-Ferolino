<template>
    <body> 
    <main class="px-8 py-6 bg-gray-100">
        <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
            <div class="main-center col-span-4 space-y-4">

                <!-- posting section start -->
                <div class="bg-white border border-gray-200 rounded-lg">
                    <form action="" method="post" v-on:submit.prevent="submitForm">
                        <div class="p-4">  
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
                        </div>
                        <div class="p-4 border-t border-gray-100 flex justify-between">
                        <!-- for attach image shit js below -->
                        <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                            <input type="file" ref="file" @change="handleFileChange">
                            <!-- fileName sa js below -->
                            <span v-if="fileName" class="text-sm text-gray-300">{{ fileName }}</span>
                            <span v-else>Attach image</span>
                        </label>
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                        </div>
                    </form>
                </div>
                <!-- posting section end -->

                <!-- posts feed section start -->
                <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" v-bind:key="post.id">

                    <!-- name and time part of the post start -->
                    <div class="mb-6 flex items-center justify-between">
                        <div class="flex items-center space-x-6">
                            <RouterLink :to="{name: 'profile', params: {id: post.created_by.id}}">
                                <img :src="post.created_by.get_avatar" class="w-[40px] rounded-full">
                            </RouterLink>
                            <p><strong><RouterLink :to="{name: 'profile', params:{'id': post.created_by.id}}">{{ post.created_by.name }}</RouterLink></strong></p>
                        </div>

                        <p class="text-gray-600">{{ post.created_at_formatted}}</p>
                    </div>
                    <!-- name and time part of the post end -->

                    <!-- mismong post start -->
                    <template v-if="post.attachments.length">
                        <img v-for="image in post.attachments" v-bind:key="image.id" :src="image.get_image" class="w-full mb-4 rounded-xl">
                    </template>

                    <p>{{ post.body }}</p>
                    <!-- mismong post end -->

                    <!-- like and comment start -->
                    <div class="my-6 flex justify-between">
                        <div class="flex space-x-6">
                            <!-- like -->
                            <div class="flex items-center space-x-2" @click="likePost(post.id)">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                                </svg>  
                                <span class="text-gray-500 text-xs">{{ post.likes_count }} {{ post.likes_count === 1 || post.likes_count === 0 ? 'like' : 'likes' }}</span>
                            </div> 
                            <!-- comment -->
                            <div class="flex items-center space-x-2">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z" />
                                </svg> 
                                <RouterLink :to="{name: 'postview', params: {id: post.id}}" class="text-gray-500 text-xs">{{ post.comments_count }} comments</RouterLink>
                            </div>
                        </div>
                    </div> 
                    <!-- like and comment end -->
                </div>
                <!-- posts feed section end -->
            </div>
        </div>
    </main>
    </body>
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

export default {
    // Component name
    name: 'FeedView',

    // Component data
    data() {
        return {
            posts: [], // Array to store posts
            body: '', // Text content of new post
            fileName: null, // Name of selected file
        }
    },

    // Lifecycle hook: Called when component is mounted
    mounted() {
        // Fetch feed when component is mounted
        this.getFeed()
    },

    // Component methods
    methods: {
        // Method to fetch feed from the server
        getFeed() {
            axios
                .get('/api/posts/')
                .then(response => {
                    console.log('data', response.data)

                    // Update posts array with fetched data
                    this.posts = response.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        // Method to handle file input change
        handleFileChange(event) {
            const file = event.target.files[0];
            if (file) {
                // Update fileName with selected file name
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
                    // this.user.posts_count +=1
                })
                .catch(error =>{
                    console.log('error',error)
                })
        },

        // Method to delete a post
        deletePost(id) {
            // Filter out the post with the given id
            this.posts = this.posts.filter(post => post.id !== id)
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
    }
}
</script>
