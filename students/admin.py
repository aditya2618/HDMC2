from django.contrib import admin
from .models import Admission, Marksheet, Certificate, AdmissionNotice, Profile
from core.admin import SoftDeleteAdmin

@admin.register(Admission)
class AdmissionAdmin(SoftDeleteAdmin):
    list_display = ('name', 'email', 'admission_class', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'admission_class', 'created_at', 'is_deleted')
    search_fields = ('name', 'email', 'aadhaar_no')
    actions = ['approve_admissions'] + SoftDeleteAdmin.actions

    def approve_admissions(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} admission(s) approved.")
    approve_admissions.short_description = "Approve selected admissions"

@admin.register(Marksheet)
class MarksheetAdmin(SoftDeleteAdmin):
    list_display = ('admission', 'exam_name', 'exam_date', 'grade')
    list_filter = ('exam_date', 'grade', 'is_deleted')
    search_fields = ('admission__name', 'exam_name', 'subject')

@admin.register(Certificate)
class CertificateAdmin(SoftDeleteAdmin):
    list_display = ('admission', 'certificate_type', 'issued_date')
    list_filter = ('certificate_type', 'issued_date', 'is_deleted')
    search_fields = ('admission__name', 'certificate_type', 'event_name')

@admin.register(AdmissionNotice)
class AdmissionNoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'dob', 'gender', 'created_at')
    search_fields = ('full_name', 'user__username', 'phone', 'address')
    list_filter = ('gender', 'created_at')
