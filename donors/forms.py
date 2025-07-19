from django import forms
from .models import Donor

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'blood_type', 'date_of_birth', 'gender', 'address',
            'city', 'state', 'zip_code', 'is_eligible'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Make email field required
        self.fields['email'].required = True
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email already exists (excluding current instance for updates)
            existing_donor = Donor.objects.filter(email=email)
            if self.instance.pk:
                existing_donor = existing_donor.exclude(pk=self.instance.pk)
            
            if existing_donor.exists():
                raise forms.ValidationError('A donor with this email already exists.')
        
        return email
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            from datetime import date
            today = date.today()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            
            if age < 18:
                raise forms.ValidationError('Donor must be at least 18 years old.')
            elif age > 65:
                raise forms.ValidationError('Donor must be 65 years old or younger.')
        
        return date_of_birth 