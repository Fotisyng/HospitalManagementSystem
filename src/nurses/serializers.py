from rest_framework import serializers
from .models import Nurse
from addresses.models import Address
from emergency_contacts.models import EmergencyContact
from rest_framework.validators import UniqueValidator


class NurseSerializer(serializers.ModelSerializer):
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), allow_null=True)
    emergency_contact = serializers.PrimaryKeyRelatedField(queryset=EmergencyContact.objects.all(), allow_null=True)
    # Add custom unique validation message for license_number field
    license_number = serializers.CharField(
        max_length=100,
        validators=[
            UniqueValidator(
                queryset=Nurse.objects.all(),
                message="A nurse with this license number already exists."
            )
        ]
    )
    class Meta:
        model = Nurse
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'phone_number', 'email', 'gender', 'license_number',
            'role', 'date_hired', 'hiring_end_date', 'department', 'address', 'emergency_contact'
        ]

    def validate(self, data):
        nurse_instance = Nurse(**data)
        nurse_instance.clean()
        return data

    def create(self, validated_data):
        return Nurse.objects.create(**validated_data)