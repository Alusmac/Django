from django.contrib import admin
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    """Inline representation of Comment model for PostAdmin
    """
    model = Comment
    extra = 1
    readonly_fields = ("created_at",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for Post model
    """
    list_display = ("title", "created_at", "comment_count")
    search_fields = ("title", "content")
    list_filter = ("created_at",)
    inlines = [CommentInline]

    actions = ["make_title_upper"]

    def comment_count(self, obj) -> int:
        """Return the number of comments related to the post
        """
        return obj.count_comments()

    comment_count.short_description = "Comments"

    def make_title_upper(self, request, queryset) -> None:
        """Convert titles of selected posts to uppercase
        """
        for post in queryset:
            post.title = post.title.upper()
            post.save()
        self.message_user(request, "Selected posts updated to uppercase!")

    make_title_upper.short_description = "Convert titles to uppercase"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for Comment model
    """
    list_display = ("post", "text", "created_at")
    search_fields = ("text",)
    list_filter = ("created_at",)
