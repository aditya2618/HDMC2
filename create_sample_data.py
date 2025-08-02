#!/usr/bin/env python
"""
Script to add sample data for the dynamic home page
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hdmc.settings')
django.setup()

from core.models import Testimonial, Performance, GalleryMedia, AdmissionNotice

def create_sample_data():
    print("Creating sample data for dynamic home page...")
    
    # Create sample testimonials
    testimonials = [
        {
            'name': 'Priya Sharma',
            'role': 'Parent',
            'content': 'HDMC has been incredible for my daughter\'s development. The teachers are passionate and caring, and the environment is nurturing.',
            'is_active': True,
            'display_order': 1
        },
        {
            'name': 'Rajesh Kumar',
            'role': 'Adult Student',
            'content': 'Learning classical dance at HDMC has been a dream come true. The instructors are patient and skilled.',
            'is_active': True,
            'display_order': 2
        },
        {
            'name': 'Anita Devi',
            'role': 'Former Student',
            'content': 'HDMC gave me the foundation I needed to pursue dance professionally. Forever grateful for the training I received here.',
            'is_active': True,
            'display_order': 3
        }
    ]
    
    for testimonial_data in testimonials:
        testimonial, created = Testimonial.objects.get_or_create(
            name=testimonial_data['name'],
            defaults=testimonial_data
        )
        if created:
            print(f"Created testimonial: {testimonial.name}")
        else:
            print(f"Testimonial already exists: {testimonial.name}")
    
    # Create sample performances
    performances = [
        {
            'title': 'Annual Cultural Festival',
            'description': 'A grand celebration of traditional arts featuring performances by all our students across different age groups.',
            'event_type': 'Annual Event',
            'event_date': datetime.now().date() + timedelta(days=30),
            'venue': 'HDMC Main Auditorium',
            'is_upcoming': True
        },
        {
            'title': 'Classical Dance Showcase',
            'description': 'An elegant evening showcasing classical dance forms performed by our advanced students.',
            'event_type': 'Showcase',
            'event_date': datetime.now().date() - timedelta(days=15),
            'venue': 'City Cultural Center',
            'is_upcoming': False
        },
        {
            'title': 'Student Recital Night',
            'description': 'A special evening where students present their progress and newly learned pieces.',
            'event_type': 'Recital',
            'event_date': datetime.now().date() + timedelta(days=45),
            'venue': 'HDMC Studio Hall',
            'is_upcoming': True
        }
    ]
    
    for perf_data in performances:
        performance, created = Performance.objects.get_or_create(
            title=perf_data['title'],
            defaults=perf_data
        )
        if created:
            print(f"Created performance: {performance.title}")
        else:
            print(f"Performance already exists: {performance.title}")
    
    # Create sample admission notice
    notice_data = {
        'title': 'New Batch Admissions Open - Fall 2025',
        'content': 'We are excited to announce that admissions are now open for our Fall 2025 batches! Join us for an enriching journey in classical and folk arts.',
        'available_classes': 'Classical Dance, Folk Music, Kids Classes, Adult Classes',
        'is_active': True
    }
    
    notice, created = AdmissionNotice.objects.get_or_create(
        title=notice_data['title'],
        defaults=notice_data
    )
    if created:
        print(f"Created admission notice: {notice.title}")
    else:
        print(f"Admission notice already exists: {notice.title}")
    
    print("Sample data creation completed!")

if __name__ == '__main__':
    create_sample_data()
