from django.db import models
from common.models import BasicInfo
from addresses.models import Address
from emergency_contacts.models import EmergencyContact
from patients.models import Patient
from django.core.exceptions import ValidationError
from django.utils import timezone

class Doctor(BasicInfo):
    class Meta:
        db_table = 'doctors'

    SPECIALTY_CHOICES = [
        ('GP', 'General Practitioner'),
        ('Cardiologist', 'Cardiologist'),
        ('Neurologist', 'Neurologist'),
        ('Dermatologist', 'Dermatologist'),
        ('Radiologist', 'Radiologist'),
        ('Pediatrician', 'Pediatrician'),
        ('Oncologist', 'Oncologist'),
        ('Orthopedist', 'Orthopedist'),
        ('Ophthalmologist', 'Ophthalmologist'),
        ('Psychiatrist', 'Psychiatrist'),
        ('Endocrinologist', 'Endocrinologist'),
        ('Rheumatologist', 'Rheumatologist'),
        ('Gastroenterologist', 'Gastroenterologist'),
        ('Nephrologist', 'Nephrologist'),
        ('Pulmonologist', 'Pulmonologist'),
        ('Urologist', 'Urologist'),
        ('Hematologist', 'Hematologist'),
        ('Anesthesiologist', 'Anesthesiologist'),
        ('Plastic Surgeon', 'Plastic Surgeon'),
        ('Obstetrician', 'Obstetrician'),
        ('Gynecologist', 'Gynecologist'),
    ]

    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES)
    date_hired = models.DateField()
    hiring_end_date = models.DateField(null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    emergency_contact = models.OneToOneField(
        EmergencyContact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='doctor_contact'
    )
    license_number = models.CharField(max_length=100, unique=True)  # Unique license number for the doctor
    patients = models.ManyToManyField(Patient, related_name='doctors')  # Many-to-many relationship

    def clean(self):
        super().clean()  # Call the base class's clean method first

        if self.date_of_birth and self.date_hired:
            age_at_hiring = self.date_hired.year - self.date_of_birth.year - (
                    (self.date_hired.month, self.date_hired.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
            if age_at_hiring < 18:
                raise ValidationError({
                    'date_hired': 'Doctor must be at least 18 years old at the time of hiring.'
                })

        if self.hiring_end_date and self.date_hired:
            if self.hiring_end_date <= self.date_hired:
                raise ValidationError({
                    'hiring_end_date': 'Hiring end date cannot be earlier than the hiring date.'
                })

        if self.hiring_end_date and self.hiring_end_date <= timezone.now().date():
            raise ValidationError({
                'hiring_end_date': 'Hiring end date must be after the current date.'
            })

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.specialty}"
