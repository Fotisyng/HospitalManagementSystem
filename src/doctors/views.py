from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from rest_framework import generics
from .models import Doctor
from addresses.models import Address, Country
from .serializers import DoctorSerializer
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction



class DoctorCreateFormView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # Fetch countries from the database
        countries = Country.objects.all().order_by('name')

        # Render a form template
        context = {
            'specialty_choices': Doctor.SPECIALTY_CHOICES,
            'countries': countries  # Pass countries to the template
        }
        return render(request, 'doctor_form.html', context)

    def post(self, request, *args, **kwargs):
        # Extract address data
        address_data = {
            'country': request.POST.get('country'),
            'city': request.POST.get('city'),
            'state': request.POST.get('state'),
            'postal_code': request.POST.get('postal_code'),
            'street_address': request.POST.get('street_address'),
        }

        # Extract doctor data and add address instance
        doctor_data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'specialty': request.POST.get('specialty'),
            'phone_number': request.POST.get('phone_number'),
            'email': request.POST.get('email'),
            'license_number': request.POST.get('license_number'),
            'patients': request.POST.getlist('patients')
        }

        try:
            with transaction.atomic():
                # Create Address instance
                address = Address(**address_data)
                address.full_clean()  # This will trigger the clean() method, validating the country
                address.save()

                # Add address to doctor data
                doctor_data['address'] = address.pk

                serializer = DoctorSerializer(data=doctor_data)
                if serializer.is_valid():
                    serializer.save()
                    # Render success page
                    countries = Country.objects.all().order_by('name')
                    return render(request, 'doctor_form.html',
                                  {'success': 'Doctor created successfully!', 'countries': countries})
                else:
                    # If serializer is not valid, raise an exception to trigger rollback
                    raise ValidationError(serializer.errors)

        except ValidationError as e:
            # Handle errors and rollback
            countries = Country.objects.all().order_by('name')
            return render(request, 'doctor_form.html', {'errors': e.message_dict, 'countries': countries})


class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctor_list.html'  # The template that will render the list
    context_object_name = 'doctors'  # The name to access the list in the template


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'doctor_detail.html'
    context_object_name = 'doctor'


class DoctorUpdateView(UpdateView):
    model = Doctor
    fields = ['first_name', 'last_name', 'specialty', 'phone_number', 'email', 'license_number']  # Add other fields as needed
    template_name = 'doctor_update_form.html'
    success_url = '/doctors/list'  # Redirect to the doctor list or detail after successful update


class DoctorDeleteView(DeleteView):
    model = Doctor
    template_name = 'doctor_confirm_delete.html'  # Create this template for delete confirmation
    success_url = reverse_lazy('doctor-list')  # Redirect to doctor list after successful deletion