from django.contrib import admin
from django.urls import path, include
from .views import UserAPI, PostAPI

urlpatterns = [
    path('user', UserAPI.as_view()),
    path('posts', PostAPI.as_view()),
    # path('authUser', AuthUserAPI.as_view()),
    # path('createPost', CreatePostAPI.as_view()),
    # path('uploadImage', UploadImageAPI.as_view()),
]
