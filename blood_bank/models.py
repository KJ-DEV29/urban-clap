from django.db import models
from donors.models import Donor

# Create your models here.

class BloodBank(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class BloodInventory(models.Model):
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
    
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name='inventory')
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    units_available = models.PositiveIntegerField(default=0)
    units_reserved = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['blood_bank', 'blood_type']
        ordering = ['blood_type']
    
    def __str__(self):
        return f"{self.blood_bank.name} - {self.blood_type} ({self.units_available} units)"
    
    @property
    def total_units(self):
        return self.units_available + self.units_reserved

class Donation(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donations')
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name='donations')
    donation_date = models.DateField()
    donation_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    units_collected = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-donation_date', '-donation_time']
    
    def __str__(self):
        return f"{self.donor.full_name} - {self.donation_date} ({self.status})"
    
    def save(self, *args, **kwargs):
        # Update donor's last donation date and total donations when donation is completed
        if self.status == 'completed' and self.pk is None:
            self.donor.last_donation_date = self.donation_date
            self.donor.total_donations += self.units_collected
            self.donor.save()
            
            # Update blood inventory
            inventory, created = BloodInventory.objects.get_or_create(
                blood_bank=self.blood_bank,
                blood_type=self.donor.blood_type,
                defaults={'units_available': 0}
            )
            inventory.units_available += self.units_collected
            inventory.save()
        
        super().save(*args, **kwargs)
