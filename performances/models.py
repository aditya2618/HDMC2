from django.db import models
import os
import uuid
from django.utils import timezone

def performance_image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_name = f"performance_{timezone.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('performances/images/', new_name)

class Performance(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=100)
    event_date = models.DateField()
    venue = models.CharField(max_length=255)
    is_upcoming = models.BooleanField(default=False, help_text="Check if this is an upcoming event. Uncheck for past events.")
    image = models.ImageField(upload_to=performance_image_upload_to, blank=True, null=True)
    video_url = models.URLField(max_length=500, blank=True)
    gallery = models.ForeignKey('gallery.GalleryMedia', on_delete=models.SET_NULL, null=True, blank=True, help_text="Link to gallery for this event.")

    def __str__(self):
        return self.title
