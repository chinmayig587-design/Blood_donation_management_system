# mysite/bloodbank/views.py
# handles all backend logic
#it is brain of project
# save data and fetch data
#bridge between frontend and database

from django.shortcuts import render,redirect
from .models import Donor # Import your Donor model
from . forms import DonorRegistrationForm
from django.contrib import messages


def home(request):
    """View for the home page."""
    return render(request, 'bloodbank/home.html')

def search_results(request):
    """Handles donor search logic and displays results."""
    # Retrieve the search terms from the form submission
    blood_group = request.GET.get('blood_group')
    country = request.GET.get('country')
    state = request.GET.get('state')
    district = request.GET.get('district')
    city = request.GET.get('city')
    
    queryset = Donor.objects.all()
    
    if blood_group:
        queryset = queryset.filter(blood_group__iexact=blood_group) 
    if country:
        queryset = queryset.filter(country__icontains=country)
    if state:
        queryset = queryset.filter(state__icontains=state)
    if district:
        queryset = queryset.filter(district__icontains=district)
    if city:
        queryset = queryset.filter(city__icontains=city)
        
    context = {
        'donors': queryset, 
        'blood_group': blood_group,
        'search_location': ', '.join(
            value for value in (city, district, state, country) if value
        ),
    }
    
    return render(request, 'bloodbank/search_results.html', context)

def register(request):
    if request.method == "POST":
        form = DonorRegistrationForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get("name")
            contact_number = form.cleaned_data.get("contact_number")
            city = form.cleaned_data.get("city")

            if Donor.objects.filter(
                name=name, contact_number=contact_number, city=city
            ).exists():
                messages.error(request, "Donor already exists with same details!")
            else:
                form.save()
                messages.success(request, "Registration successful!")
                return redirect("home")
    else:
        form = DonorRegistrationForm()

    context = {"form": form}
    return render(request, "bloodbank/register.html", context)