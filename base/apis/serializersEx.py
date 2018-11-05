# Examples
# from rest_framework import serializers
# from datetime import datetime


# class Comment(object):
#     def __init__(self, email, content, created=None):
#         self.email = email
#         self.content = content
#         self.created = created or datetime.now()


# comment = Comment(email='leila@example.com', content='foo bar')


# class CommentSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     content = serializers.CharField(max_length=200)
#     created = serializers.DateTimeField()

#     def create(self, validated_data):
#         return Comment(**validated_data)

#     def update(self, instance, validated_data):
#         instance.email = validated_data.get('email', instance.email)
#         instance.content = validated_data.get('content', instance.content)
#         instance.created = validated_data.get('created', instance.created)
#         return instance


# serializer = CommentSerializer(comment)
# serializer.data

# from rest_framework.renderers import JSONRenderer

# json = JSONRenderer().render(serializer.data)
# json

# import io
# from rest_framework.parsers import JSONParser

# stream = io.BytesIO(json)
# data = JSONParser().parse(stream)

# serializer = CommentSerializer(data=data)
# serializer.is_valid()
# serializer.validated_data
# comment = serializer.create()

from apis.serializers import PostSerializer
serializer = PostSerializer()
print(repr(serializer))