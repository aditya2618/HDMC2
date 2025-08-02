from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('performance/', views.performance, name='performance'),
    path('admissions/', views.admissions, name='admissions'),
    path('admissions/form/', views.admission_form, name='admission_form'),
    path('gallery/', views.gallery, name='gallery'),
    path('accounts/profile/', views.profile, name='profile'),
    path('documents/', views.documents, name='documents'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
