from django.db import models
from addresses.models import Address
from common.models import BasicInfo
from django.core.validators import RegexValidator


class EmergencyContact(BasicInfo):  # Inherit from BasicInfo
    class Meta:
        db_table = 'emergency_contacts'  # Set the table name to 'emergency_contacts'

    secondary_phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^[0-9\(\)\[\]\.\-\*\/]+$',
                message='Phone number can only contain digits and the characters ()[] .-* /'
            )
        ]
    )
    relationship = models.CharField(max_length=50, blank=True, null=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone_number}"
