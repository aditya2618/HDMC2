#!/usr/bin/env python3

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hdmc.settings')
django.setup()

from django.contrib.auth.models import User
from students.models import Admission

def fix_admission_users():
    """Associate existing admissions with users based on email matching"""
    
    # Get admissions without user association
    unlinked_admissions = Admission.objects.filter(user__isnull=True)
    
    print(f"Found {unlinked_admissions.count()} admissions without user association")
    
    for admission in unlinked_admissions:
        try:
            # Try to find user by email
            user = User.objects.get(email=admission.email)
            admission.user = user
            admission.save()
            print(f"Associated admission {admission.id} ({admission.name}) with user {user.username}")
        except User.DoesNotExist:
            print(f"No user found for email {admission.email} (admission {admission.id} - {admission.name})")
        except User.MultipleObjectsReturned:
            # If multiple users with same email, use the first one
            user = User.objects.filter(email=admission.email).first()
            admission.user = user
            admission.save()
            print(f"Multiple users found for {admission.email}, associated with {user.username}")

if __name__ == "__main__":
    fix_admission_users()
    print("Admission user association complete!")
