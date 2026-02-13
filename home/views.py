from django.http import HttpResponse, HttpRequest


def home_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("****** Wellcome to My Home Page! ******")


def about_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("****** About page ******")


def contact_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("****** Contact page ******")


def post_view(request: HttpRequest, id: int) -> HttpResponse:
    return HttpResponse(f"You are viewing a post from {id}")


def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    return HttpResponse(f"You are viewing the user profile: {username}")


def event_view(request: HttpRequest, year: int, month: int, day: int) -> HttpResponse:
    return HttpResponse(f"Date of view: {year}-{month}-{day}")
