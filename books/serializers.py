from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model
    """

    class Meta:
        model = Book

        fields = [
            'id',
            'title',
            'author',
            'genre',
            'publication_year',
            'created_at'
        ]

        read_only_fields = ['id', 'created_at']
