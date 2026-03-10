from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from .forms import RegisterForm
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAdminOrReadOnly
from .forms import ColorForm, TagForm


def latest_posts_view(request: HttpRequest) -> HttpResponse:
    """Render the latest posts template
    """
    return render(request, "customization_22/latest_posts.html")


def register_view(request: HttpRequest) -> HttpResponse:
    """Render the latest posts template
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "customization_22/register.html", {"form": form})


class PostListAPIView(generics.ListAPIView):
    """API view for listing posts with optional title filtering
    """
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """Return filtered queryset based on optional 'title' GET parameter
        """
        queryset = Post.objects.all()

        title = self.request.GET.get("title")

        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset


def color_view(request: HttpRequest) -> HttpResponse:
    """Render and process ColorForm to display favorite color
    """
    if request.method == "POST":
        form = ColorForm(request.POST)
        if form.is_valid():
            color = form.cleaned_data["favorite_color"]

            return render(request, "customization_22/color_result.html", {"color": color})
    else:
        form = ColorForm()
    return render(request, "customization_22/color_form.html", {"form": form})


def tag_view(request: HttpRequest) -> HttpResponse:
    """Render and process TagForm to create new tags
    """
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tag_view")
    else:
        form = TagForm()
    return render(request, "customization_22/tag_form.html", {"form": form})
