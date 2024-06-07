<template>
    <div>
        <main class="px-8 py-6 bg-gray-100">
            <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
                <!-- left side - pfp, name, number of post, edit profile and logout button start-->
                <div class="main-left col-span-1">
                    <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                        <!-- pfp -->
                        <div class="mb-6 flex justify-center">
                            <img :src="user.get_avatar" class="shadow-md w-[100px] h-[100px] md:w-[150px] md:h-[150px] lg:w-[200px] lg:h-[200px] rounded-full">
                        </div>      
                        <!-- name -->
                        <p><strong>{{user.name}}</strong></p>
                        <!-- number of posts -->
                        <div class="mt-1 mb-2 font-bold text-lg"> 
                            <p class="text-gray-500">{{user.posts_count}} posts</p>
                        </div>
                        <!-- edit profile routerlink since it will go to ediprofileview.vue -->
                        <RouterLink 
                            class="inline-block mr-5 py-4 px-3 bg-purple-600 text-xs text-white rounded-lg" 
                            to="/profile/edit"
                            v-if="userStore.user.id === user.id"
                        >
                            Edit profile
                        </RouterLink>
                        <!-- logout button -->
                        <button 
                            class="inline-block py-4 px-3 bg-red-600 text-xs text-white rounded-lg" 
                            @click="logout"
                            v-if="userStore.user.id === user.id"
                        >
                            Log out
                        </button>
                    </div>
                </div>
                <!-- left side - pfp, name, number of post, edit profile and logout button end-->

                <!-- main center - posting and posts start -->
                <div class="main-center col-span-3 space-y-4">
                    <!-- posting start -->
                    <div class="bg-white border border-gray-200 rounded-lg" v-if="userStore.user.id === user.id">
                        <form action="" method="post" v-on:submit.prevent="submitForm">
                            <!-- textfield -->
                            <div class="p-4">
                                <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
                            </div>
                            <!-- attachimage and post -->
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
                    <!-- posting end -->

                    <!-- posts start -->
                    <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" v-bind:key="post.id">
                        <!--pfp name and time starts -->
                        <div class="mb-6 flex items-center justify-between">
                            <div class="flex items-center space-x-6">
                                <router-link :to="{name: 'profile', params: {id: post.created_by.id}}">
                                    <img :src="user.get_avatar" class="w-[40px] rounded-full">
                                </router-link>
                                <p><strong><router-link :to="{name: 'profile', params:{'id': post.created_by.id}}">{{ post.created_by.name }}</router-link></strong></p>
                            </div>
                            <p class="text-gray-600">{{ post.created_at_formatted}}</p>
                        </div>
                        <!--pfp name and time end -->

                        <!-- mismong post start -->
                        <template v-if="post.attachments.length">
                            <img v-for="image in post.attachments" v-bind:key="image.id" :src="image.get_image" class="w-full mb-4 rounded-xl">
                        </template>
                        
                        <p>{{ post.body }}</p>
                        <!-- mismong post start -->

                        <!-- comment and like and yung dotdotdot start-->
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
                                    <router-link :to="{name: 'postview', params: {id: post.id}}" class="text-gray-500 text-xs">{{ post.comments_count }} comments</router-link>
                                </div>
                            </div>

                            <!-- dotdotdot -->
                            <div>
                                <div @click="toggleExtraModal">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z" />
                                    </svg>
                                </div>
                            </div>
                        </div>
                        <!-- comment and like and yung dotdotdot end-->

                        <!-- delete post dotdotdot start -->
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
                        <!-- delete post dotdotdot end -->
                    </div>
                    <!-- posts end -->
                </div>
                <!-- main center - posting and posts end -->
            </div>
        </main>
    </div>
</template>