from django import forms
from .models import Doctor, Patient


class AssignPatientsForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), label="Select Doctor")
    patients = forms.ModelMultipleChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Patients"
    )
