from rest_framework import serializers

# from .models import User, Post, Image
from .models import User, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['email', 'username', 'last_login']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields= '__all__'

# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Image
#         fields= '__all__'