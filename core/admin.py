from django.contrib import admin
from .models import DeletionLog, ContactMessage

# Base admin class for soft delete functionality
class SoftDeleteAdmin(admin.ModelAdmin):
    list_filter = ('is_deleted',)
    actions = ['soft_delete_selected', 'restore_selected', 'hard_delete_selected']

    def get_queryset(self, request):
        """Show all items including soft deleted"""
        return self.model.objects.all()

    def soft_delete_selected(self, request, queryset):
        """Soft delete selected items"""
        count = 0
        for obj in queryset.filter(is_deleted=False):
            obj.soft_delete(user=request.user)
            count += 1
        self.message_user(request, f'{count} items soft deleted.')
    soft_delete_selected.short_description = "Soft delete selected items"

    def restore_selected(self, request, queryset):
        """Restore soft deleted items"""
        count = queryset.filter(is_deleted=True).count()
        for obj in queryset.filter(is_deleted=True):
            obj.restore()
        self.message_user(request, f'{count} items restored.')
    restore_selected.short_description = "Restore selected items"

    def hard_delete_selected(self, request, queryset):
        """Permanently delete items (admin only)"""
        if not request.user.is_superuser:
            self.message_user(request, "Only superusers can permanently delete items.", level='ERROR')
            return
        
        count = 0
        for obj in queryset:
            if not obj.is_deleted:
                obj.soft_delete(user=request.user)
            obj.delete()  # Hard delete
            count += 1
        self.message_user(request, f'{count} items permanently deleted.')
    hard_delete_selected.short_description = "Permanently delete selected items (Admin only)"

    def delete_model(self, request, obj):
        """Override single item deletion to use soft delete"""
        obj.soft_delete(user=request.user)

    def delete_queryset(self, request, queryset):
        """Override bulk deletion to use soft delete"""
        for obj in queryset:
            obj.soft_delete(user=request.user)

@admin.register(DeletionLog)
class DeletionLogAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'object_id', 'deleted_by', 'deleted_at')
    list_filter = ('model_name', 'deleted_at', 'deleted_by')
    search_fields = ('model_name', 'object_id')
    readonly_fields = [f.name for f in DeletionLog._meta.fields]
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(ContactMessage)
class ContactMessageAdmin(SoftDeleteAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at', 'is_read', 'is_deleted')
    list_filter = ('is_read', 'submitted_at', 'is_deleted')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('submitted_at',)

# All models have been moved to their respective apps:
# - Student models: students/admin.py
# - Gallery models: gallery/admin.py  
# - Performance models: performances/admin.py
# - About/Guru models: about/admin.py
# - Homepage/Testimonial models: homepage/admin.py
