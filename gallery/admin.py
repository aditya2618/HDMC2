from django.contrib import admin
from .models import GalleryMedia

@admin.register(GalleryMedia)
class GalleryMediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'is_active', 'uploaded_at')
    list_filter = ('media_type', 'is_active', 'uploaded_at')
    search_fields = ('title', 'description')
