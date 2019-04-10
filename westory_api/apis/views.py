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


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by('-created_date')
    serializer_class = StorySerializer
    permission_classes = (IsAuthenticated | ReadOnly,)
    pagination_class = StoryPagenation

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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

    @detail_route(methods=['get'])
    def comments(self, request, pk=None):
        story = self.get_object()
        comments = story.comments.all().order_by('-created_date')
        serializer = CommentSerializer(
            comments, context={'request': request}, many=True)
        return Response(serializer.data)

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
