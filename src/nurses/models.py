from django.db import models
from addresses.models import Address
from emergency_contacts.models import EmergencyContact
from common.models import BasicInfo
from django.core.exceptions import ValidationError
from django.utils import timezone


class Nurse(BasicInfo):

    class Meta:
        db_table = 'nurses'

    ROLE_CHOICES = [
        ('staff', 'Staff Nurse'),
        ('charge', 'Charge Nurse'),  # supervises nursing staff during a shift
        ('chief', 'Chief Nurse'),  # responsible for overall management of nursing staff in the facility
    ]

    DEPARTMENT_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('oncology', 'Oncology'),
        ('pediatrics', 'Pediatrics'),
        ('surgery', 'Surgery'),
        ('anesthesiology', 'Anesthesiology'),
        ('dermatology', 'Dermatology'),
        ('emergency_medicine', 'Emergency Medicine'),
        ('endocrinology', 'Endocrinology'),
        ('gastroenterology', 'Gastroenterology'),
        ('gynecology', 'Gynecology'),
        ('hematology', 'Hematology'),
        ('infectious_disease', 'Infectious Disease'),
        ('nephrology', 'Nephrology'),
        ('obstetrics', 'Obstetrics'),
        ('orthopedics', 'Orthopedics'),
        ('otolaryngology', 'Otolaryngology (ENT)'),
        ('pathology', 'Pathology'),
        ('psychiatry', 'Psychiatry'),
        ('pulmonology', 'Pulmonology'),
        ('radiology', 'Radiology'),
        ('rheumatology', 'Rheumatology'),
        ('urology', 'Urology'),
        ('vascular_surgery', 'Vascular Surgery'),
        ('plastic_surgery', 'Plastic Surgery'),
    ]
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    emergency_contact = models.OneToOneField(
        EmergencyContact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='nurse_contact'
    )
    license_number = models.CharField(max_length=100, unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, null=True, blank=True)
    hiring_end_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')
    date_hired = models.DateField()
    supervisor_nurses = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='supervised_by',
        blank=True
    )

    def clean(self):
        super().clean()  # Call the base class's clean method first

        if self.date_of_birth and self.date_hired:
            age_at_hiring = self.date_hired.year - self.date_of_birth.year - (
                    (self.date_hired.month, self.date_hired.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
            if age_at_hiring < 18:
                raise ValidationError({
                    'date_hired': 'Nurse must be at least 18 years old at the time of hiring.'
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
        return f"Nurse {self.first_name} {self.last_name} - {self.department}"
