#defines database tables
#stores donor information

from django.db import models

class Donor(models.Model):
    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3)
    contact_number = models.CharField(max_length=15)

    country = models.CharField(max_length=50, default='India')
    state = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    class Meta:  
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'contact_number', 'city'],
                name='unique_donor'
            )
        ]

    def __str__(self):
        return self.name