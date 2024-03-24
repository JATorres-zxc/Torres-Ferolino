from django.forms import ModelForm
from .models import *


# forms to set what is needed for that form

class PostForm(ModelForm): 
    class Meta:
        model = Post
        fields = ('body',)
        
class AttachmentForm(ModelForm):
    class Meta:
        model = PostAttachment
        fields = ('image',)