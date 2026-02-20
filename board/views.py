from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from .models import Ad, Category
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.shortcuts import render
from .models import Ad


def ads_list(request):
    ads = Ad.objects.annotate(comments_total=Count('comments'))
    return render(request, "board/ads_list.html", {"ads": ads})


def ads_by_category(request: HttpRequest, category_id: int) -> HttpResponse:
    """Display a list of active ads filtered by a specific category
    """
    category = get_object_or_404(Category, id=category_id)
    ads = Ad.objects.filter(category=category, is_active=True)
    return render(request, "board/ads_by_category.html", {"ads": ads})


def my_ads(request: HttpRequest) -> HttpResponse:
    """Display a list of ads created by user
    """
    user = request.user
    ads = user.ads.all()
    return render(request, "board/my_ads.html", {"ads": ads})


def recent_ads_view(request: HttpRequest) -> HttpResponse:
    """Display a list of ads created in the last 30 days.
    """
    recent_ads = Ad.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=30)
    )
    return render(request, "board/recent_ads.html", {"ads": recent_ads})

