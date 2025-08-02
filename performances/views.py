from django.shortcuts import render
from .models import Performance

def performance(request):
    upcoming = Performance.objects.filter(is_upcoming=True).order_by('event_date')
    past = Performance.objects.filter(is_upcoming=False).order_by('-event_date')
    return render(request, 'performance.html', {'upcoming': upcoming, 'past': past})
