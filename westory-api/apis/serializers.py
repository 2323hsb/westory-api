from rest_framework import serializers
from .models import User, Post, Reply, Story, UploadImage, Comment
from hashid_field.rest import HashidSerializerCharField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'profile_img', 'last_login']


class PostSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField()
    user_profile_img = serializers.ReadOnlyField()
    replies_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_replies_count(self, obj):
        return obj.replys.count()

    def get_likes_count(self, obj):
        return obj.like_users.count()

    class Meta:
        model = Post
        fields = ['user_username', 'user_profile_img', 'id',
                  'content', 'created_date', 'replies_count', 'likes_count']


class ReplySerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField()
    user_profile_img = serializers.ReadOnlyField()

    class Meta:
        model = Reply
        fields = ['user_username', 'user_profile_img',
                  'content', 'created_date']

class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField()
    user_profile_img = serializers.ReadOnlyField()
    class Meta:
        model = Comment
        fields = ['user_username', 'user_profile_img',
                  'content', 'created_date']


class StorySerializer(serializers.ModelSerializer):
    hash_id = serializers.PrimaryKeyRelatedField(pk_field=HashidSerializerCharField(
        source_field='apis.Story.hash_id'), read_only=True)
    user_username = serializers.ReadOnlyField()
    user_profile_img = serializers.ReadOnlyField()
    lovers_count = serializers.SerializerMethodField()
    is_lover = serializers.SerializerMethodField()

    def get_lovers_count(self, obj):
        return obj.lovers.count()

    def get_is_lover(self, obj):
        isLover = False
        if self.context['request'].user in obj.lovers.all():
            isLover = True
        return isLover

    class Meta:
        model = Story
        fields = ['hash_id', 'user_username', 'user_profile_img',
                  'title', 'content', 'created_date', 'lovers_count', 'is_lover', 'view_count']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImage
        fields = ['image']
