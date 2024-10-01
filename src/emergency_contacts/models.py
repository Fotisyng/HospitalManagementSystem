from django.db import models
from addresses.models import Address


class EmergencyContact(models.Model):
    class Meta:
        db_table = 'emergency_contacts'  # Set the table name to 'patients'

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    mobile_phone_number = models.CharField(max_length=15)
    relationship = models.CharField(max_length=50, blank=True, null=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.phone_number}"
