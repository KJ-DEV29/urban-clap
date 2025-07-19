from django.urls import path
from . import views

app_name = 'donors'

urlpatterns = [
    path('', views.donor_list, name='donor_list'),
    path('register/', views.donor_register, name='donor_register'),
    path('<int:donor_id>/', views.donor_detail, name='donor_detail'),
    path('<int:donor_id>/edit/', views.donor_edit, name='donor_edit'),
    path('<int:donor_id>/delete/', views.donor_delete, name='donor_delete'),
    path('search/', views.donor_search, name='donor_search'),
] 