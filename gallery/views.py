from django.shortcuts import render
from .models import GalleryMedia

def gallery(request):
    gallery_items = GalleryMedia.objects.filter(is_active=True).order_by('display_order', '-uploaded_at')
    return render(request, 'gallery.html', {'gallery_items': gallery_items})
