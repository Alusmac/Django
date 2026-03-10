from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model
    """

    class Meta:
        model = Comment
        fields = ["id", "text", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model including nested comments
    """

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "created_at",
            "comments"
        ]
