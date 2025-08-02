
from django.shortcuts import render, get_object_or_404, redirect
from .models import AboutUs, Guru, ContactInfo, ContactMessage
from django import forms
from django.contrib import messages

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']

def about(request):
    about_obj = AboutUs.objects.first()
    gurus = Guru.objects.filter(is_active=True).order_by('display_order', 'name')
    contact = ContactInfo.objects.first()
    form = ContactMessageForm()
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent!')
            return redirect('about')
    return render(request, 'about.html', {
        'about': about_obj,
        'gurus': gurus,
        'contact': contact,
        'form': form,
    })

def guru_detail(request, pk):
    guru = get_object_or_404(Guru, pk=pk)
    return render(request, 'guru_detail.html', {'guru': guru})
