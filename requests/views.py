from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import BloodRequest
from blood_bank.models import BloodBank

def request_list(request):
    """Display list of all blood requests"""
    requests = BloodRequest.objects.select_related('assigned_blood_bank').all()
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        requests = requests.filter(status=status)
    
    # Filter by priority
    priority = request.GET.get('priority')
    if priority:
        requests = requests.filter(priority=priority)
    
    # Filter by blood type
    blood_type = request.GET.get('blood_type')
    if blood_type:
        requests = requests.filter(blood_type=blood_type)
    
    context = {
        'requests': requests,
        'status_choices': BloodRequest.STATUS_CHOICES,
        'priority_choices': BloodRequest.PRIORITY_CHOICES,
        'blood_types': BloodRequest.BLOOD_TYPES,
    }
    return render(request, 'requests/request_list.html', context)

def request_create(request):
    """Create a new blood request"""
    if request.method == 'POST':
        # Handle request creation
        requester_name = request.POST.get('requester_name')
        requester_phone = request.POST.get('requester_phone')
        requester_email = request.POST.get('requester_email')
        hospital_name = request.POST.get('hospital_name')
        hospital_address = request.POST.get('hospital_address')
        blood_type = request.POST.get('blood_type')
        units_needed = request.POST.get('units_needed')
        priority = request.POST.get('priority')
        patient_name = request.POST.get('patient_name')
        patient_age = request.POST.get('patient_age')
        reason_for_request = request.POST.get('reason_for_request')
        doctor_name = request.POST.get('doctor_name')
        needed_by_date = request.POST.get('needed_by_date')
        
        try:
            request_obj = BloodRequest.objects.create(
                requester_name=requester_name,
                requester_phone=requester_phone,
                requester_email=requester_email,
                hospital_name=hospital_name,
                hospital_address=hospital_address,
                blood_type=blood_type,
                units_needed=units_needed,
                priority=priority,
                patient_name=patient_name,
                patient_age=patient_age if patient_age else None,
                reason_for_request=reason_for_request,
                doctor_name=doctor_name,
                needed_by_date=needed_by_date
            )
            
            messages.success(request, f'Blood request created for {hospital_name}')
            return redirect('requests:request_detail', request_id=request_obj.id)
            
        except Exception as e:
            messages.error(request, f'Error creating request: {str(e)}')
    
    context = {
        'blood_types': BloodRequest.BLOOD_TYPES,
        'priority_choices': BloodRequest.PRIORITY_CHOICES,
    }
    return render(request, 'requests/request_form.html', context)

def request_detail(request, request_id):
    """Display blood request details"""
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    context = {
        'blood_request': blood_request,
    }
    return render(request, 'requests/request_detail.html', context)

def request_edit(request, request_id):
    """Edit blood request information"""
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    
    if request.method == 'POST':
        # Handle request update
        blood_request.requester_name = request.POST.get('requester_name')
        blood_request.requester_phone = request.POST.get('requester_phone')
        blood_request.requester_email = request.POST.get('requester_email')
        blood_request.hospital_name = request.POST.get('hospital_name')
        blood_request.hospital_address = request.POST.get('hospital_address')
        blood_request.blood_type = request.POST.get('blood_type')
        blood_request.units_needed = request.POST.get('units_needed')
        blood_request.priority = request.POST.get('priority')
        blood_request.patient_name = request.POST.get('patient_name')
        blood_request.patient_age = request.POST.get('patient_age')
        blood_request.reason_for_request = request.POST.get('reason_for_request')
        blood_request.doctor_name = request.POST.get('doctor_name')
        blood_request.needed_by_date = request.POST.get('needed_by_date')
        blood_request.notes = request.POST.get('notes', '')
        blood_request.save()
        
        messages.success(request, 'Blood request updated successfully!')
        return redirect('requests:request_detail', request_id=blood_request.id)
    
    context = {
        'blood_request': blood_request,
        'blood_types': BloodRequest.BLOOD_TYPES,
        'priority_choices': BloodRequest.PRIORITY_CHOICES,
    }
    return render(request, 'requests/request_form.html', context)

def request_delete(request, request_id):
    """Delete a blood request"""
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    
    if request.method == 'POST':
        hospital_name = blood_request.hospital_name
        blood_request.delete()
        messages.success(request, f'Blood request for {hospital_name} deleted successfully!')
        return redirect('requests:request_list')
    
    context = {
        'blood_request': blood_request,
    }
    return render(request, 'requests/request_confirm_delete.html', context)

def request_approve(request, request_id):
    """Approve a blood request"""
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    
    if request.method == 'POST':
        blood_bank_id = request.POST.get('blood_bank')
        try:
            blood_bank = BloodBank.objects.get(id=blood_bank_id)
            blood_request.approve(blood_bank)
            messages.success(request, f'Blood request approved and assigned to {blood_bank.name}')
        except BloodBank.DoesNotExist:
            messages.error(request, 'Invalid blood bank selected.')
    
    context = {
        'blood_request': blood_request,
        'blood_banks': BloodBank.objects.filter(is_active=True),
    }
    return render(request, 'requests/request_approve.html', context)

def request_reject(request, request_id):
    """Reject a blood request"""
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    
    if request.method == 'POST':
        blood_request.reject()
        messages.success(request, 'Blood request rejected successfully!')
        return redirect('requests:request_detail', request_id=blood_request.id)
    
    context = {
        'blood_request': blood_request,
    }
    return render(request, 'requests/request_confirm_reject.html', context)

def request_fulfill(request, request_id):
    """Fulfill a blood request"""
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    
    if request.method == 'POST':
        blood_request.fulfill()
        messages.success(request, 'Blood request fulfilled successfully!')
        return redirect('requests:request_detail', request_id=blood_request.id)
    
    context = {
        'blood_request': blood_request,
    }
    return render(request, 'requests/request_confirm_fulfill.html', context)
