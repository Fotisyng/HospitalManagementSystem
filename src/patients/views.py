from django.urls import reverse_lazy
from doctors.models import Doctor
from patients.models import Patient
from insurances.models import Insurance
from .serializers import PatientSerializer
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from hospitalManagementSystem.views import BaseCreateView
from common.utils import create_address, create_emergency_contact
from django.core.exceptions import ValidationError as DjangoValidationError


class PatientCreateView(BaseCreateView):
    template_name = 'patient_form.html'
    success_message = 'Patient registered successfully!'

    def get_context_data(self):
        """Extends the base context with additional patient-specific data."""
        # Call the base method to get the shared context (e.g., countries)
        context = super().get_context_data()

        # Add nurse-specific context data
        doctors = Doctor.objects.all().order_by('last_name')
        gender_choices = Patient.GENDER_CHOICES
        status_choices = Patient.STATUS_CHOICES

        # Update the context with nurse-specific choices and data
        context.update({
            'doctors': doctors,  # Pass doctors to the template
            'gender_choices': gender_choices,
            'status_choices': status_choices,
        })

        return context

    def create_related_models(self, data):
        """Handles patient-related model creation."""
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
            if all(data.get(field) for field in
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
        if any(data.get(field) for field in
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

        insurance_provider = {
            'provider': data.get('insurance_provider'),
            'policy_number': data.get('insurance_policy_number'),
            'start_date': data.get('coverage_start_date'),
            'end_date': data.get('coverage_end_date'),
        }

        insurance = Insurance.objects.create(**insurance_provider)

        # Now create the patient using the patient data
        patient_data = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'date_of_birth': data.get('date_of_birth'),
            'gender': data.get('gender'),
            'phone_number': data.get('phone_number'),
            'email': data.get('email'),
            'status': data.get('status'),
            'address': address.pk,
            'emergency_contact': emergency_contact.pk,
            'insurance_provider': insurance.pk,
            'doctors': data.getlist('doctor')
        }

        serializer = PatientSerializer(data=patient_data)

        if serializer.is_valid():
            print("Validation Passed: Data is valid.")
            patient = serializer.save()
            # Set supervised nurses if provided
            assigned_doctor = patient_data.get('doctors')
            if assigned_doctor:
                patient.doctors.set(assigned_doctor)
            else:
                patient.doctors.clear()

            print(f"Patient Created: {patient}")
        else:
            # If validation fails, print errors
            print("Validation Failed: Errors occurred.")
            print(serializer.errors)
            errors['nurse'] = serializer.errors
        print("The errors are:")
        print(errors)
        return errors


class PatientListView(ListView):
    model = Patient
    template_name = 'patient_list.html'  # The template to render the list
    context_object_name = 'patients'  # The name to access the list in the template

    def get_queryset(self):
        status = self.request.GET.get('status', 'active')  # Default to 'active' if no status is selected
        return Patient.objects.filter(status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status_choices = Patient.STATUS_CHOICES
        context['status_choices'] = status_choices
        context['selected_status'] = self.request.GET.get('status', 'active')
        return context


class PatientDetailView(DetailView):
    model = Patient
    template_name = 'patient_detail.html'
    context_object_name = 'patient'  # The name to access the list in the template


class PatientUpdateView(UpdateView):
    model = Patient
    fields = '__all__'  # All fields will be editable
    template_name = 'patient_update_form.html'  # The template to render the form
    success_url = reverse_lazy('patient-list')  # Redirect to the list after successful update


class PatientDeleteView(DeleteView):
    model = Patient
    template_name = 'patient_confirm_delete.html'  # Create this template for delete confirmation
    success_url = reverse_lazy('patient-list')  # Redirect to list after successful deletion
