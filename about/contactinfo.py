from django.db import models

class ContactInfo(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.email
