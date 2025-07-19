from django.contrib import admin
from .models import Contact, Enquiry, Review, UserProfile, BloodPurchase

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} contact(s) marked as read.')
    mark_as_read.short_description = "Mark selected contacts as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} contact(s) marked as unread.')
    mark_as_unread.short_description = "Mark selected contacts as unread"

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'enquiry_type', 'status', 'created_at']
    list_filter = ['enquiry_type', 'status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['mark_as_resolved', 'mark_as_closed']
    
    fieldsets = (
        ('Enquiry Information', {
            'fields': ('name', 'email', 'phone', 'enquiry_type', 'subject', 'message')
        }),
        ('Status Management', {
            'fields': ('status', 'admin_response')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(status='resolved')
        self.message_user(request, f'{updated} enquiry(ies) marked as resolved.')
    mark_as_resolved.short_description = "Mark selected enquiries as resolved"
    
    def mark_as_closed(self, request, queryset):
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} enquiry(ies) marked as closed.')
    mark_as_closed.short_description = "Mark selected enquiries as closed"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'title', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'title', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} review(s) approved.')
    approve_reviews.short_description = "Approve selected reviews"
    
    def disapprove_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} review(s) disapproved.')
    disapprove_reviews.short_description = "Disapprove selected reviews"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'is_donor', 'is_staff_member', 'created_at']
    list_filter = ['is_donor', 'is_staff_member', 'city', 'state', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone', 'city']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone', 'date_of_birth')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zip_code')
        }),
        ('Profile Picture', {
            'fields': ('profile_picture',)
        }),
        ('Status', {
            'fields': ('is_donor', 'is_staff_member')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(BloodPurchase)
class BloodPurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'blood_type', 'units_needed', 'urgency_level', 'status', 'total_amount', 'created_at']
    list_filter = ['blood_type', 'urgency_level', 'status', 'created_at']
    search_fields = ['user__username', 'hospital_name', 'patient_name', 'doctor_name']
    readonly_fields = ['total_amount', 'created_at', 'updated_at']
    actions = ['approve_purchases', 'complete_purchases', 'cancel_purchases']
    
    fieldsets = (
        ('Purchase Information', {
            'fields': ('user', 'blood_type', 'units_needed', 'purpose')
        }),
        ('Medical Information', {
            'fields': ('hospital_name', 'doctor_name', 'patient_name', 'urgency_level')
        }),
        ('Financial Information', {
            'fields': ('price_per_unit', 'total_amount')
        }),
        ('Status Management', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def approve_purchases(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} purchase(s) approved.')
    approve_purchases.short_description = "Approve selected purchases"
    
    def complete_purchases(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} purchase(s) completed.')
    complete_purchases.short_description = "Complete selected purchases"
    
    def cancel_purchases(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} purchase(s) cancelled.')
    cancel_purchases.short_description = "Cancel selected purchases"
