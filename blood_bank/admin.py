from django.contrib import admin
from .models import BloodBank, BloodInventory, Donation

@admin.register(BloodBank)
class BloodBankAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'phone_number', 'email', 'is_active']
    list_filter = ['is_active', 'city', 'state']
    search_fields = ['name', 'address', 'city', 'state']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zip_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ['blood_bank', 'blood_type', 'units_available', 'units_reserved', 'total_units', 'last_updated']
    list_filter = ['blood_type', 'blood_bank', 'last_updated']
    search_fields = ['blood_bank__name']
    readonly_fields = ['last_updated']
    ordering = ['blood_bank__name', 'blood_type']

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor', 'blood_bank', 'donation_date', 'donation_time', 'status', 'units_collected']
    list_filter = ['status', 'donation_date', 'blood_bank', 'donor__blood_type']
    search_fields = ['donor__first_name', 'donor__last_name', 'blood_bank__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'donation_date'
    fieldsets = (
        ('Donation Details', {
            'fields': ('donor', 'blood_bank', 'donation_date', 'donation_time', 'status', 'units_collected')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('donor', 'blood_bank')
