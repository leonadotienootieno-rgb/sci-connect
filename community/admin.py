from django.contrib import admin
from .models import Resource, Topic, Post


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_by', 'uploaded_at')
    list_filter = ('category',)
    search_fields = ('title', 'description', 'uploaded_by__email')
    ordering = ('-uploaded_at',)

    def uploaded_by(self, obj):
        return obj.uploaded_by.email

    uploaded_by.short_description = 'Uploader Email'


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name', 'created_by__email')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'created_by', 'created_at', 'content_snippet')
    list_filter = ('topic',)
    search_fields = ('content', 'created_by__email')
    ordering = ('-created_at',)

    # Helper to show a snippet of the post content
    def content_snippet(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_snippet.short_description = 'Content'
