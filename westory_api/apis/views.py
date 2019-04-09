from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.reverse import reverse
from rest_framework.decorators import action, detail_route
from rest_framework import viewsets
from rest_framework import status, renderers


from .models import Post, Story, User, Reply, Comment, User
from .serializers import *

from rest_framework.parsers import JSONParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer


apis_renderer = (BrowsableAPIRenderer, JSONRenderer, )


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class StoryPagenation(LimitOffsetPagination):
    default_limit = 10


class ApiRoot(views.APIView):
    permission_classes = (IsAuthenticated | ReadOnly,)

    def get(self, request, format=None):
        return Response({
            'users': reverse('user-list', request=request, format=format),
            'stories': reverse('story-list', request=request, format=format),
            'comments': reverse('comment-list', request=request, format=format)
        })


# class UserAPI(generics.ListAPIView):
#     serializer_class = UserSerializer

#     def get_queryset(self):
#         current_user = self.request.user
#         if current_user:
#             user = User.objects.filter(email=current_user)
#         return user


# class PostAPI(generics.ListCreateAPIView):
#     serializer_class = PostSerializer
#     queryset = Post.objects.all().order_by('-created_date')
#     pagination_class = LimitOffsetPagination

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# class LikesAPI(views.APIView):
#     def get(self, request, *args, **kwargs):
#         if not 'post_id' in self.request.query_params:
#             like_post_list = self.request.user.like_posts.all()
#             results = []
#             for like_post in like_post_list:
#                 results.append(like_post.pk)

#             return Response(data=results)
#         else:
#             post_id = self.request.query_params.get('post_id')
#             try:
#                 target_post = Post.objects.get(id=post_id)
#                 like_count = target_post.like_users.all().count()
#                 is_like = False
#                 if self.request.user in target_post.like_users.all():
#                     is_like = True
#                 results = {}
#                 results['like_count'] = like_count
#                 results['is_like'] = is_like
#                 return Response(data=results)
#             except Post.DoesNotExist:
#                 raise ValidationError("invaild post id")

#     def post(self, request, *args, **kwargs):
#         if not 'post_id' in self.request.data:
#             raise ValidationError("You need 'post_id'")
#         post_id = self.request.data['post_id']
#         try:
#             target_post = Post.objects.get(id=post_id)
#             is_like = self.request.data['is_like']
#             if is_like == 'true':
#                 target_post.like_users.add(self.request.user)
#             else:
#                 target_post.like_users.remove(self.request.user)
#             target_post.save()
#         except Post.DoesNotExist:
#             raise ValidationError("invaild post id")

#         return Response(data="a")


# class ReplyAPI(generics.ListCreateAPIView):
#     serializer_class = ReplySerializer

#     def get_queryset(self):
#         post_id = self.request.query_params.get('post_id')
#         return Reply.objects.filter(post=post_id)

#     def perform_create(self, serializer):
#         if not 'post_id' in self.request.data:
#             raise ValidationError("You need 'post_id'")
#         post_id = self.request.data['post_id']
#         try:
#             target_post = Post.objects.get(id=post_id)
#             serializer.save(user=self.request.user, post=target_post)
#         except Post.DoesNotExist:
#             raise ValidationError("invaild post id")


class UploadImageAPI(generics.CreateAPIView):
    queryset = UploadImage.objects.all()
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        current_user = self.request.user
        if current_user:
            image = self.request.data['image']
            serializer.save(user=current_user, image=image)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated | ReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by('-created_date')
    serializer_class = StorySerializer
    permission_classes = (IsAuthenticated | ReadOnly,)
    pagination_class = StoryPagenation

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     # print(queryset.count())

    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         print(serializer.data)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        story = self.get_object()
        story.view_count += 1
        story.save()
        return super().retrieve(request, *args, **kwargs)

    @detail_route(methods=['post'])
    def love_story(self, request, pk=None):
        serializer_class = None

        try:
            target = self.get_object()
            user_is_lover = request.user in target.lovers.all()
            if user_is_lover:
                target.lovers.remove(self.request.user)
            else:
                target.lovers.add(self.request.user)
            target.save()
            return Response(data={
                'status': 'love story sucesss',
                'user_is_lover': request.user in target.lovers.all(),
                'lovers_count': target.lovers.all().count()
            })
        except Story.DoesNotExist:
            raise ValidationError("invaild story id")

    @detail_route(methods=['post'])
    def add_comment(self, request, pk=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, story=self.get_object())
            return Response(data={
                'status': 'add comment success',
            })
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated | ReadOnly,)