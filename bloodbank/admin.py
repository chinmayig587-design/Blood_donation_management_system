from django.contrib import admin
from .models import Donor 
@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    # Optional: Customize the list view in the admin panel
    list_display = ('name', 'blood_group', 'contact_number') 
    

