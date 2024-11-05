from django.db import models
from addresses.models import Address
from emergency_contacts.models import EmergencyContact
from insurances.models import Insurance
from common.models import BasicInfo


class Patient(BasicInfo):
    class Meta:
        db_table = 'patients'  # Set the table name to 'patients'

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    ]

    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    emergency_contact = models.OneToOneField(
        EmergencyContact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='patient_contact'
    )
    medical_history = models.TextField(blank=True, null=True)
    insurance_provider = models.OneToOneField(Insurance, on_delete=models.CASCADE, related_name='insurance')
    last_visit_date = models.DateField(null=True, blank=True)
    allergies = models.TextField(blank=True, null=True)
    registration_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
