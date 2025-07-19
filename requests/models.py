from django.db import models
from blood_bank.models import BloodBank

# Create your models here.

class BloodRequest(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('fulfilled', 'Fulfilled'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Requester Information
    requester_name = models.CharField(max_length=200)
    requester_phone = models.CharField(max_length=15)
    requester_email = models.EmailField()
    hospital_name = models.CharField(max_length=200)
    hospital_address = models.TextField()
    
    # Request Details
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    units_needed = models.PositiveIntegerField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Medical Information
    patient_name = models.CharField(max_length=200, blank=True)
    patient_age = models.PositiveIntegerField(null=True, blank=True)
    reason_for_request = models.TextField()
    doctor_name = models.CharField(max_length=200, blank=True)
    
    # Timing
    needed_by_date = models.DateField()
    request_date = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    fulfilled_date = models.DateTimeField(null=True, blank=True)
    
    # Blood Bank Assignment
    assigned_blood_bank = models.ForeignKey(
        BloodBank, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='blood_requests'
    )
    
    # Additional Information
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-request_date']
    
    def __str__(self):
        return f"{self.hospital_name} - {self.blood_type} ({self.units_needed} units) - {self.status}"
    
    @property
    def is_urgent(self):
        return self.priority == 'urgent'
    
    @property
    def days_until_needed(self):
        from datetime import date
        today = date.today()
        return (self.needed_by_date - today).days
    
    def approve(self, blood_bank):
        """Approve the blood request and assign a blood bank"""
        from django.utils import timezone
        self.status = 'approved'
        self.assigned_blood_bank = blood_bank
        self.approved_date = timezone.now()
        self.save()
    
    def fulfill(self):
        """Mark the request as fulfilled"""
        from django.utils import timezone
        self.status = 'fulfilled'
        self.fulfilled_date = timezone.now()
        self.save()
        
        # Update blood inventory
        if self.assigned_blood_bank:
            inventory = self.assigned_blood_bank.inventory.filter(blood_type=self.blood_type).first()
            if inventory and inventory.units_available >= self.units_needed:
                inventory.units_available -= self.units_needed
                inventory.save()
    
    def reject(self):
        """Reject the blood request"""
        self.status = 'rejected'
        self.save()
