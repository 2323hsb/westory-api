from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.reverse import reverse
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import renderers


from .models import Post, Story, User, Reply, Comment, User
from .serializers import *

from rest_framework.parsers import JSONParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer


apis_renderer = (BrowsableAPIRenderer, JSONRenderer, )


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class ApiRoot(views.APIView):
    permission_classes = (IsAuthenticated | ReadOnly,)

    def get(self, request, format=None):
        return Response({
            'users': reverse('user-list', request=request, format=format),
            'stories': reverse('story-list', request=request, format=format)
        })


# class UserAPI(generics.ListAPIView):
#     serializer_class = UserSerializer

#     def get_queryset(self):
#         current_user = self.request.user
#         if current_user:
#             user = User.objects.filter(email=current_user)
#         return user


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-created_date')
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated | ReadOnly,)


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by('-created_date')
    serializer_class = StorySerializer
    permission_classes = (IsAuthenticated | ReadOnly,)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def comment(self, request, *args, **kwargs):
        story = self.get_object()
        return Response('hi')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

# class StoryList(generics.ListCreateAPIView):
#     # renderer_classes = apis_renderer
#     # serializer_class = StorySerializer
#     # permission_classes = (IsAuthenticated | ReadOnly,)
#     queryset = Story.objects.all().order_by('-created_date')
#     # lookup_field = "hash_id"

#     # def get(self, request, *args, **kwargs):
#     #     return self.list(request, *args, **kwargs)


#     permission_classes = (IsAuthenticated | ReadOnly,)
#     def get(self, request, format=None):
#         return Response({
#             'stories': reverse('story-detail', 'hash', request=request, format=format)
#         })

# class StoryDetail(generics.RetrieveUpdateDestroyAPIView):
#     renderer_classes = apis_renderer
#     queryset = Story.objects.all()
#     serializer_class = StorySerializer
#     lookup_field = "hash_id"

#     def get_queryset(self):
#         queryset = Story.objects.all().order_by('-created_date')
#         story_id = self.kwargs.get('hash_id')
#         if story_id is not None:
#             queryset = queryset.filter(hash_id=story_id)
#             queryset.update(view_count=queryset[0].view_count+1)
#         return queryset

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# class StoryAPI(generics.ListCreateAPIView):
#     renderer_classes = apis_renderer
#     serializer_class = StorySerializer
#     permission_classes = (IsAuthenticated | ReadOnly,)

#     def get_queryset(self):
#         print(self.request.user)
#         queryset = Story.objects.all().order_by('-created_date')
#         story_id = self.kwargs.get('hash_id')
#         if story_id is not None:
#             queryset = queryset.filter(hash_id=story_id)
#             queryset.update(view_count=queryset[0].view_count+1)
#         return queryset

#     def post(self, request, *args, **kwargs):
#         last_path = get_last_url_path(request.get_full_path())
#         if last_path == "love":
#             try:
#                 target = Story.objects.get(hash_id=self.kwargs['hash_id'])
#                 user_is_lover = request.user in target.lovers.all()
#                 if user_is_lover:
#                     target.lovers.remove(self.request.user)
#                 else:
#                     target.lovers.add(self.request.user)
#                 target.save()
#                 return Response(data={
#                     'user_is_lover': request.user in target.lovers.all(),
#                     'lovers_count': target.lovers.all().count()
#                 })
#             except Story.DoesNotExist:
#                 raise ValidationError("invaild story id")
#         return super().post(request, *args, **kwargs)

#     def perform_create(self, serializer):
#         current_user = self.request.user
#         if current_user:
#             title = self.request.data['title']
#             content = self.request.data['content']
#             serializer.save(user=current_user, title=title, content=content)


# class CommentAPI(generics.ListCreateAPIView):
#     serializer_class = CommentSerializer

#     def get_queryset(self):
#         storyID = self.kwargs['hash_id']
#         return Comment.objects.filter(story=storyID).order_by('-created_date')

#     def perform_create(self, serializer):
#         storyID = self.kwargs['hash_id']
#         try:
#             target_story = Story.objects.get(hash_id=storyID)
#             serializer.save(user=self.request.user, story=target_story)
#         except Story.DoesNotExist:
#             raise ValidationError("invaild Story id")


def get_last_url_path(fullpath):
    split_path = fullpath.split("/")
    return split_path[-1]
