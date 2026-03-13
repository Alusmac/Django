from djongo import models


class Author(models.Model):
    """Represents an author in the relational database
    """
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    """Represents a book in the relational database
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    publication_year = models.IntegerField()

    def __str__(self) -> str:
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['publication_year']),
        ]


class Review(models.Model):
    """Represents a review of a book
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    rating = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['rating']),
        ]


class BookMongo(models.Model):
    """Represents a book stored in MongoDB (NoSQL)
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return self.title
