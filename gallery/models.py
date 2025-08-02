from django.db import models
import os
import uuid
from django.utils import timezone

def gallery_media_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_name = f"gallery_{timezone.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('gallery/', new_name)

class GalleryMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file_path = models.FileField(upload_to=gallery_media_upload_to, blank=True, null=True)
    video_url = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
