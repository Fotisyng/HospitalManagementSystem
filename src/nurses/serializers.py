from rest_framework import serializers
from .models import Nurse
from addresses.models import Address
from emergency_contacts.models import EmergencyContact


class NurseSerializer(serializers.ModelSerializer):
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
    emergency_contact = serializers.PrimaryKeyRelatedField(queryset=EmergencyContact.objects.all())

    class Meta:
        model = Nurse
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'phone_number', 'email', 'license_number',
            'role', 'date_hired', 'department', 'address', 'emergency_contact'
        ]
