from django.urls import path
from . import views

app_name = 'about'
urlpatterns = [
    path('', views.about, name='about'),
    path('guru/<int:pk>/', views.guru_detail, name='guru_detail'),
]
