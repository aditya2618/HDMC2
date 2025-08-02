from django.contrib import admin
from .models import HomepageSection, Testimonial, HomepageHighlight

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active', 'display_order')
    list_filter = ('is_active', 'role')
    search_fields = ('name', 'content')
    ordering = ['display_order', '-created_at']

@admin.register(HomepageSection)
class HomepageSectionAdmin(admin.ModelAdmin):
    list_display = ('section_name', 'heading', 'active', 'display_order')
    list_filter = ('active',)
    ordering = ['display_order']

admin.site.register(HomepageHighlight)
