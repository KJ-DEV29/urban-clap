from django.contrib import admin
from .models import BloodRequest

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ['hospital_name', 'blood_type', 'units_needed', 'priority', 'status', 'needed_by_date', 'request_date']
    list_filter = ['status', 'priority', 'blood_type', 'request_date', 'needed_by_date']
    search_fields = ['hospital_name', 'requester_name', 'patient_name', 'doctor_name']
    readonly_fields = ['request_date', 'approved_date', 'fulfilled_date', 'updated_at']
    date_hierarchy = 'request_date'
    ordering = ['-request_date']
    
    fieldsets = (
        ('Requester Information', {
            'fields': ('requester_name', 'requester_phone', 'requester_email')
        }),
        ('Hospital Information', {
            'fields': ('hospital_name', 'hospital_address')
        }),
        ('Request Details', {
            'fields': ('blood_type', 'units_needed', 'priority', 'status', 'needed_by_date')
        }),
        ('Medical Information', {
            'fields': ('patient_name', 'patient_age', 'reason_for_request', 'doctor_name')
        }),
        ('Blood Bank Assignment', {
            'fields': ('assigned_blood_bank',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('request_date', 'approved_date', 'fulfilled_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        """Approve selected blood requests"""
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} blood request(s) were successfully approved.')
    approve_requests.short_description = "Approve selected blood requests"
    
    def reject_requests(self, request, queryset):
        """Reject selected blood requests"""
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} blood request(s) were successfully rejected.')
    reject_requests.short_description = "Reject selected blood requests"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('assigned_blood_bank')
