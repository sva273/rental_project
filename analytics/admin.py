from django.contrib import admin
from .models import SearchHistory, ViewHistory


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing SearchHistory entries.

    Features:
        - Displays the user, search keyword, and timestamp of the search.
        - Orders entries by the most recent search first.
        - Makes 'searched_at' field read-only to prevent modification.
        - Adds filtering by 'searched_at'.
        - Allows searching by user's email or search keyword.
    """

    list_display = ["user", "keyword", "searched_at"]
    ordering = ["-searched_at"]
    readonly_fields = ["searched_at"]
    list_filter = ["searched_at"]
    search_fields = ["user__email", "keyword"]


@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing ViewHistory entries.

    Features:
        - Displays the user, listing viewed, and timestamp of the view.
        - Orders entries by the most recent view first.
        - Makes 'viewed_at' field read-only.
        - Adds filtering by 'viewed_at' and listing.
        - Allows searching by user's email or listing title.
    """

    list_display = ["user", "listing", "viewed_at"]
    ordering = ["-viewed_at"]
    readonly_fields = ["viewed_at"]
    list_filter = ["viewed_at", "listing"]
    search_fields = ["user__email", "listing__title"]
