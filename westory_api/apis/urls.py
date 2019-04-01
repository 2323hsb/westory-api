from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('user', UserAPI.as_view()),
    path('likes', LikesAPI.as_view()),
    path('post', PostAPI.as_view()),
    path('reply', ReplyAPI.as_view()),

    path('story', StoryAPI.as_view()),
    path('story/<str:hash_id>', StoryAPI.as_view()),
    path('story/<str:hash_id>/love', StoryAPI.as_view()),
    
    # path('story/<str:hash_id>/comment', CommentAPI.as_view()),
    path('uploadImage', UploadImageAPI.as_view()),
]