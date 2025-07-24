from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Donor
from .forms import DonorForm

def donor_list(request):
    """Display list of all donors"""
    donors = Donor.objects.all()
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        donors = donors.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(blood_type__icontains=query)
        )
    
    # Filter by blood type
    blood_type = request.GET.get('blood_type')
    if blood_type:
        donors = donors.filter(blood_type=blood_type)
    
    context = {
        'donors': donors,
        'blood_types': Donor.BLOOD_TYPES,   
    }
    return render(request, 'donors/donor_list.html', context)

def donor_register(request):
    """Register a new donor"""
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            donor = form.save()
            messages.success(request, f'Donor {donor.full_name} registered successfully!')
            return redirect('donors:donor_detail', donor_id=donor.id)
    else:
        form = DonorForm()
    
    context = {
        'form': form,
        'title': 'Register New Donor'
    }
    return render(request, 'donors/donor_form.html', context)

def donor_detail(request, donor_id):
    """Display donor details"""
    donor = get_object_or_404(Donor, id=donor_id)
    context = {
        'donor': donor,
    }
    return render(request, 'donors/donor_detail.html', context)

def donor_edit(request, donor_id):
    """Edit donor information"""
    donor = get_object_or_404(Donor, id=donor_id)
    
    if request.method == 'POST':
        form = DonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Donor {donor.full_name} updated successfully!')
            return redirect('donors:donor_detail', donor_id=donor.id)
    else:
        form = DonorForm(instance=donor)
    
    context = {
        'form': form,
        'donor': donor,
        'title': f'Edit {donor.full_name}'
    }
    return render(request, 'donors/donor_form.html', context)

def donor_delete(request, donor_id):
    """Delete a donor"""
    donor = get_object_or_404(Donor, id=donor_id)
    
    if request.method == 'POST':
        donor_name = donor.full_name
        donor.delete()
        messages.success(request, f'Donor {donor_name} deleted successfully!')
        return redirect('donors:register')  # or any valid URL name
    
    context = {
        'donor': donor,
    }
    return render(request, 'donors/donor_confirm_delete.html', context)

def donor_search(request):
    """Search donors"""
    query = request.GET.get('q', '')
    donors = Donor.objects.all()
    
    if query:
        donors = donors.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(blood_type__icontains=query)
        )
    
    context = {
        'donors': donors,
        'query': query,
    }
    return render(request, 'donors/donor_search.html', context)

def register(request):
    # You can add your registration logic here
    return render(request, 'donors/register.html')
