from django.db import models
import os
import uuid
from django.utils import timezone
from django.contrib.auth import get_user_model
from core.models import SoftDeleteModel

def student_photo_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_name = f"student_{timezone.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('students/photos/', new_name)

def student_file_upload_to(subfolder):
    def _upload_to(instance, filename):
        ext = filename.split('.')[-1]
        new_name = f"student_{subfolder}_{timezone.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
        return os.path.join(f'students/{subfolder}/', new_name)
    return _upload_to

def marksheet_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_name = f"marksheet_{timezone.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('marksheets/', new_name)

def certificate_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_name = f"certificate_{timezone.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('certificates/', new_name)

def aadhaar_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_name = f"admission_aadhaar_{timezone.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('admission/aadhaar/', new_name)

def education_certs_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_name = f"admission_education_certs_{timezone.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('admission/education_certs/', new_name)

def medical_fitness_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_name = f"admission_medical_fitness_{timezone.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('admission/medical_fitness/', new_name)

def training_certs_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_name = f"admission_training_certs_{timezone.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('admission/training_certs/', new_name)

class Admission(SoftDeleteModel):
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Third Gender', 'Third Gender'),
    ]
    EXPERTISE_LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    
    # Link admission to user (nullable for existing records)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='admissions', null=True, blank=True)
    
    name = models.CharField(max_length=255)
    aadhaar_no = models.CharField(max_length=20)
    father_mother_guardian = models.CharField(max_length=255)
    permanent_address = models.CharField(max_length=255)
    permanent_pincode = models.CharField(max_length=10)
    present_address = models.CharField(max_length=255)
    present_pincode = models.CharField(max_length=10)
    contact_no = models.CharField(max_length=20)
    email = models.EmailField()
    preferred_language = models.CharField(max_length=50)
    blood_group = models.CharField(max_length=10)
    medical_conditions = models.CharField(max_length=255, blank=True)
    admission_class = models.CharField(max_length=50)
    dob = models.DateField()
    age = models.IntegerField()
    sex = models.CharField(max_length=20, choices=SEX_CHOICES)
    qualification = models.CharField(max_length=255)
    school_college = models.CharField(max_length=255)
    school_college_address = models.CharField(max_length=255)
    reason_for_learning = models.TextField()
    previous_training = models.CharField(max_length=255, blank=True)
    affiliation = models.CharField(max_length=255, blank=True)
    art_form = models.CharField(max_length=100)
    expertise_level = models.CharField(max_length=20, choices=EXPERTISE_LEVEL_CHOICES)
    course_duration_years = models.IntegerField()
    photo_id_attached = models.BooleanField(default=False)
    photo_path = models.ImageField(upload_to=student_photo_upload_to, blank=True, null=True)
    aadhaar_path = models.FileField(upload_to=aadhaar_upload_to, blank=True, null=True)
    education_cert_path = models.FileField(upload_to=education_certs_upload_to, blank=True, null=True)
    medical_fitness_path = models.FileField(upload_to=medical_fitness_upload_to, blank=True, null=True)
    previous_training_cert = models.FileField(upload_to=training_certs_upload_to, blank=True, null=True)
    is_approved = models.BooleanField(default=False, help_text="Admin approval status for admission")
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default="Pending", choices=[("Pending", "Pending"), ("Paid", "Paid"), ("Failed", "Failed")])
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Marksheet(SoftDeleteModel):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=255)
    exam_date = models.DateField()
    subject = models.CharField(max_length=100)
    marks_obtained = models.FloatField()
    max_marks = models.FloatField()
    grade = models.CharField(max_length=20, blank=True)
    file_path = models.FileField(upload_to=marksheet_upload_to, blank=True, null=True)
    issued_date = models.DateField()

    def __str__(self):
        return f"{self.admission.name} - {self.exam_name}"

class Certificate(SoftDeleteModel):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE)
    certificate_type = models.CharField(max_length=100)
    issued_date = models.DateField()
    event_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to=certificate_upload_to, blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.admission.name} - {self.certificate_type}"

class AdmissionNotice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    available_classes = models.CharField(max_length=255, help_text="Comma-separated list of available classes")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Admission notice"
        verbose_name_plural = "Admission notices"


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name or self.user.username
