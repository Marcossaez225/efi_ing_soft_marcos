from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_text', 'created_at', 'vehicle')
    list_filter = ('created_at', 'user', 'vehicle')
    search_fields = ('text', 'user__username', 'vehicle__model')

    def short_text(self, obj):
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    short_text.short_description = 'Comment'

admin.site.register(Comment, CommentAdmin)
