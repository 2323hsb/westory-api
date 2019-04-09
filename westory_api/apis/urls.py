from .views import *

from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'stories', StoryViewSet)
router.register(r'user', UserViewSet)
router.register(r'comment', CommentViewSet)

urlpatterns = [
    path('', ApiRoot.as_view()),
    path('', include(router.urls)),
    path('uploadImage', UploadImageAPI.as_view()),
]