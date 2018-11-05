from django.contrib import admin
from django.urls import path, include
from .views import UserAPI, PostAPI, ReplyAPI
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('user', UserAPI.as_view()),
    # path('new_post', NewPostAPI.as_view()),
    # path('public-user', PublicUserAPI.as_view()),
    path('post', PostAPI.as_view()),
    path('reply', ReplyAPI.as_view()),
    # path('authUser', AuthUserAPI.as_view()),
    # path('createPost', CreatePostAPI.as_view()),
    # path('uploadImage', UploadImageAPI.as_view()),
]
