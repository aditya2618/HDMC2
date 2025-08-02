from django.urls import path
from . import views

urlpatterns = [
    path('admissions/', views.admissions, name='admissions'),
    path('admission-form/', views.admission_form, name='admission_form'),
    path('documents/', views.documents, name='documents'),
    path('profile/', views.profile, name='profile'),
    path('user-profile/', views.user_profile_view, name='user_profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
