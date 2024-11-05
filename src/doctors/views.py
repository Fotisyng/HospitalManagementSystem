from .models import Doctor
from .serializers import DoctorSerializer
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from hospitalManagementSystem.views import BaseCreateView
from common.utils import create_address, create_emergency_contact
from django.core.exceptions import ValidationError as DjangoValidationError



class DoctorCreateFormView(BaseCreateView):
    template_name = 'doctor_form.html'
    success_message = 'Doctor registered successfully!'

    def get_context_data(self):
        """Extends the base context with additional doctor-specific context data."""
        context = super().get_context_data()
        specialty_choices = Doctor.SPECIALTY_CHOICES
        gender_choices = Doctor.GENDER_CHOICES

        context.update({
            'gender_choices': gender_choices,
            'specialty_choices': specialty_choices,
        })

        return context

    def create_related_models(self, data):
        """Handles doctor-specific related model creation. The doctor address and
        emergency_contact are also created along with the doctor object."""
        errors = {}
        address = None
        try:
            if all(data.get(field) for field in ['country', 'city', 'postal_code']):
                address_data = {
                    'country': data.get('country'),
                    'city': data.get('city'),
                    'state': data.get('state'),
                    'postal_code': data.get('postal_code'),
                    'street_address': data.get('street_address'),
                }
                address = create_address(address_data)
            else:
                address = None
        except DjangoValidationError as e:
            errors['address'] = {
                'messages': [str(error) for error in e.error_list]}  # or str(e) if you prefer a string format
        # Create Address for the emergency contact
        emergency_contact_address = None
        try:
            if all(data.get(field, '').strip() for field in
                   ['emergency_contact_country', 'emergency_contact_city', 'emergency_contact_postal_code']):
                emergency_contact_address_data = {
                    'country': data.get('emergency_contact_country'),
                    'city': data.get('emergency_contact_city'),
                    'state': data.get('emergency_contact_state'),
                    'postal_code': data.get('emergency_contact_postal_code'),
                    'street_address': data.get('emergency_contact_street_address'),
                }
                emergency_contact_address = create_address(emergency_contact_address_data)
            else:
                emergency_contact_address = None
        except DjangoValidationError as e:
            # If emergency contact address validation fails, store the error
            errors['emergency_contact_address'] = {'messages': [str(error) for error in e.error_list]}

        # Create Emergency Contact
        emergency_contact = None
        if all(data.get(field, '').strip() for field in
               ['emergency_contact_first_name', 'emergency_contact_last_name', 'emergency_contact_phone_number',
                'emergency_contact_relationship', 'emergency_contact_secondary_phone_number',
                'emergency_contact_date_of_birth', 'emergency_contact_gender', 'emergency_contact_email']):
            emergency_contact_data = {
                'first_name': data.get('emergency_contact_first_name'),
                'last_name': data.get('emergency_contact_last_name'),
                'email': data.get('emergency_contact_email'),
                'date_of_birth': data.get('emergency_contact_date_of_birth'),
                'gender': data.get('emergency_contact_gender'),
                'phone_number': data.get('emergency_contact_phone_number'),
                'secondary_phone_number': data.get('emergency_contact_secondary_phone_number'),
                'relationship': data.get('emergency_contact_relationship'),
            }
            try:
                emergency_contact = create_emergency_contact(emergency_contact_data, emergency_contact_address)
            except DjangoValidationError as e:
                # If emergency contact validation fails, store the error
                errors['emergency_contact'] = {'messages': [str(error) for error in e.error_list]}

        print({emergency_contact})

        # Extract doctor data
        doctor_data = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'phone_number': data.get('phone_number'),
            'email': data.get('email'),
            'date_of_birth': data.get('date_of_birth'),
            'gender': data.get('gender'),
            'specialty': data.get('specialty'),
            'date_hired': data.get('date_hired'),
            'hiring_end_date': data.get('hiring_end_date') if data.get('hiring_end_date') else None,
            'license_number': data.get('license_number'),
            'address': address.pk if address else None,
            'emergency_contact': emergency_contact.pk if emergency_contact else None,
        }
        print(doctor_data)
        serializer = DoctorSerializer(data=doctor_data)

        if serializer.is_valid():
            print("Validation Passed: Data is valid.")
            doctor = serializer.save()
            print(f"Doctor Created: {doctor}")
        else:
            # If validation fails, print errors
            print("Validation Failed: Errors occurred.")
            print(serializer.errors)
            errors['doctor'] = serializer.errors
        print("The errors are:")
        print(errors)
        return errors


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