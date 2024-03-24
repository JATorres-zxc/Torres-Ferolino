from django.shortcuts import render
from django.http import JsonResponse
from .serializers import *
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from .models import *
from .forms import * # import form for postform and attachmentform
from usermodel.models import *
from usermodel.serializers import *


# Create your views here.

# same with views.py pero api.py BUT STILL THE SAME FUNCTION


@api_view(['GET']) # GET since retrieve lang naman to show
def postList(request):
    posts = Post.objects.all() # get all post objects( or yung mga post na nagawa)
    
    serializer = PostSerializer(posts,many=True) # serialize posts then many=true since postlist 
    
    return JsonResponse(serializer.data, safe=False) # return serialized posts
    


@api_view(['POST']) # POST since to create something
def createPost(request): 
    form = PostForm(request.POST)  # PostForm from forms.py of post folder with fields na body - body only since yung lang naman 
    attachment = None # set attachment to none muna
    attachment_form = AttachmentForm(request.POST, request.FILES) # AttachmentForm alsofrom post folder with fields na image
    
    # print(request.FILES) 
    # print(attachment_form)

    if attachment_form.is_valid(): # check if AttachmentForm content is valid
        # print('imagevalid')
        attachment = attachment_form.save(commit=False) # save then to allow na maset muna yung created_by before saving to db
        attachment.created_by = request.user # setting the created_by of that attacvhment to the request.user or kung sino yung user na yon
        attachment.save() # save malamang

    if form.is_valid(): # same lang above 
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment: # if may attachment then add lang sa content ng form
            post.attachments.add(attachment)

        user = request.user # set user to the request.user
        user.posts_count = user.posts_count + 1 # increase by 1 that user's posts_count
        user.save()

        serializer = PostSerializer(post) # serialize that post
    # print(data)   
        return JsonResponse(serializer.data, safe=False) 
    else:
        return JsonResponse({'error':'error here'})



# mainly used for ProfileView.vue
@api_view(['GET']) 
def postListProfile(request, id):
    posts = Post.objects.filter(created_by_id=id) # set muna yung mga posts then filter by created_by=id
    user = User.objects.get(pk=id) # set muna to get the user by pk=id
    
    post_serializer = PostSerializer(posts, many=True) # serilizer then many to true since pwede naman
    user_serializer = UserSerializer(user)
    
    # 'posts' and 'user' will be used sa profileView.vue
    return JsonResponse({
        'posts': post_serializer.data,
        'user': user_serializer.data
    }, safe=False)



@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk) # post lang since 1 post lang naman ililike mo per time
    user = request.user # set user


    existing_like = post.likes.filter(created_by=user).first() # check if user already liked the post

    if existing_like:
        existing_like.delete() # if user already liked the post then remove the like vice versa
        post.likes_count = max(post.likes_count - 1, 0)  # ensure likes_count dont go negative
        post.save() 
        return JsonResponse({'message': 'like removed'}) # ket wala na
    else:
        like = Like.objects.create(created_by=user) # if new like palang then create that like 
        post.likes.add(like) 
        post.likes_count += 1 # i++
        post.save()
        return JsonResponse({'message': 'like added'}) # ket wala na


# will be used for PostView.vue which is for adding comment and shit
@api_view(['GET'])
def postDetail(request,pk):
    post = Post.objects.get(pk=pk) # post lang since 1 so pk=pk, pwedeng id=id
    
    # will be used sa PostViwe.vue yung 'post'
    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })


# will be used for PostView.vue which is for adding comment and shit
@api_view(['POST'])
def createComment(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)
    post = Post.objects.get(pk=pk)
    
    
    post.comments.add(comment) # add comment to comments(from models.py)
    post.comments_count = post.comments_count + 1 # increase comments_count
    post.save()
    # print(request.data)
    
    serializer = CommentSerializer(comment) # serialize that comment
    
    return JsonResponse(serializer.data, safe=False) # return that serlized data


# will be used for feedView and profileView.vue
@api_view(['DELETE'])
def deletePost(request, pk): 
    post = Post.objects.filter(created_by=request.user).get(pk=pk) # filter that post by created_by and id or pk para alam san babawasan
    
    post.delete() # delete that post
    user = request.user # set user 
    user.posts_count -=1 # decreatse 1
    user.save()
    
    return JsonResponse({'message':'post deleted'}) #ket wala na
