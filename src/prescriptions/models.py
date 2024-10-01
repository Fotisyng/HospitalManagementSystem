from django.db import models
from patients.models import Patient


class Prescription(models.Model):
    class Meta:
        db_table = 'prescriptions'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.medication_name} for {self.patient} from {self.start_date} to {self.end_date}"
