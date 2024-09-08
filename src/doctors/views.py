from django.shortcuts import render, redirect
from rest_framework import generics
from .models import Doctor
from addresses.models import Address
from .serializers import DoctorSerializer
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View


class DoctorCreateFormView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # Render a form template
        return render(request, 'doctor_form.html')

    def post(self, request, *args, **kwargs):
        # Extract address data
        address_data = {
            'country': request.POST.get('country'),
            'city': request.POST.get('city'),
            'state': request.POST.get('state'),
            'postal_code': request.POST.get('postal_code'),
            'street_address': request.POST.get('street_address'),
        }

        # Create Address instance
        address = Address.objects.create(**address_data)

        # Extract doctor data and add address instance
        doctor_data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'specialty': request.POST.get('specialty'),
            'phone_number': request.POST.get('phone_number'),
            'email': request.POST.get('email'),
            'address': address.pk,  # Use the primary key here
            'license_number': request.POST.get('license_number'),
            # Handle patients if applicable
            'patients': request.POST.getlist('patients')
        }

        serializer = DoctorSerializer(data=doctor_data)
        if serializer.is_valid():
            serializer.save()
            return render(request, 'doctor_form.html', {'success': 'Doctor created successfully!'})
        return render(request, 'doctor_form.html', {'errors': serializer.errors})
