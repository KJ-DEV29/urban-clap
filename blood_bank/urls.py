from django.urls import path
from . import views

app_name = 'blood_bank'

urlpatterns = [
    path('', views.blood_bank_list, name='blood_bank_list'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('donations/', views.donation_list, name='donation_list'),
    path('donations/create/', views.donation_create, name='donation_create'),
    path('donations/<int:donation_id>/', views.donation_detail, name='donation_detail'),
    path('donations/<int:donation_id>/edit/', views.donation_edit, name='donation_edit'),
    path('donations/<int:donation_id>/delete/', views.donation_delete, name='donation_delete'),
] 