from rest_framework import serializers
from .models import User, Post, Reply

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'profile_img', 'last_login']

class PostSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField()
    user_profile_img = serializers.ReadOnlyField()
    replies_count = serializers.SerializerMethodField()

    def get_replies_count(self, obj):
        return obj.replys.count()

    class Meta:
        model = Post
        fields = ['user_username', 'user_profile_img', 'id' ,'content', 'created_date', 'replies_count']

class ReplySerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField()
    user_profile_img = serializers.ReadOnlyField()
    class Meta:
        model = Reply
        fields = ['user_username', 'user_profile_img', 'content', 'created_date']