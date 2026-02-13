from django.http import HttpResponse

def home_view(request):
    return HttpResponse("****** Wellcome to My Home Page! ******")

def about_view(request):
    return HttpResponse("****** About page ******")

def contact_view(request):
    return HttpResponse("****** Contact page ******")

def post_view(request, id):
    return HttpResponse(f"You are viewing a post from {id}")
def profile_view(request, username):
    return HttpResponse(f"You are viewing the user profile: {username}")

def event_view(request, year, month, day):
    return HttpResponse(f"Date of view: {year}-{month}-{day}")
