from django.urls import path
from . import views
from . import payment_views

urlpatterns = [
    path('admissions/', views.admissions, name='admissions'),
    path('admission-form/', payment_views.admission_form, name='admission_form'),
    path('documents/', views.documents, name='documents'),
    path('profile/', views.profile, name='profile'),
    # path('user-profile/', views.user_profile_view, name='user_profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('payment/callback/', payment_views.payment_callback, name='payment_callback'),
]
