from django.http import HttpResponse, HttpRequest


def home_view(request: HttpRequest) -> HttpResponse:
    """Return a simple welcome message for the home page
    """
    return HttpResponse("****** Wellcome to My Home Page! ******")


def about_view(request: HttpRequest) -> HttpResponse:
    """Return a basic response for the about page
    """
    return HttpResponse("****** About page ******")


def contact_view(request: HttpRequest) -> HttpResponse:
    """Return a basic response for the contact page
    """
    return HttpResponse("****** Contact page ******")


def post_view(request: HttpRequest, id: int) -> HttpResponse:
    """Display a specific post by its ID
    """
    return HttpResponse(f"You are viewing a post from {id}")


def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    """Display a user profile by username
    """
    return HttpResponse(f"You are viewing the user profile: {username}")


def event_view(request: HttpRequest, year: int, month: int, day: int) -> HttpResponse:
    """Display an event page based on a specific date
    """
    return HttpResponse(f"Date of view: {year}-{month}-{day}")
