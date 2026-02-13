from django.urls import path, re_path
from . import views

urlpatterns = [

    path('home/', views.home_view),
    path('about/', views.about_view),
    path('contact/', views.contact_view),

    re_path(r'^post/(?P<id>\d+)/$', views.post_view),
    re_path(r'^profile/(?P<username>[A-Za-z]+)/$', views.profile_view),

    re_path(r'^event/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.event_view),

]
