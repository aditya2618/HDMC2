from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from .models import HomepageSection, Testimonial
from gallery.models import GalleryMedia
from performances.models import Performance
from students.models import Admission, AdmissionNotice
from about.models import ContactMessage

def home(request):
    # Get recent gallery images for hero section
    hero_images = GalleryMedia.objects.filter(
        media_type='photo', 
        is_active=True
    ).order_by('-uploaded_at')[:5]
    
    # Get upcoming events/performances for the events section
    upcoming_events = Performance.objects.filter(
        is_upcoming=True
    ).order_by('event_date')[:3]
    
    # Get recent performance highlights
    recent_performances = Performance.objects.filter(
        is_upcoming=False
    ).order_by('-event_date')[:2]
    
    # Get homepage sections (if any custom content exists)
    homepage_sections = HomepageSection.objects.filter(
        active=True
    ).order_by('display_order')
    
    # Get admission notices that are active
    active_notices = AdmissionNotice.objects.filter(
        is_active=True
    ).order_by('-created_at')[:2]
    
    # Get recent gallery items for showcase
    recent_gallery = GalleryMedia.objects.filter(
        is_active=True
    ).order_by('-uploaded_at')[:6]
    
    # Get active testimonials
    testimonials = Testimonial.objects.filter(
        is_active=True
    ).order_by('display_order')[:4]
    
    context = {
        'hero_images': hero_images,
        'upcoming_events': upcoming_events,
        'recent_performances': recent_performances,
        'homepage_sections': homepage_sections,
        'active_notices': active_notices,
        'recent_gallery': recent_gallery,
        'testimonials': testimonials,
    }
    
    return render(request, 'home.html', context)

@staff_member_required
def admin_dashboard(request):
    stats = {
        'total_students': Admission.objects.count(),
        'pending_approvals': Admission.objects.filter(is_approved=False).count(),
        'total_performances': Performance.objects.count(),
        'total_gallery': GalleryMedia.objects.count(),
    }
    upcoming = Performance.objects.filter(event_date__gte=timezone.now()).order_by('event_date')[:5]
    pending_students = Admission.objects.filter(is_approved=False)[:5]
    recent_gallery = GalleryMedia.objects.order_by('-id')[:5]
    notices = AdmissionNotice.objects.order_by('-created_at')[:5]
    recent_contacts = ContactMessage.objects.order_by('-id')[:5]
    return render(request, 'admin_dashboard.html', {
        'stats': stats,
        'upcoming': upcoming,
        'pending_students': pending_students,
        'recent_gallery': recent_gallery,
        'notices': notices,
        'recent_contacts': recent_contacts,
    })
