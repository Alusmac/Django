from rest_framework import viewsets, permissions, filters
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Book objects
    """
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer

    filterset_fields = ['author', 'genre', 'publication_year']
    search_fields = ['title']

    def get_permissions(self) -> list:
        """Returns permission classes depending on the action
        """

        if self.action == 'destroy':
            return [permissions.IsAdminUser()]

        return [permissions.IsAuthenticated()]
