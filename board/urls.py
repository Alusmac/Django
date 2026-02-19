from django.urls import path
from . import views

urlpatterns = [
    path('ads/', views.ads_list, name='ads_list'),
    path('ads/category/<int:category_id>/', views.ads_by_category, name='ads_by_category'),
    path('my_ads/', views.my_ads, name='my_ads'),
]
