# from django.contrib import admin
# from django.urls import path, include

from .views import *

# from rest_framework.urlpatterns import format_suffix_patterns

# story_list = StoryViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# story_detail = StoryViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })

# urlpatterns = format_suffix_patterns([
#     # api root
#     path('', ApiRoot.as_view()),

    # path('user', UserAPI.as_view()),
    # path('likes', LikesAPI.as_view()),
    # path('post', PostAPI.as_view()),
    # path('reply', ReplyAPI.as_view()),

    # path('story/', StoryAPI.as_view(), name='story-api'),
    # path('story/<str:hash_id>/', StoryAPI.as_view(), name='story-detail'),

    # path('stories/', story_list, name='story-list'),
    # path('stories/<str:hash_id>/', story_detail, name='story-detail'),
    
    # path('story/<str:hash_id>/love', StoryAPI.as_view()),
    
    # path('story/<str:hash_id>/comment/', CommentAPI.as_view(), name='story-comment'),
    # path('uploadImage', UploadImageAPI.as_view()),
# ])

from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'stories', StoryViewSet)
router.register(r'user', UserViewSet)
# router.register(r'comment', CommentViewSet)

urlpatterns = [
    path('', ApiRoot.as_view()),
    path('', include(router.urls)),
]