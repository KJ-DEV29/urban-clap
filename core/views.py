from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count, Sum
from .models import Contact, Enquiry, Review, UserProfile, BloodPurchase
from donors.models import Donor
from blood_bank.models import BloodBank, BloodInventory, Donation
from requests.models import BloodRequest

def home(request):
    """Home page view"""
    # Get statistics
    total_donors = Donor.objects.count()
    total_donations = Donation.objects.filter(status='completed').count()
    total_blood_banks = BloodBank.objects.filter(is_active=True).count()
    total_requests = BloodRequest.objects.count()
    
    # Get recent reviews
    recent_reviews = Review.objects.filter(is_approved=True)[:3]
    
    # Get blood inventory summary
    inventory_summary = BloodInventory.objects.values('blood_type').annotate(
        total_units=Sum('units_available')
    ).order_by('blood_type')
    
    context = {
        'total_donors': total_donors,
        'total_donations': total_donations,
        'total_blood_banks': total_blood_banks,
        'total_requests': total_requests,
        'recent_reviews': recent_reviews,
        'inventory_summary': inventory_summary,
    }
    return render(request, 'core/home.html', context)

def about(request):
    """About page view"""
    return render(request, 'core/about.html')

def services(request):
    """Services page view"""
    return render(request, 'core/services.html')

def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
        return redirect('core:contact')
    
    return render(request, 'core/contact.html')

def enquiry(request):
    """Enquiry page view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        enquiry_type = request.POST.get('enquiry_type')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        Enquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            enquiry_type=enquiry_type,
            subject=subject,
            message=message
        )
        
        messages.success(request, 'Your enquiry has been submitted successfully! We will respond soon.')
        return redirect('core:enquiry')
    
    return render(request, 'core/enquiry.html')

def review(request):
    """Review page view"""
    if request.user.is_authenticated:
        if request.method == 'POST':
            rating = request.POST.get('rating')
            title = request.POST.get('title')
            comment = request.POST.get('comment')
            
            Review.objects.create(
                user=request.user,
                rating=rating,
                title=title,
                comment=comment
            )
            
            messages.success(request, 'Your review has been submitted successfully! It will be visible after approval.')
            return redirect('core:review')
    else:
        messages.warning(request, 'Please login to submit a review.')
        return redirect('auth_app:login')  # Assuming your login URL is named 'login' in auth_app
    
    # Get approved reviews
    approved_reviews = Review.objects.filter(is_approved=True).order_by('-created_at')
    
    context = {
        'reviews': approved_reviews,
    }
    return render(request, 'core/review.html', context)

@login_required
def dashboard(request):
    """User dashboard view"""
    user = request.user
    
    # Get user-specific data
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    # Get user's donations if they are a donor
    user_donations = []
    if profile.is_donor:
        try:
            donor = Donor.objects.get(user=user)
            user_donations = Donation.objects.filter(donor=donor).order_by('-donation_date')[:5]
        except Donor.DoesNotExist:
            pass
    
    # Get user's blood purchases
    user_purchases = BloodPurchase.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Get user's reviews
    user_reviews = Review.objects.filter(user=user).order_by('-created_at')[:3]
    
    context = {
        'profile': profile,
        'user_donations': user_donations,
        'user_purchases': user_purchases,
        'user_reviews': user_reviews,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def donate_blood(request):
    """Donate blood view"""
    if request.method == 'POST':
        blood_bank_id = request.POST.get('blood_bank')
        donation_date = request.POST.get('donation_date')
        donation_time = request.POST.get('donation_time')
        notes = request.POST.get('notes', '')
        
        try:
            blood_bank = BloodBank.objects.get(id=blood_bank_id)
            
            # Check if user is a donor
            try:
                donor = Donor.objects.get(user=request.user)
            except Donor.DoesNotExist:
                messages.error(request, 'You need to register as a donor first.')
                return redirect('donors:register')  # Assuming donor registration is in donors app
            
            # Create donation
            Donation.objects.create(
                donor=donor,
                blood_bank=blood_bank,
                donation_date=donation_date,
                donation_time=donation_time,
                notes=notes,
                status='scheduled'
            )
            
            messages.success(request, 'Blood donation scheduled successfully!')
            return redirect('core:dashboard')
            
        except BloodBank.DoesNotExist:
            messages.error(request, 'Invalid blood bank selected.')
    
    blood_banks = BloodBank.objects.filter(is_active=True)
    context = {
        'blood_banks': blood_banks,
    }
    return render(request, 'core/donate_blood.html', context)

@login_required
def purchase_blood(request):
    """Purchase blood view"""
    if request.method == 'POST':
        blood_type = request.POST.get('blood_type')
        units_needed = int(request.POST.get('units_needed'))
        purpose = request.POST.get('purpose')
        hospital_name = request.POST.get('hospital_name')
        doctor_name = request.POST.get('doctor_name', '')
        patient_name = request.POST.get('patient_name', '')
        urgency_level = request.POST.get('urgency_level')
        
        # Price calculation
        base_price = 100.00  # Base price per unit
        urgency_multiplier = {
            'normal': 1.0,
            'urgent': 1.5,
            'emergency': 2.0
        }
        
        price_per_unit = base_price * urgency_multiplier.get(urgency_level, 1.0)
        total_price = price_per_unit * units_needed
        
        BloodPurchase.objects.create(
            user=request.user,
            blood_type=blood_type,
            units_needed=units_needed,
            purpose=purpose,
            hospital_name=hospital_name,
            doctor_name=doctor_name,
            patient_name=patient_name,
            urgency_level=urgency_level,
            price_per_unit=price_per_unit,
            total_price=total_price
        )
        
        messages.success(request, f'Blood purchase request submitted successfully! Total cost: ${total_price:.2f}')
        return redirect('core:dashboard')
    
    return render(request, 'core/purchase_blood.html')

@staff_member_required
def admin_dashboard(request):
    """Admin dashboard view"""
    # Get statistics for admin dashboard
    total_donors = Donor.objects.count()
    total_donations = Donation.objects.count()
    completed_donations = Donation.objects.filter(status='completed').count()
    pending_requests = BloodRequest.objects.filter(status='pending').count()
    pending_enquiries = Enquiry.objects.filter(status='pending').count()
    pending_reviews = Review.objects.filter(is_approved=False).count()
    
    # Get recent activities
    recent_donations = Donation.objects.select_related('donor', 'blood_bank').order_by('-created_at')[:5]
    recent_requests = BloodRequest.objects.select_related('assigned_blood_bank').order_by('-created_at')[:5]
    recent_enquiries = Enquiry.objects.order_by('-created_at')[:5]
    
    # Get blood inventory summary
    inventory_summary = BloodInventory.objects.values('blood_type').annotate(
        total_units=Sum('units_available')
    ).order_by('blood_type')
    
    context = {
        'total_donors': total_donors,
        'total_donations': total_donations,
        'completed_donations': completed_donations,
        'pending_requests': pending_requests,
        'pending_enquiries': pending_enquiries,
        'pending_reviews': pending_reviews,
        'recent_donations': recent_donations,
        'recent_requests': recent_requests,
        'recent_enquiries': recent_enquiries,
        'inventory_summary': inventory_summary,
    }
    return render(request, 'core/admin_dashboard.html', context)