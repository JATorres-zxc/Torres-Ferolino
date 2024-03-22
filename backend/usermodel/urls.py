from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .api import *

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='tokenObtain'),
    path('refresh/', TokenRefreshView.as_view(), name='tokenRefresh'),
    path('signup/', signup, name='signup'),
    path('me/', me, name='me'),
    path('editprofile/', editprofile, name='editProfile'),
    path('editpassword/', editPassword, name='editPassword'),
    
]
