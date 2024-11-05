from rest_framework import serializers
from .models import Doctor
from addresses.models import Address
from emergency_contacts.models import EmergencyContact
from rest_framework.validators import UniqueValidator


class DoctorSerializer(serializers.ModelSerializer):
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), allow_null=True)
    emergency_contact = serializers.PrimaryKeyRelatedField(queryset=EmergencyContact.objects.all(), allow_null=True)
    # Add custom unique validation message for license_number field
    license_number = serializers.CharField(
        max_length=100,
        validators=[
            UniqueValidator(
                queryset=Doctor.objects.all(),
                message="A doctor with this license number already exists."
            )
        ]
    )

    class Meta:
        model = Doctor
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'gender',
            'date_of_birth',
            'specialty',
            'license_number',
            'date_hired',
            'hiring_end_date',
            'address',
            'emergency_contact',
        ]

    def validate(self, data):
        doctor_instance = Doctor(**data)
        doctor_instance.clean()
        return data

    def create(self, validated_data):
        return Doctor.objects.create(**validated_data)
