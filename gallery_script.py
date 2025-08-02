from core.models import GalleryMedia

# Clear existing gallery items
GalleryMedia.objects.all().delete()

# Gallery data
gallery_items = [
    {
        'title': 'Manipuri Classical Dance Performance',
        'description': 'Students performing traditional Manipuri classical dance showcasing the rich cultural heritage of Manipur.',
        'file_path': 'gallery/Culture-of-Manipur.jpg',
        'media_type': 'photo',
        'display_order': 1
    },
    {
        'title': 'Dance Workshop Session',
        'description': 'Interactive dance workshop where students learn traditional dance forms and techniques.',
        'file_path': 'gallery/3.jpg',
        'media_type': 'photo',
        'display_order': 2
    },
    {
        'title': 'Group Performance at Cultural Event',
        'description': 'A group of talented students performing at our annual cultural celebration.',
        'file_path': 'gallery/4.jpg',
        'media_type': 'photo',
        'display_order': 3
    },
    {
        'title': 'Traditional Costume Showcase',
        'description': 'Students showcasing beautiful traditional Manipuri costumes during a performance.',
        'file_path': 'gallery/5.jpg',
        'media_type': 'photo',
        'display_order': 4
    },
    {
        'title': 'About HDMC - Our Heritage',
        'description': 'Visual representation of our cultural center and its mission to preserve Manipuri arts.',
        'file_path': 'aboutus/Culture-of-Manipur.jpg',
        'media_type': 'photo',
        'display_order': 5
    },
    {
        'title': 'Dance Class in Session',
        'description': 'Students learning fundamental movements in our spacious dance studio.',
        'file_path': 'aboutus/4.jpg',
        'media_type': 'photo',
        'display_order': 6
    },
    {
        'title': 'Cultural Heritage Display',
        'description': 'Display of traditional artifacts and cultural elements that inspire our teaching.',
        'file_path': 'aboutus/5.jpg',
        'media_type': 'photo',
        'display_order': 7
    },
    {
        'title': 'Student Achievement Celebration',
        'description': 'Celebrating the achievements of our dedicated students in traditional arts.',
        'file_path': 'aboutus/1.webp',
        'media_type': 'photo',
        'display_order': 8
    },
    {
        'title': 'Performance Stage Setup',
        'description': 'Behind the scenes of our performance preparations and stage arrangements.',
        'file_path': 'performances/images/Culture-of-Manipur.jpg',
        'media_type': 'photo',
        'display_order': 9
    },
    {
        'title': 'Student Portrait Session',
        'description': 'Professional portraits of our talented students in traditional attire.',
        'file_path': 'students/photos/3.jpg',
        'media_type': 'photo',
        'display_order': 10
    }
]

# Create gallery items
created_count = 0
for item_data in gallery_items:
    gallery_item = GalleryMedia.objects.create(
        title=item_data['title'],
        description=item_data['description'],
        media_type=item_data['media_type'],
        file_path=item_data['file_path'],
        display_order=item_data['display_order'],
        is_active=True
    )
    print(f"✅ Created: {gallery_item.title}")
    created_count += 1

print(f"\n🎉 Successfully created {created_count} gallery items!")

# Display all gallery items
print("\n📋 Gallery Items:")
print("-" * 50)
for item in GalleryMedia.objects.all().order_by('display_order'):
    print(f"{item.display_order}. {item.title}")
    print(f"   Type: {item.media_type}")
    print(f"   File: {item.file_path}")
    print(f"   Active: {item.is_active}")
    print()
