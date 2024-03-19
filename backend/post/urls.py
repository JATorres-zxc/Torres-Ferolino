from django.urls import path
from .api import *


urlpatterns = [
    path('', postList, name='postList'),
    path('create/', createPost,name='createPost'),
    path('profile/<uuid:id>/', postListProfile, name='postListProfile')
]
