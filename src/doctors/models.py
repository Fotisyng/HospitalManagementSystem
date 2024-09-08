from django.db import models
from addresses.models import Address
from patients.models import Patient


class Doctor(models.Model):
    class Meta:
        db_table = 'doctors'

    SPECIALTY_CHOICES = [
        ('GP', 'General Practitioner'),
        ('Cardiologist', 'Cardiologist'),
        ('Neurologist', 'Neurologist'),
        ('Dermatologist', 'Dermatologist'),
        # Add more specialties as needed
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    license_number = models.CharField(max_length=100, unique=True)  # Unique license number for the doctor
    patients = models.ManyToManyField(Patient, related_name='doctors', null=True)  # Many-to-many relationship

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.specialty}"
