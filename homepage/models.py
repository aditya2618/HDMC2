from django.db import models
import os
import uuid
from django.utils import timezone

def testimonial_image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_name = f"testimonial_{timezone.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('testimonials/', new_name)

class HomepageSection(models.Model):
    section_name = models.CharField(max_length=50)
    heading = models.CharField(max_length=255)
    content = models.TextField()
    image_path = models.CharField(max_length=255, blank=True)
    video_link = models.CharField(max_length=255, blank=True)
    display_order = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.section_name

class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100, help_text="e.g., Student, Parent, etc.")
    content = models.TextField()
    image = models.ImageField(upload_to=testimonial_image_upload_to, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.role}"

    class Meta:
        ordering = ['display_order', '-created_at']

class HomepageHighlight(models.Model):
    SECTION_TYPE_CHOICES = [
        ('gallery', 'Gallery'),
        ('performance', 'Performance'),
    ]
    section_type = models.CharField(max_length=20, choices=SECTION_TYPE_CHOICES)
    ref_id = models.IntegerField()
    display_order = models.IntegerField(default=0)
    comment = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.section_type} - {self.ref_id}"
