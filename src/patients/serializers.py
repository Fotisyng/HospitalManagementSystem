from rest_framework import serializers
from .models import Patient
from doctors.models import Doctor
from addresses.models import Address
from emergency_contacts.models import EmergencyContact
from insurances.models import Insurance

class PatientSerializer(serializers.ModelSerializer):
    # These will now accept the primary keys (foreign key relationships)
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
    emergency_contact = serializers.PrimaryKeyRelatedField(queryset=EmergencyContact.objects.all())
    insurance_provider = serializers.PrimaryKeyRelatedField(queryset=Insurance.objects.all())
    doctors = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), many=True)

    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number', 'email', 'status',
            'address', 'emergency_contact', 'insurance_provider', 'doctors'
        ]
