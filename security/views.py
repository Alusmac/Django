from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.db import connection
from django.contrib.auth import get_user_model


def register_view(request: HttpRequest) -> HttpResponse:
    """User registration"""

    if request.method == "POST":
        form: RegisterForm = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect("/dashboard/")
    else:
        form = RegisterForm()
    return render(request, "security/register.html", {"form": form}, )


class CustomLoginView(LoginView):
    """class login view when user logs and have success or failed
    """
    template_name: str = "security/login.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form) -> HttpResponse:
        """Called when authentication is successful
        """
        print("LOGIN SUCCESS ✅")
        return super().form_valid(form)

    def form_invalid(self, form) -> HttpResponse:
        """Called when authentication fails
        """
        print("LOGIN FAILED ❌")
        print(form.errors)
        return super().form_invalid(form)


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Protected dashboard view
    Accessible only to authenticated users
    """
    return render(request, "security/dashboard.html", )


def logout_view(request: HttpRequest) -> HttpResponse:
    """Logout the current user
    Redirects to login page
    """
    logout(request)
    return redirect("/login/")


def safe_sql_example(request: HttpRequest) -> HttpResponse:
    """safe SQL execution using parameterized queries.
    """

    username = request.GET.get("username", "")
    result = []

    User = get_user_model()
    table_name = User._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT username FROM {table_name} WHERE username = %s",
            [username],
        )
        result = cursor.fetchall()

    return render(
        request,
        "security/sql_example.html",
        {
            "username": username,
            "result": result,
        },
    )
