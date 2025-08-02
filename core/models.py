
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import json

# Deletion audit trail model
class DeletionLog(models.Model):
    model_name = models.CharField(max_length=128)
    object_id = models.PositiveIntegerField()
    deleted_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    deleted_at = models.DateTimeField(auto_now_add=True)
    data_snapshot = models.JSONField()

    def __str__(self):
        return f"{self.model_name} id={self.object_id} deleted by {self.deleted_by} at {self.deleted_at}"

    class Meta:
        ordering = ['-deleted_at']

# Abstract base model with soft delete functionality
class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        abstract = True

    def as_dict(self):
        """Serialize model instance to dictionary for backup"""
        data = {}
        for field in self._meta.fields:
            value = getattr(self, field.name)
            if hasattr(value, 'url'):  # Handle file fields
                data[field.name] = value.url if value else None
            elif hasattr(value, 'isoformat'):  # Handle datetime fields
                data[field.name] = value.isoformat() if value else None
            else:
                data[field.name] = str(value) if value is not None else None
        return data

    def soft_delete(self, user=None):
        """Soft delete with audit trail"""
        # Create backup in DeletionLog
        DeletionLog.objects.create(
            model_name=self.__class__.__name__,
            object_id=self.id,
            deleted_by=user,
            data_snapshot=self.as_dict(),
        )
        
        # Mark as deleted
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save()

    def restore(self):
        """Restore soft deleted item"""
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save()

# ContactMessage model for About Us contact form
class ContactMessage(SoftDeleteModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.email})"
