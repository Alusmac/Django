from django.contrib import admin
from .models import Profile, Category, Ad, Comment

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Comment)


# admin.site.register(Ad) # Adding without full information


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_active', 'category', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('title',)
#⬆︎⬆︎⬆︎Shows full information about the price, title, who added it, category, active or no
