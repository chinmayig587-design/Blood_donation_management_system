from django import forms
from .models import Donor

class DonorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Donor
        # Specify all the fields you want in the registration form
        fields = ['name', 'blood_group', 'contact_number', 'country', 'state', 'district', 'city']