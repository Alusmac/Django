import csv
from celery import shared_task
from django.core.mail import send_mail
from .models import Author, Book


@shared_task
def import_books_from_csv(file_path: str, user_email: str) -> str:
    """Celery task to import books from a CSV file and notify the user via email
    """
    created_count = 0
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            author, _ = Author.objects.get_or_create(name=row['author'])
            Book.objects.create(
                title=row['title'],
                author=author,
                publication_year=int(row['publication_year'])
            )
            created_count += 1

    send_mail(
        subject="Імпорт книг завершено",
        message=f"Було імпортовано {created_count} книг.",
        from_email="no-reply@example.com",
        recipient_list=[user_email],
    )

    return f"{created_count} books imported"
