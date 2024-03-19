from django.shortcuts import render
from django.http import JsonResponse
from .serializers import *
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from .models import *
from .forms import *
from usermodel.models import *
from usermodel.serializers import *


# Create your views here.

# for everone's post
@api_view(['GET'])
def postList(request):
    posts = Post.objects.all()
    
    
    serializer = PostSerializer(posts,many=True)
    
    return JsonResponse(serializer.data, safe=False)
    

@api_view(['POST'])
def createPost(request):
    data = request.data
    
    form = PostForm(request.data)

    
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
        
        serializer = PostSerializer(post)
    # print(data)   
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error':'error here'})


# for the user psots only
@api_view(['GET'])
def postListProfile(request, id):
    posts = Post.objects.filter(created_by_id=id)
    user = User.objects.get(pk=id)
    
    post_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)
    
    return JsonResponse({
        'posts': post_serializer.data,
        'user': user_serializer.data
    }, safe=False)
