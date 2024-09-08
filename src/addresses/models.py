from django.db import models


class Address(models.Model):
    class Meta:
        db_table = 'addresses'  # Set the table name to 'patients'

    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.country}"
