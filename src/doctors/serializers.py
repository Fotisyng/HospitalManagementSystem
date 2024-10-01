from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            'first_name',
            'last_name',
            'specialty',
            'phone_number',
            'email',
            'address',
            'license_number',
        ]
