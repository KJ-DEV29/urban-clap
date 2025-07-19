from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import BloodBank, BloodInventory, Donation
from donors.models import Donor

# Create your views here.

def blood_bank_list(request):
    """Display list of all blood banks"""
    blood_banks = BloodBank.objects.filter(is_active=True)
    context = {
        'blood_banks': blood_banks,
    }
    return render(request, 'blood_bank/blood_bank_list.html', context)

def inventory_list(request):
    """Display blood inventory across all blood banks"""
    inventory = BloodInventory.objects.select_related('blood_bank').all()
    
    # Filter by blood bank
    blood_bank_id = request.GET.get('blood_bank')
    if blood_bank_id:
        inventory = inventory.filter(blood_bank_id=blood_bank_id)
    
    # Filter by blood type
    blood_type = request.GET.get('blood_type')
    if blood_type:
        inventory = inventory.filter(blood_type=blood_type)
    
    context = {
        'inventory': inventory,
        'blood_banks': BloodBank.objects.filter(is_active=True),
        'blood_types': BloodInventory.BLOOD_TYPES,
    }
    return render(request, 'blood_bank/inventory_list.html', context)

def donation_list(request):
    """Display list of all donations"""
    donations = Donation.objects.select_related('donor', 'blood_bank').all()
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        donations = donations.filter(status=status)
    
    # Filter by blood bank
    blood_bank_id = request.GET.get('blood_bank')
    if blood_bank_id:
        donations = donations.filter(blood_bank_id=blood_bank_id)
    
    context = {
        'donations': donations,
        'blood_banks': BloodBank.objects.filter(is_active=True),
        'status_choices': Donation.STATUS_CHOICES,
    }
    return render(request, 'blood_bank/donation_list.html', context)

def donation_create(request):
    """Create a new donation"""
    if request.method == 'POST':
        # Handle donation creation
        donor_id = request.POST.get('donor')
        blood_bank_id = request.POST.get('blood_bank')
        donation_date = request.POST.get('donation_date')
        donation_time = request.POST.get('donation_time')
        units_collected = request.POST.get('units_collected', 1)
        
        try:
            donor = Donor.objects.get(id=donor_id)
            blood_bank = BloodBank.objects.get(id=blood_bank_id)
            
            donation = Donation.objects.create(
                donor=donor,
                blood_bank=blood_bank,
                donation_date=donation_date,
                donation_time=donation_time,
                units_collected=units_collected,
                status='scheduled'
            )
            
            messages.success(request, f'Donation scheduled for {donor.full_name}')
            return redirect('blood_bank:donation_detail', donation_id=donation.id)
            
        except (Donor.DoesNotExist, BloodBank.DoesNotExist):
            messages.error(request, 'Invalid donor or blood bank selected.')
    
    context = {
        'donors': Donor.objects.filter(is_eligible=True),
        'blood_banks': BloodBank.objects.filter(is_active=True),
    }
    return render(request, 'blood_bank/donation_form.html', context)

def donation_detail(request, donation_id):
    """Display donation details"""
    donation = get_object_or_404(Donation, id=donation_id)
    context = {
        'donation': donation,
    }
    return render(request, 'blood_bank/donation_detail.html', context)

def donation_edit(request, donation_id):
    """Edit donation information"""
    donation = get_object_or_404(Donation, id=donation_id)
    
    if request.method == 'POST':
        # Handle donation update
        donation.donation_date = request.POST.get('donation_date')
        donation.donation_time = request.POST.get('donation_time')
        donation.status = request.POST.get('status')
        donation.units_collected = request.POST.get('units_collected', 1)
        donation.notes = request.POST.get('notes', '')
        donation.save()
        
        messages.success(request, 'Donation updated successfully!')
        return redirect('blood_bank:donation_detail', donation_id=donation.id)
    
    context = {
        'donation': donation,
        'status_choices': Donation.STATUS_CHOICES,
    }
    return render(request, 'blood_bank/donation_form.html', context)

def donation_delete(request, donation_id):
    """Delete a donation"""
    donation = get_object_or_404(Donation, id=donation_id)
    
    if request.method == 'POST':
        donation.delete()
        messages.success(request, 'Donation deleted successfully!')
        return redirect('blood_bank:donation_list')
    
    context = {
        'donation': donation,
    }
    return render(request, 'blood_bank/donation_confirm_delete.html', context)
