<template>
    <body> 
    <main class="px-8 py-6 bg-[#badfe7]">
        <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
            <div class="main-center col-span-4 space-y-4">
                <!-- post section start -->
                <div class="p-4 bg-[#f6f6f2] border border-gray-200 rounded-lg shadow-md" v-if="post.id">

                    <!-- name and time start -->
                    <div class="mb-6 flex items-center justify-between">
                        <!-- pfp and name -->
                        <div class="flex items-center space-x-6">
                            <RouterLink :to="{name: 'profile', params: {id: post.created_by.id}}">
                                <img :src="post.created_by.get_avatar" class="w-[40px] rounded-full">
                            </RouterLink>
                            <p><strong><RouterLink :to="{name: 'profile', params:{'id': post.created_by.id}}">{{ post.created_by.name }}</RouterLink></strong></p>
                        </div>
                        <!-- time -->
                        <p class="text-gray-600">{{ post.created_at_formatted}}</p>
                    </div>
                    <!-- name and time start -->

                    <!-- mismong post start -->
                    <template v-if="post.attachments.length">
                        <img v-for="image in post.attachments" v-bind:key="image.id" :src="image.get_image" class="w-full mb-4 rounded-xl">
                    </template>
                    <p>{{ post.body }}</p>
                    <!-- mismong post end -->
                    
                    <!-- like and comment start-->
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
                    <!-- like and comment end-->
                </div>
                <!-- post section end -->


                <!-- comment section start -->
                <div class="p-4 ml-6 border border-[#50909e] rounded-lg shadow-md">
                    <div class="text-lg font-semibold mb-4">
                        Comments
                    </div>
                    <!-- for loop ng comments -->
                    <div class="comment-item p-4 bg-[#a9d2db] border-gray-200 rounded-lg mb-4" v-for="comment in post.comments" :key="comment.id">
                        <CommentItem :comment="comment" />
                    </div>
                </div>
                <!-- comment section end-->

                <!-- comment form start -->
                <div class="bg-[#f6f6f2] border border-gray-200 rounded-lg shadow-md">
                    <form action="" method="post" v-on:submit.prevent="submitForm">
                        <div class="p-4">  
                            <textarea v-model="body" class="p-4 w-full bg-white rounded-lg" placeholder="What do you think?"></textarea>
                        </div>

                        <div class="p-4 border-t border-gray-100 flex justify-between">
                            <button class="inline-block py-3 px-6 bg-[#c2edce] text-black rounded-lg ml-auto">Comment</button>
                        </div>
                    </form>
                </div>
                <!-- comment form end -->
            </div>
        </div>
    </main>
    </body>
</template>


<script>
import axios from 'axios'
import CommentItem from '../components/CommentItem.vue'

export default {
    // Component name
    name: 'PostView',

    // Components used in this component
    components:{
        CommentItem,
    },

    // Component data
    data() {
        return {
            // Initialize post object with empty comments array
            post: {
                comments:[]
            },
            // Text content of new comment
            body: ''
        }
    },

    // Lifecycle hook: Called when component is mounted
    mounted() {
        // Fetch post when component is mounted
        this.getPost()
    },

    // Component methods
    methods: {
        // Method to fetch post from the server
        getPost() {
            axios
                .get(`/api/posts/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)

                    // Update post object with fetched data
                    this.post = response.data.post
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        // Method to submit new comment
        submitForm() {
            console.log('submitForm:', this.body);

            // Send request to create new comment
            axios
                .post(`/api/posts/${this.$route.params.id}/comment/`, {
                    'body':this.body
                })
                .then(response => {
                    console.log('data',response.data)

                    // Add new comment to post's comments array
                    this.post.comments.push(response.data)
                    this.post.comments_count += 1
                    this.body = ''
                })
                .catch(error =>{
                    console.log('error',error)
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
    }
}
</script>
