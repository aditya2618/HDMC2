from django import forms
from .models import Student, ContactMessage

class StudentAdmissionForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['is_approved', 'created_at']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

# ContactMessage form for About Us contact message
class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Type your message here...'}),
        }
    class Meta:
        model = Student
        exclude = ['is_approved', 'created_at']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
