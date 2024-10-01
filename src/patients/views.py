from django.db import transaction
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from rest_framework import generics
from doctors.models import Doctor
from patients.models import Patient
from addresses.models import Address, Country
from emergency_contacts.models import EmergencyContact
from insurances.models import Insurance
from .serializers import PatientSerializer  # Assuming you have a serializer
from django.views.generic import ListView, DetailView, UpdateView, DeleteView


class PatientCreateView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        # Fetch countries and doctors from the database
        countries = Country.objects.all().order_by('name')
        doctors = Doctor.objects.all().order_by('last_name')
        gender_choices = Patient.GENDER_CHOICES
        status_choices = Patient.STATUS_CHOICES

        # Render a form template
        context = {
            'countries': countries,  # Pass countries to the template
            'doctors': doctors, # Pass doctors to the template
            'gender_choices': gender_choices,
            'status_choices': status_choices,
        }
        return render(request, 'patient_form.html', context)

    def post(self, request, *args, **kwargs):
        # Extract patient data and nested related data from request
        patient_data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'date_of_birth': request.POST.get('date_of_birth'),
            'gender': request.POST.get('gender'),
            'phone_number': request.POST.get('phone_number'),
            'email': request.POST.get('email'),
            'status': request.POST.get('status'),
            'address': {
                'country': request.POST.get('country'),
                'city': request.POST.get('city'),
                'state': request.POST.get('state'),
                'postal_code': request.POST.get('postal_code'),
                'street_address': request.POST.get('street_address'),
            },
            'emergency_contact_address': {
                'country': request.POST.get('emergency_contact_country'),
                'city': request.POST.get('emergency_contact_city'),
                'state': request.POST.get('emergency_contact_state'),
                'postal_code': request.POST.get('emergency_contact_postal_code'),
                'street_address': request.POST.get('emergency_contact_street_address'),
            },
            'emergency_contact': {
                'name': request.POST.get('emergency_contact_name'),
                'phone_number': request.POST.get('emergency_contact_phone'),
                'mobile_phone_number': request.POST.get('emergency_contact_mobile_phone'),
                'relationship': request.POST.get('emergency_contact_relationship'),
                'address': request.POST.get('emergency_contact_address'),
            },
            'insurance_provider': {
                'provider': request.POST.get('insurance_provider'),
                'policy_number': request.POST.get('insurance_policy_number'),
                'start_date': request.POST.get('coverage_start_date'),
                'end_date': request.POST.get('coverage_end_date'),
            },
            'doctors': request.POST.getlist('doctor')
        }

        countries = Country.objects.all().order_by('name')
        doctors = Doctor.objects.all().order_by('last_name')

        try:
            with transaction.atomic():

                # Create address, emergency contact address, emergency contact, and insurance
                address = Address.objects.create(**patient_data['address'])
                emergency_contact_address = Address.objects.create(**patient_data['emergency_contact_address'])
                insurance = Insurance.objects.create(**patient_data['insurance_provider'])
                emergency_contact_data = patient_data['emergency_contact']
                emergency_contact_data['address'] = emergency_contact_address  # Link the address
                emergency_contact = EmergencyContact.objects.create(**emergency_contact_data)

                # Prepare the data for the patient serializer
                patient_data['address'] = address.pk
                patient_data['emergency_contact'] = emergency_contact.pk
                patient_data['insurance_provider'] = insurance.pk

                # Use the PatientSerializer to create the patient
                serializer = PatientSerializer(data=patient_data)

                if serializer.is_valid():
                    patient = serializer.save()
                    patient.doctors.set(patient_data['doctors'])
                    print(f"Patient Created: {patient}")  # Debugging
                    patient.save()

                    return render(request, 'patient_form.html', {
                        'success': 'Patient registered successfully!',
                        'countries': countries,
                        'doctors': doctors,
                    })
                else:
                    print(serializer.errors)  # Print out errors for debugging
                    raise ValidationError(serializer.errors)

        except ValidationError as e:
            return render(request, 'patient_form.html', {
                'errors': e.message_dict,
                'countries': countries,
                'doctors': doctors,
            })

        except Exception as e:
            import traceback
            print(f"Exception occurred: {str(e)}")
            print(traceback.format_exc())  # This will show the full traceback
            return render(request, 'patient_form.html', {
                'errors': str(e),
                'countries': countries,
                'doctors': doctors,
            })

class PatientListView(ListView):
    model = Patient
    template_name = 'patient_list.html'  # The template to render the list
    context_object_name = 'patients'  # The name to access the list in the template

    def get_queryset(self):
        status = self.request.GET.get('status', 'active')  # Default to 'active' if no status is selected
        return Patient.objects.filter(status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status_choices = Patient.STATUS_CHOICES  # Fetch status choices from the model
        context['status_choices'] = status_choices  # Pass status choices to the template
        context['selected_status'] = self.request.GET.get('status', 'active')  # Pass selected status to the template
        return context

class PatientDetailView(DetailView):
    model = Patient
    template_name = 'patient_detail.html'
    context_object_name = 'patient' # The name to access the list in the template

class PatientUpdateView(UpdateView):
    model = Patient
    fields = '__all__'  # All fields will be editable
    template_name = 'patient_update_form.html'  # The template to render the form
    success_url = reverse_lazy('patient-list')  # Redirect to the list after successful update

class PatientDeleteView(DeleteView):
    model = Patient
    template_name = 'patient_confirm_delete.html'  # Create this template for delete confirmation
    success_url = reverse_lazy('patient-list')  # Redirect to list after successful deletion