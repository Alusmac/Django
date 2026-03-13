from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("greet/", views.greet_view, name="greet"),
    path("logout/", views.logout_view, name="logout"),

    path("books/", views.book_list, name="book_list"),
    path("task/<task_id>/", views.task_status_view, name="task_status"),

    path("author-book-stats/", views.author_book_stats, name="author_book_stats"),
    path("raw-sql/", views.authors_with_popular_books, name="authors_with_popular_books"),
    path("compare-db/", views.compare_db_performance, name="compare_db_performance"),

    path("import-books/", views.import_books_view, name="import_books"),
]