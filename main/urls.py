from django.urls import path
from . import views
from .views import ContactView, ServiceView

urlpatterns = [
    #path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('service/', ServiceView.as_view(), name='service'),
]
