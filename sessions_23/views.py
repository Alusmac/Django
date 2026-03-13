from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.core.cache import cache
from .models import Book, Author
from .tasks import import_books_from_csv
from celery.result import AsyncResult
from django.db.models import Avg, Count
from sessions_23.models import BookMongo
from django.db import connection
import time
from django.conf import settings
import os


def login_view(request: HttpRequest) -> HttpResponse:
    """Handles user login, sets cookies and session data
    """
    request.session.set_test_cookie()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if not request.session.test_cookie_worked():
            return render(request, "sessions_23/login.html", {"form": form, "error": "Cookies off"})

        request.session.delete_test_cookie()

        if form.is_valid():
            name = form.cleaned_data["name"]
            age = form.cleaned_data["age"]

            response = redirect("greet")

            response.set_cookie("username", name, max_age=3600)
            request.session["age"] = age

            return response
    else:
        form = LoginForm()

    return render(request, "sessions_23/login.html", {"form": form})


def greet_view(request: HttpRequest) -> HttpResponse:
    """Greets the user using session and cookie data
    """
    name = request.COOKIES.get("username")
    age = request.session.get("age")

    if not name or not age:
        return redirect("login")

    response = render(
        request,
        "sessions_23/greet.html",
        {"name": name, "age": age}
    )
    response.set_cookie("username", name, max_age=3600)
    return response


def logout_view(request: HttpRequest) -> HttpResponse:
    """Logs out the user by deleting cookies and clearing session
    """
    response = redirect("login")
    response.delete_cookie("username")
    request.session.flush()
    return response


def book_list(request: HttpRequest) -> HttpResponse:
    """Displays a cached list of books for improved performance
    """
    books = cache.get("books_list")

    if not books:
        books = Book.objects.select_related("author").prefetch_related("reviews")
        cache.set("books_list", books, 60 * 5)

    return render(request, "sessions_23/book_list.html", {"books": books})


def add_book(request: HttpRequest) -> None:
    """Creates a new empty book  and clears the cache
    """
    book = Book.objects.create()
    cache.delete("books_list")


def book_list_optimized(request: HttpRequest) -> HttpResponse:
    """ORM optimization
    """
    books = cache.get("books_list")
    if not books:
        books = Book.objects.select_related("author").prefetch_related("reviews")
        cache.set("books_list", books, 60 * 5)
    return render(request, "sessions_23/book_list.html", {"books": books})


def import_books_view(request: HttpRequest) -> HttpResponse:
    """ Starts a Celery task to import books from a CSV file
    """

    if request.method == "POST":
        file_path = os.path.join(settings.BASE_DIR, 'sessions_23', 'books.csv')
        user_email = request.POST.get("email")

        task = import_books_from_csv.delay(file_path, user_email)

        return redirect("task_status", task_id=task.id)

    return render(request, "sessions_23/import_form.html")


def task_status_view(request: HttpRequest, task_id: str) -> HttpResponse:
    """Checks the status of a Celery task
    """
    task_result = AsyncResult(task_id)
    context = {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None
    }
    return render(request, "sessions_23/task_status.html", context)


def author_book_stats(request: HttpRequest) -> HttpResponse:
    """Displays authors with their average book rating and books with review
    """

    authors = Author.objects.annotate(
        avg_rating=Avg('book__reviews__rating')
    )

    books = Book.objects.annotate(
        review_count=Count('reviews'),
        avg_rating=Avg('reviews__rating')
    ).order_by('-review_count', '-avg_rating')  # сортування

    return render(request, "sessions_23/author_book_stats.html", {
        "authors": authors,
        "books": books
    })


def authors_with_popular_books(request: HttpRequest) -> HttpResponse:
    """Uses raw SQL to find authors with books having more than 10 reviews
    """
    min_reviews = 10

    with connection.cursor() as cursor:
        cursor.execute("""
                       SELECT a.id, a.name, COUNT(r.id) as total_reviews
                       FROM sessions_23_author a
                                JOIN sessions_23_book b ON b.author_id = a.id
                                JOIN sessions_23_review r ON r.book_id = b.id
                       GROUP BY a.id, a.name
                       HAVING COUNT(r.id) > %s
                       """, [min_reviews])
        authors = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM sessions_23_book")
        total_books = cursor.fetchone()[0]

    for q in connection.queries:
        print(q['sql'])

    return render(request, "sessions_23/raw_sql.html", {
        "authors": authors,
        "total_books": total_books
    })


book = BookMongo.objects.create(title="Mongo Book 1", author="Author Mongo", publication_year=2023)

books = BookMongo.objects.all()
for b in books:
    print(b.title, b.author, b.publication_year)


def compare_db_performance(request: HttpRequest) -> HttpResponse:
    """Compares performance between relational DB and MongoDB
    """
    # ⬇︎⬇︎⬇︎⬇︎⬇︎ Реляційна база ⬇︎⬇︎⬇︎⬇︎⬇︎
    start_rel = time.time()
    books_rel = list(Book.objects.all())
    end_rel = time.time()
    time_rel = end_rel - start_rel

    # ⬇︎⬇︎⬇︎⬇︎⬇︎ MongoDB ⬇︎⬇︎⬇︎⬇︎⬇︎
    start_mongo = time.time()
    books_nosql = list(BookMongo.objects.all())
    end_mongo = time.time()
    time_mongo = end_mongo - start_mongo

    context = {
        "books_rel": books_rel,
        "books_nosql": books_nosql,
        "time_rel": round(time_rel, 4),
        "time_mongo": round(time_mongo, 4),
    }
    return render(request, "sessions_23/compare_db.html", context)
