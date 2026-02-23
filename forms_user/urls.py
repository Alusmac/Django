from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile_view, name="home"),
    path('register/', views.register_view, name='register'),
    path('edit/', views.edit_profile_view, name='edit_profile'),
    path('password/', views.change_password_view, name='change_password'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<str:username>/', views.profile_view, name='user_profile'),
    path("delete-account/", views.delete_account_view, name="delete_account"),
]