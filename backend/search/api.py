from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes,authentication_classes

from usermodel.models import *
from usermodel.serializers import *
from post.models import *
from post.serializers import *


# for SearchView.vue
@api_view(['POST'])
def search(request):
    data = request.data
    query = data['query'] # will be used sa SearchView.vue 
    
    # print('qeury',query)
    users = User.objects.filter(name__icontains=query) # para ma initialize yung set ng users based sa name__icontains=query
    users_serializer = UserSerializer(users, many=True) # serialize that shit

    
    posts = Post.objects.filter(body__icontains=query)# para ma initialize yung set ng posts based sa name__icontains=query
    posts_serializer = PostSerializer(posts, many=True)
    
    
    return JsonResponse({'users':users_serializer.data, 'posts':posts_serializer.data},safe=False) # will be used sa SearchView.vue 