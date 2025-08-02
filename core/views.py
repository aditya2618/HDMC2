from django.contrib.auth.decorators import login_required
from students.models import Admission
from django.shortcuts import render
# ...existing code...

@login_required
def myaccounts(request):
    admissions = Admission.objects.filter(user=request.user)
    return render(request, 'account/myaccounts.html', {'admissions': admissions})
from django.shortcuts import render

# All views have been moved to their respective apps:
# - Student views: students/views.py
# - Gallery views: gallery/views.py  
# - Performance views: performances/views.py
# - About views: about/views.py
# - Homepage views: homepage/views.py
