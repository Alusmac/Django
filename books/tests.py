import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from books.models import Book


@pytest.mark.django_db
def test_book_workflow_without_fixtures() -> None:
    """Test1: creating a client, user, book, and checking the list
    """

    client = APIClient()
    user = User.objects.create_user(username='tester', password='password123')
    client.force_authenticate(user=user)

    Book.objects.create(
        title="1984",
        author="George Orwell",
        genre="Dystopia",
        publication_year=1949
    )

    response = client.get('/api/books/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == "1984"


@pytest.mark.django_db
def test_filter_by_year_explicit() -> None:
    """Test 2: Filtering: create two workbooks and search for one specific one
    """
    client = APIClient()
    user = User.objects.create_user(username='filter_user', password='password123')
    client.force_authenticate(user=user)

    Book.objects.create(title="Old", author="A", genre="G", publication_year=1900)
    Book.objects.create(title="New", author="B", genre="G", publication_year=2024)

    response = client.get('/api/books/', {'publication_year': 2024})

    assert len(response.data['results']) == 1
    assert response.data['results'][0]['title'] == "New"


@pytest.mark.django_db
def test_delete_permissions_explicit() -> None:
    """Test 3: Access rights: regular user vs. admin
    """

    book = Book.objects.create(title="To be deleted", author="A", genre="G", publication_year=2000)
    url = f'/api/books/{book.id}/'

    client_user = APIClient()
    regular_user = User.objects.create_user(username='regular', password='password123')
    client_user.force_authenticate(user=regular_user)

    response_user = client_user.delete(url)
    assert response_user.status_code == status.HTTP_403_FORBIDDEN

    client_admin = APIClient()
    admin_user = User.objects.create_superuser(username='admin_boss', password='password123')
    client_admin.force_authenticate(user=admin_user)

    response_admin = client_admin.delete(url)
    assert response_admin.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_retrieve_single_book() -> None:
    """Test 4: Checking the receipt of data for one specific book by ID
    """
    client = APIClient()
    user = User.objects.create_user(username='reader_user', password='password123')
    client.force_authenticate(user=user)

    book = Book.objects.create(title="The Hobbit", author="Tolkien", genre="Fantasy", publication_year=1937)

    url = f'/api/books/{book.id}/'
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == "The Hobbit"


@pytest.mark.django_db
def test_api_unauthorized_access() -> None:
    """Test 5: Verify that an anonymous user CANNOT obtain a list of books
    """
    client = APIClient()

    response = client.get('/api/books/')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_search_by_title_partial() -> None:
    """Test 6: Checking the search by part of the book title
    """
    client = APIClient()
    user = User.objects.create_user(username='searcher', password='password123')
    client.force_authenticate(user=user)

    Book.objects.create(title="Django for Beginners", author="W.S.", genre="Tech", publication_year=2020)
    Book.objects.create(title="Python Tips", author="W.S.", genre="Tech", publication_year=2021)

    response = client.get('/api/books/', {'search': 'Django'})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert "Django" in response.data['results'][0]['title']
