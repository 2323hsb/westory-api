from django.shortcuts import render
from django.http.response import HttpResponse
from django.core.serializers import serialize

from rest_framework import views, generics, mixins
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination

from .models import Post, User, Reply
from .serializers import UserSerializer, PostSerializer, ReplySerializer

from google.oauth2 import id_token
from google.auth.transport import requests

CLIENT_ID = '877944658856-1tr4gmmtc8nm4ur7m1p3jv2e9omm8fo3.apps.googleusercontent.com'

class UserAPI(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        current_user = self.request.user
        if current_user:
            user = User.objects.filter(email=current_user)
        return user


class PostAPI(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-created_date')
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikesAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        if not 'post_id' in self.request.query_params:
            like_post_list = self.request.user.like_posts.all()
            results = []
            for like_post in like_post_list:
                results.append(like_post.pk)
            
            return Response(data=results)
        else:
            post_id = self.request.query_params.get('post_id')
            try:
                target_post = Post.objects.get(id=post_id)
                like_count = target_post.like_users.all().count()
                is_like = False
                if self.request.user in target_post.like_users.all():
                    is_like = True
                results = {}
                results['like_count'] = like_count
                results['is_like'] = is_like
                return Response(data=results)
            except Post.DoesNotExist:
                raise ValidationError("invaild post id")

    def post(self, request, *args, **kwargs):
        if not 'post_id' in self.request.data:
            raise ValidationError("You need 'post_id'")
        post_id = self.request.data['post_id']
        try:
            target_post = Post.objects.get(id=post_id)
            is_like = self.request.data['is_like']
            if is_like == 'true':
                target_post.like_users.add(self.request.user)
            else:
                target_post.like_users.remove(self.request.user)
            target_post.save()
        except Post.DoesNotExist:
            raise ValidationError("invaild post id")

        return Response(data="a")

class ReplyAPI(generics.ListCreateAPIView):
    serializer_class = ReplySerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        return Reply.objects.filter(post=post_id)

    def perform_create(self, serializer):
        if not 'post_id' in self.request.data:
            raise ValidationError("You need 'post_id'")
        post_id = self.request.data['post_id']
        try:
            target_post = Post.objects.get(id=post_id)
            serializer.save(user=self.request.user, post=target_post)
        except Post.DoesNotExist:
            raise ValidationError("invaild post id")

# class UploadImageAPI(generics.GenericAPIView, mixins.CreateModelMixin):
#     queryset = Image.objects.all()
#     serializer_class = ImageSerializer

#     def post(self, request, *args, **kargs):
#         return self.create(request, *args, **kargs)
