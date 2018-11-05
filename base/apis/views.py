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

    # 나중에 친구기능 추가하면 쓸거 같음
    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = PostSerializer(queryset, many=True)
    #     return Response(serializer.data)

# class NewPostAPI(generics.ListCreateAPIView):
#     serializer_class = PostSerializer
#     queryset = Post.objects.all().order_by('-created_date')
#     pagination_class = LimitOffsetPagination

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

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


# class AuthUserAPI(generics.GenericAPIView):
#     serializer_class = UserSerializer

#     def post(self, request, *args, **kwargs):
#         email = request.data['email']
#         password = request.data['password']

#         try:
#             user = User.objects.get(email=email, password=password)
#         except User.DoesNotExist:
#             return Response({'Error': 'Invalid User'}, status='400')

#         return Response({'Error': 'Not Ready Service'}, status='500')

    # def get(self, request, *args, **kargs):
    #     pass

    # def post(self, request, *args, **kargs):
    #     pass

# class CreatePostAPI(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
#     queryset = Post.objects.all().order_by('-created_date')[:5]
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kargs):
#         return self.list(request, *args, **kargs)

#     def post(self, request, *args, **kargs):
#         return self.create(request, *args, **kargs)

# class UploadImageAPI(generics.GenericAPIView, mixins.CreateModelMixin):
#     queryset = Image.objects.all()
#     serializer_class = ImageSerializer

#     def post(self, request, *args, **kargs):
#         return self.create(request, *args, **kargs)
