from django.db import models
from django.core.validators import RegexValidator


class BasicInfo(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('Other', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^[0-9\(\)\[\]\.\-\*\/]+$',
                message='Phone number can only contain digits and the characters ()[] .-* /'
            )
        ]
    )
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()

    class Meta:
        abstract = True
