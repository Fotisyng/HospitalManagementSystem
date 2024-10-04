from django.db import models
from addresses.models import Address
from emergency_contacts.models import EmergencyContact


class Nurse(models.Model):

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

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    emergency_contact = models.OneToOneField(
        EmergencyContact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='nurse_contact'
    )
    license_number = models.CharField(max_length=100, unique=True)  # Unique license number for the nurse
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, null=True, blank=True)  # Updated to use choices
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')  # Nurse's role (chief, staff, etc.)
    date_hired = models.DateField()  # Date the nurse was hired
    date_ended = models.DateField(null=True, blank=True)  # End date of employment, optional
    supervised_nurses = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='supervised_by',
        blank=True
    )  # Nurses supervised by this nurse

    def __str__(self):
        return f"Nurse {self.first_name} {self.last_name} - {self.department}"
