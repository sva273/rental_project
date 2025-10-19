from django.contrib import admin
from .models import SearchHistory, ViewHistory

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'keyword', 'searched_at']
    ordering = ['-searched_at']
    readonly_fields = ['searched_at']
    list_filter = ['searched_at']
    search_fields = ['user__email', 'keyword']


@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'viewed_at']
    ordering = ['-viewed_at']
    readonly_fields = ['viewed_at']
    list_filter = ['viewed_at', 'listing']
    search_fields = ['user__email', 'listing__title']
