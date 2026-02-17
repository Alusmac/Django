from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from datetime import datetime


def home(request: HttpRequest) -> HttpResponse:
    context = {
        "title": "Home Page",
        "welcome_text": "Welcome to our website!",
    }
    return render(request, "main/home.html", context)


def about(request: HttpRequest) -> HttpResponse:
    context = {
        "title": "About Us",
        "company_name": "My Company",
        "description": "We are a company that provides quality services to customers around the world.",
        "updated": datetime.now(),
        "is_active": True,
    }
    return render(request, "main/about.html", context)


class ContactView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "title": "Contacts",
            "address": "Kherson, 135 I.Kulika Street",
            "phone": "+380552501000",
            "email": "info@company.com",
        }
        return render(request, "main/contact.html", context)


class ServiceView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        services = [
            {"name": "Web development", "description": "Create web sites.", "category": "IT"},
            {"name": "SEO optimization", "description": "Website promotion in search engines.", "category": "Marketing"},
            {"name": "Analyze", "description": "Consultation and Audit.", "category": "Business"},
            {"name": "UI/UX design", "description": "Design.", "category": "IT"},
        ]

        query = request.GET.get("q", "").strip()

        filtered_services = services

        if query:
            filtered_services = [
                s for s in services
                if query.lower() in s["name"].lower()
                or query.lower() in s["description"].lower()
            ]

        context = {
            "title": "Services",
            "services": filtered_services,
            "query": query,
            "categories": list({s["category"] for s in services}),
            "selected_category": "",
        }

        return render(request, "main/service.html", context)


# Create your views here.
