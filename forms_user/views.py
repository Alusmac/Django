from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistrationForm, UserProfileForm, CustomPasswordChangeForm
from .models import UserProfile


def register_view(request: HttpRequest) -> HttpResponse:
    """User registration view.
    """
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()

    return render(request, 'forms_user/register.html', {'form': form})


@login_required
def edit_profile_view(request: HttpRequest) -> HttpResponse:
    """User edit profile view
    """
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("profile")

    else:
        form = UserProfileForm(instance=profile)

    return render(
        request,
        "forms_user/edit_profile.html",
        {"form": form}
    )


def change_password_view(request: HttpRequest) -> HttpResponse:
    """User change password view
    """
    if not request.user.is_authenticated:
        return redirect('register')

    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            login(request, request.user)
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'forms_user/change_password.html', {'form': form})


def profile_view(request: HttpRequest, username=None) -> HttpResponse:
    """User profile view
    """
    if not request.user.is_authenticated:
        return redirect('register')

    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    return render(request, 'forms_user/profile.html', {'profile_user': user})


@login_required
def delete_account_view(request: HttpRequest) -> HttpResponse:
    """Delete authenticated user account
    """
    if request.method == "POST":
        user = request.user

        user.delete()

        logout(request)

        return redirect("register")

    return render(
        request,
        "forms_user/delete_account.html"
    )
