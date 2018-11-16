from django.contrib import admin
from django.urls import path, include
from .views import UserAPI, PostAPI, ReplyAPI, LikesAPI
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('user', UserAPI.as_view()),
    path('likes', LikesAPI.as_view()),
    path('post', PostAPI.as_view()),
    path('reply', ReplyAPI.as_view()),
]
