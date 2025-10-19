from django.contrib import admin, messages
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'listing',
        'tenant',
        'rating',
        'short_comment',
        'is_approved',
        'created_at',
    )

    list_filter = (
        'rating',
        'is_approved',
        'created_at',
        'listing__city',
    )

    search_fields = (
        'listing__title',
        'tenant__email',
        'tenant__username',
        'comment',
    )

    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 25

    fieldsets = (
        ('Main Information', {
            'fields': ('listing', 'tenant', 'rating', 'is_approved')
        }),
        ('Comment', {
            'fields': ('comment',)
        }),
        ('System Fields', {
            'fields': ('created_at',)
        }),
    )

    actions = ['approve_reviews']

    def short_comment(self, obj):
        """Short version of the comment (for list display)"""
        return (obj.comment[:50] + '...') if len(obj.comment) > 50 else obj.comment
    short_comment.short_description = 'Comment'

    @admin.action(description="Approve selected reviews")
    def approve_reviews(self, request, queryset):
        """Bulk approval of selected reviews"""
        updated = 0
        for review in queryset:
            if not review.is_approved:
                review.is_approved = True
                review.save()
                updated += 1
        self.message_user(request, f"{updated} review(s) approved.", messages.SUCCESS)
