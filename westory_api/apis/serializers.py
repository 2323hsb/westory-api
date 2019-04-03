from rest_framework import serializers
from .models import User, Post, Reply, Story, UploadImage, Comment
from hashid_field.rest import HashidSerializerCharField


class UserSerializer(serializers.HyperlinkedModelSerializer):
    stories = serializers.HyperlinkedRelatedField(
        many=True, view_name='story-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'email', 'username',
                  'profile_img', 'last_login', 'stories']


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


class StorySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        many=False, view_name='user-detail', read_only=True)
    lovers_count = serializers.SerializerMethodField()
    user_is_lover = serializers.SerializerMethodField()
    # comments = serializers.HyperlinkedRelatedField(
    #     many=True, view_name='comment-detail', read_only=True)
    comments = serializers.HyperlinkedIdentityField(view_name='story-comment')

    def get_lovers_count(self, obj):
        return obj.lovers.count()

    def get_user_is_lover(self, obj):
        return self.context['request'].user in obj.lovers.all()

    class Meta:
        model = Story
        fields = ('url', 'user', 'title', 'content',
                  'created_date', 'view_count', 'lovers_count', 'user_is_lover', 'comments')
        # fields = ('url', 'hash_id', 'title', 'content', 'created_date', 'view_count')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        many=False, view_name='user-detail', read_only=True)
    story = serializers.HyperlinkedRelatedField(
        many=False, view_name='story-detail', read_only=True)

    class Meta:
        model = Comment
        fields = ['url', 'user', 'story', 'created_date', 'content', ]

# class StorySerializer(serializers.HyperlinkedModelSerializer):
    # hash_id = serializers.PrimaryKeyRelatedField(pk_field=HashidSerializerCharField(
    #     source_field='apis.Story.hash_id'), read_only=True)
    # url = serializers.HyperlinkedIdentityField(view_name='story-detail', format='html')
    # user_username = serializers.ReadOnlyField()
    # user_profile_img = serializers.ReadOnlyField()
    # lovers_count = serializers.SerializerMethodField()
    # user_is_lover = serializers.SerializerMethodField()

    # def get_lovers_count(self, obj):
    #     return obj.lovers.count()

    # def get_user_is_lover(self, obj):
    #     return self.context['request'].user in obj.lovers.all()

    # class Meta:
    #     model = Story
    #     fields = ('url', 'user',
    #               'title', 'content', 'created_date', 'view_count')
        # fields = ('url', 'hash_id', 'title', 'content', 'created_date', 'view_count')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImage
        fields = ['image']
