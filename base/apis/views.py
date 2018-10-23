from django.shortcuts import render
from django.http.response import HttpResponse

from rest_framework import views, generics, mixins
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Post, User
from .serializers import PostSerializer

from google.oauth2 import id_token
from google.auth.transport import requests

CLIENT_ID = '877944658856-1tr4gmmtc8nm4ur7m1p3jv2e9omm8fo3.apps.googleusercontent.com'

class UserAPI(views.APIView):
    def post(self, request):
        access_token = request.data['access_token']
        if access_token:
            try:
                User.objects.get(auth_token=access_token)
                print('good')
            except User.DoesNotExist:
                print('bad')
        return Response('on develop')

class PostAPI(generics.GenericAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        request_id_token = self.request.query_params.get('id_token')
        auth_user = getUserByToken(request_id_token)

        if auth_user is not None:
            queryset = Post.objects.filter(user=auth_user)
            return queryset

        else:
            return Response('invalid token')

def getUserByToken(request_id_token):
    try:
        idinfo = id_token.verify_oauth2_token(request_id_token, requests.Request(), CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return None

        try:
            return User.objects.get(password=idinfo['sub'])
        except OAuthUser.DoesNotExist:
            return None

    except ValueError:
        return None


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
