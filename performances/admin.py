from django.contrib import admin
from .models import Performance

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'is_upcoming', 'venue')
    list_filter = ('is_upcoming', 'event_date')
    search_fields = ('title', 'venue', 'description')
