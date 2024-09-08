from django.db import models


class Insurance(models.Model):
    class Meta:
        db_table = 'insurances'

    provider = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    coverage_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.provider} - {self.policy_number}"
