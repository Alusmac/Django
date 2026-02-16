from datetime import datetime
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


def home(request: HttpRequest) -> HttpResponse:
    context = {
        "title": "Home Page",
        "welcome_text": "Welcome to Our Site ",
    }
    return render(request, "main/home.html", context)


def about(request: HttpRequest) -> HttpResponse:
    context = {
        "title": "About Us",
        "company_name": "My Company",
        "description": "Welcome to Our Site from Testing Django",
        "updated": datetime.now(),
        "is_active": True,
    }
    return render(request, "main/about.html", context)


class ContactView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "title": "Contacts",
            "address": "Kherson , I.Kylika street 135",
            "phone": "+380551000000",
            "email": "info@company.com",
        }
        return render(request, "main/contact.html", context)


class ServiceView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        service = [
            {"name": "Web development", "description": "Creation websites.", "category": "IT"},
            {"name": "Optimization", "description": "Website promotion in search systems.", "category": "Marketing"},
            {"name": "Consulting", "description": "Business consulting.", "category": "Business"},
            {"name": "UI/UX Design", "description": "Interface design.", "category": "IT"},
        ]

        context = {
            "title": "Services",
            "services": service,
            "updated": datetime.now(),

        }

        return render(request, "main/service.html", context)
