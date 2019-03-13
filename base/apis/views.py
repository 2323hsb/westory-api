from django.shortcuts import render
from django.http.response import HttpResponse
from django.core.serializers import serialize

from rest_framework import views, generics, mixins
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination

from .models import Post, User, Reply, Story, UploadImage
from .serializers import UserSerializer, PostSerializer, ReplySerializer, StorySerializer, ImageSerializer

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


class UploadImageAPI(generics.CreateAPIView):
    queryset = UploadImage.objects.all()
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        current_user = self.request.user
        if current_user:
            image = self.request.data['image']
            serializer.save(user=current_user, image=image)


class StoryAPI(generics.ListCreateAPIView):
    serializer_class = StorySerializer

    def get_queryset(self):
        if not 'hash_id' in self.request.query_params:
            stories = Story.objects.all().order_by('-created_date')
            return stories
        else:
            hash_id = self.request.query_params.get('hash_id')
            try:
                return Story.objects.filter(hash_id=hash_id)
            except Story.DoesNotExist:
                raise ValidationError("invaild story id")

    def perform_create(self, serializer):
        current_user = self.request.user
        if current_user:
            title = self.request.data['title']
            content = self.request.data['content']
            serializer.save(user=current_user, title=title, content=content)

class loveStoryAPI(views.APIView):
    serialzer_class = StorySerializer

    def get(self, request, *args, **kwargs):
        storyID = self.kwargs['hash_id']
        try:
            targetStory = Story.objects.get(hash_id=storyID)
            loversCount = targetStory.lovers.all().count()
            isLover = False
            if self.request.user in targetStory.lovers.all():
                isLover = True
            results = {}
            results['lovers_count'] = loversCount
            results['is_lover'] = isLover
            return Response(data=results)
        except Story.DoesNotExist:
            raise ValidationError('invaild story id')

    def post(self, request, *args, **kwargs):
        storyID = self.kwargs['hash_id']
        try:
            targetStory = Story.objects.get(hash_id=storyID)
            isLover = self.request.data['is_lover']
            if isLover == 'True':
                targetStory.lovers.add(self.request.user)
            else:
                targetStory.lovers.remove(self.request.user)
            targetStory.save()
        except Story.DoesNotExist:
            raise ValidationError("invaild story id")

        return Response(data="a")
