from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Common routes
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('enquiry/', views.enquiry, name='enquiry'),
    path('review/', views.review, name='review'),
    
    # User routes
    path('dashboard/', views.dashboard, name='dashboard'),
    path('donate-blood/', views.donate_blood, name='donate_blood'),
    path('purchase-blood/', views.purchase_blood, name='purchase_blood'),
    
    # Admin routes
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
] 