import os
import uuid
from django.utils import timezone
from django.db import models

def aboutus_image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_name = f"aboutus_{timezone.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('aboutus/', new_name)

def guru_photo_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_name = f"guru_{timezone.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('gurus/', new_name)

class ContactInfo(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.email

class AboutUs(models.Model):
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "About Us"

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"

class AboutUsImage(models.Model):
    about = models.ForeignKey('AboutUs', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=aboutus_image_upload_to)
    caption = models.CharField(max_length=255, blank=True)
    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self.caption or f"Image {self.pk}"

class Guru(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    biodata = models.TextField()
    photo = models.ImageField(upload_to=guru_photo_upload_to, blank=True, null=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name}"
