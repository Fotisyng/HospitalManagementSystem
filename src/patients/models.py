from django.db import models
from addresses.models import Address
from emergency_contacts.models import EmergencyContact
from insurances.models import Insurance


class Patient(models.Model):
    class Meta:
        db_table = 'patients'  # Set the table name to 'patients'

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('N/A', 'Not Applicable'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
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
