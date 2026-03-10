from django.urls import path
from . import views
from .views import PostListAPIView
from .views import color_view, tag_view

urlpatterns = [
    path('latest/', views.latest_posts_view, name="latest_posts"),
    path("register/", views.register_view, name="register"),
    path("api/posts/", PostListAPIView.as_view(), name="api_posts"),
    path("color/", color_view, name="color_view"),
    path("tag/", tag_view, name="tag_view"),
]
