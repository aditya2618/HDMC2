from .forms import ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
@login_required
def profile_edit(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
    if not profile:
        messages.error(request, "No profile found for this user.")
        return redirect('profile')
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_edit.html', {'form': form, 'profile': profile})
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Admission, Marksheet, Certificate, AdmissionNotice, Profile
from .forms import AdmissionForm

class CustomLoginRedirect:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and hasattr(request.user, 'profile') and request.path == settings.LOGIN_REDIRECT_URL:
            if request.session.get('new_user', False):
                request.session['new_user'] = False
                return redirect('user_profile')
        return response

@login_required
def documents(request):
    user = request.user
    # Replace with logic using request.user or Profile if needed
    marksheets = []
    certificates = []
    return render(request, 'marksheets_certificates.html', {'marksheets': marksheets, 'certificates': certificates})

@login_required
def profile(request):
    from .models import Profile, Admission
    profile = None
    admission = None
    blogs = []  # Placeholder for blogs - will need actual blog model later
    
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
        
        # Get admission status by user foreign key (fallback to email for existing records)
        try:
            admission = Admission.objects.get(user=request.user)
        except Admission.DoesNotExist:
            # Fallback for existing records without user association
            try:
                admission = Admission.objects.get(email=request.user.email, user__isnull=True)
                # Automatically associate with current user
                admission.user = request.user
                admission.save()
            except Admission.DoesNotExist:
                admission = None
    
    return render(request, 'profile.html', {
        'profile': profile,
        'admission': admission,
        'blogs': blogs
    })

@login_required


def admissions(request):
    notices = AdmissionNotice.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'admissions.html', {'notices': notices})

def admission_form(request):
    if request.method == 'POST':
        form = AdmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'admission_form.html', {'form': AdmissionForm(), 'submitted': True})
    else:
        form = AdmissionForm()
    return render(request, 'admission_form.html', {'form': form})
