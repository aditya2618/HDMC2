#!/usr/bin/env python
"""
Script to populate related data for all database records in HDMC2
"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hdmc.settings')
django.setup()

from core.models import Performance, GalleryMedia, Testimonial, HomepageSection, AdmissionNotice, Student

def run():
    # Link performances to gallery media
    gallery_items = list(GalleryMedia.objects.filter(is_active=True))
    performances = Performance.objects.all()
    for i, perf in enumerate(performances):
        if gallery_items:
            perf.gallery = gallery_items[i % len(gallery_items)]
            perf.save()
    print(f"Linked {len(performances)} performances to gallery media.")

    # Add testimonials for students and parents
    students = Student.objects.all()
    for i, student in enumerate(students):
        Testimonial.objects.get_or_create(
            name=student.name,
            role='Student',
            content=f"I love learning at HDMC! My favorite art form is {student.art_form}.",
            is_active=True,
            display_order=10+i
        )
    print(f"Added testimonials for {len(students)} students.")

    # Add parent testimonials (if students exist)
    for i, student in enumerate(students):
        Testimonial.objects.get_or_create(
            name=f"Parent of {student.name}",
            role='Parent',
            content=f"My child {student.name} has grown so much at HDMC!",
            is_active=True,
            display_order=20+i
        )
    print(f"Added parent testimonials for {len(students)} students.")

    # Add homepage sections
    HomepageSection.objects.get_or_create(
        section_name='Welcome',
        heading='Welcome to HDMC',
        content='Join our vibrant cultural family and experience the rhythm of tradition.',
        display_order=1,
        active=True
    )
    HomepageSection.objects.get_or_create(
        section_name='Programs',
        heading='Our Programs',
        content='We offer classical dance, folk music, and creative classes for all ages.',
        display_order=2,
        active=True
    )
    print("Added homepage sections.")

    # Link admission notices to available classes
    notices = AdmissionNotice.objects.all()
    for notice in notices:
        notice.available_classes = 'Classical Dance, Folk Music, Kids Classes, Adult Classes'
        notice.save()
    print(f"Updated {len(notices)} admission notices with available classes.")

if __name__ == '__main__':
    run()
