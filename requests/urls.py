from django.urls import path
from . import views

app_name = 'requests'

urlpatterns = [
    path('', views.request_list, name='request_list'),
    path('create/', views.request_create, name='request_create'),
    path('<int:request_id>/', views.request_detail, name='request_detail'),
    path('<int:request_id>/edit/', views.request_edit, name='request_edit'),
    path('<int:request_id>/delete/', views.request_delete, name='request_delete'),
    path('<int:request_id>/approve/', views.request_approve, name='request_approve'),
    path('<int:request_id>/reject/', views.request_reject, name='request_reject'),
    path('<int:request_id>/fulfill/', views.request_fulfill, name='request_fulfill'),
] 