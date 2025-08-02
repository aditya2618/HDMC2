import os
import django
import random
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hdmc.settings')
django.setup()

from gallery.models import GalleryMedia
from performances.models import Performance

gallery_folder = os.path.join('media', 'gallery')
gallery_files = [f for f in os.listdir(gallery_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]

titles = [
    'Culture of Manipur',
    'Annual Performance',
    'Traditional Dance',
    'Student Showcase',
    'Festival Moments',
]
descriptions = [
    'A glimpse of the vibrant culture of Manipur.',
    'Students performing traditional dance.',
    'Celebrating our heritage through dance.',
    'Memorable moments from our annual event.',
    'Capturing the spirit of the festival.',
]

gallery_objs = []
for idx, filename in enumerate(gallery_files):
    title = titles[idx % len(titles)]
    desc = descriptions[idx % len(descriptions)]
    obj, created = GalleryMedia.objects.get_or_create(
        media_type='photo',
        title=title,
        description=desc,
        file_path=os.path.join('gallery', filename),
        display_order=idx+1,
        is_active=True,
    )
    gallery_objs.append(obj)
    print(f"{'Created' if created else 'Exists'}: {title} -> {filename}")

# Add sample performances
performance_samples = [
    {
        'title': 'Manipuri Dance Showcase',
        'description': 'A special event featuring Manipuri dance and music.',
        'event_type': 'Dance',
        'event_date': date(2025, 7, 15),
        'venue': 'HDMC Auditorium',
        'is_upcoming': False,
        'image': os.path.join('performances/images', 'Culture-of-Manipur.jpg'),
        'gallery': gallery_objs[0] if gallery_objs else None,
    },
    {
        'title': 'Annual Student Performance',
        'description': 'Students present their annual cultural performances.',
        'event_type': 'Annual Event',
        'event_date': date(2025, 6, 10),
        'venue': 'Main Hall',
        'is_upcoming': False,
        'image': os.path.join('performances/images', 'Culture-of-Manipur.jpg'),
        'gallery': gallery_objs[1] if len(gallery_objs) > 1 else None,
    },
]
for data in performance_samples:
    obj, created = Performance.objects.get_or_create(
        title=data['title'],
        defaults={
            'description': data['description'],
            'event_type': data['event_type'],
            'event_date': data['event_date'],
            'venue': data['venue'],
            'is_upcoming': data['is_upcoming'],
            'image': data['image'],
            'gallery': data['gallery'],
        }
    )
    print(f"{'Created' if created else 'Exists'}: {data['title']}")

print("Gallery and Performance sample data populated.")
