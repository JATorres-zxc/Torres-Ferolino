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
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)
    
    print(request.FILES)
    print(attachment_form)

    if attachment_form.is_valid():
        print('imagevalid')
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post.attachments.add(attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

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


@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user

    # Check if the user has already liked the post
    existing_like = post.likes.filter(created_by=user).first()

    if existing_like:
        # If the user has already liked the post, remove the like
        existing_like.delete()
        post.likes_count = max(post.likes_count - 1, 0)  # Ensure likes_count doesn't go negative
        post.save()
        return JsonResponse({'message': 'like removed'})
    else:
        # If the user has not liked the post, add a like
        like = Like.objects.create(created_by=user)
        post.likes.add(like)
        post.likes_count += 1
        post.save()
        return JsonResponse({'message': 'like added'})

@api_view(['GET'])
def postDetail(request,pk):
    post = Post.objects.get(pk=pk)
    
    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })


@api_view(['POST'])
def createComment(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()
    # print(request.data)
    
    serializer = CommentSerializer(comment)
    
    return JsonResponse(serializer.data, safe=False)
