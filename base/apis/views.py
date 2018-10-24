from django.shortcuts import render
from django.http.response import HttpResponse
from django.core.serializers import serialize

from rest_framework import views, generics, mixins
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Post, User
from .serializers import UserSerializer, PostSerializer

from google.oauth2 import id_token
from google.auth.transport import requests

CLIENT_ID = '877944658856-1tr4gmmtc8nm4ur7m1p3jv2e9omm8fo3.apps.googleusercontent.com'


class UserAPI(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        access_token = self.request.query_params.get('access_token')
        user = User.objects.filter(auth_token=access_token)
        return user

class PostAPI(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        access_token = self.request.query_params.get('access_token')
        try:
            user = User.objects.get(auth_token=access_token)
            post = Post.objects.filter(user=user)
            return post
        except User.DoesNotExist:
            return []

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)


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
