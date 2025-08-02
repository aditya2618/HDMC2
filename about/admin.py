from django.contrib import admin
from .models import AboutUs, AboutUsImage, Guru, ContactMessage, ContactInfo

class AboutUsImageInline(admin.TabularInline):
    model = AboutUsImage
    extra = 1

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    inlines = [AboutUsImageInline]

@admin.register(Guru)
class GuruAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('name', 'designation', 'biodata')
    ordering = ['display_order', 'name']

admin.site.register(ContactMessage)
admin.site.register(ContactInfo)
