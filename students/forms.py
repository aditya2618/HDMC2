from django import forms
from .models import Admission, Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'phone', 'address', 'dob', 'gender', 'photo']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        exclude = ['is_deleted', 'deleted_by', 'deleted_at', 'is_active', 'is_approved', 'payment_status', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'reason_for_learning': forms.Textarea(attrs={'rows': 3}),
        }
