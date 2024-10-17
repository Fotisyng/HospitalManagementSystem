from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Nurse
from .serializers import NurseSerializer
from hospitalManagementSystem.views import BaseCreateView
from common.utils import create_address, create_emergency_contact


class NurseCreateView(BaseCreateView):

    template_name = 'nurse_form.html'
    success_message = 'Nurse registered successfully!'

    def get_context_data(self):
        """Extends the base context with additional nurse-specific context data."""
        context = super().get_context_data()
        role_choices = Nurse.ROLE_CHOICES
        gender_choices = Nurse.GENDER_CHOICES
        department_choices = Nurse.DEPARTMENT_CHOICES
        head_nurses = Nurse.objects.filter(role__in=['charge', 'chief'])

        context.update({
            'role_choices': role_choices,
            'gender_choices': gender_choices,
            'department_choices': department_choices,
            'nurses': head_nurses,
        })

        return context


    def create_related_models(self, data):
        """Handles nurse-specific related model creation. The nurse address and
        emergency_contact are also created along with the nurse object."""
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

        print({address})

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

        print({emergency_contact_address})

        if any(data.get(field) for field in
               ['emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_mobile_phone',
                'emergency_contact_relationship']):
            emergency_contact_data = {
                'name': data.get('emergency_contact_name'),
                'phone_number': data.get('emergency_contact_phone'),
                'mobile_phone_number': data.get('emergency_contact_mobile_phone'),
                'relationship': data.get('emergency_contact_relationship'),
            }
            emergency_contact = create_emergency_contact(emergency_contact_data, emergency_contact_address)
        else:
            emergency_contact = None

        print({emergency_contact})

        nurse_data = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'date_of_birth': data.get('date_of_birth'),
            'phone_number': data.get('phone_number'),
            'email': data.get('email'),
            'gender': data.get('gender'),
            'license_number': data.get('license_number'),
            'role': data.get('role'),
            'department': data.get('department'),
            'date_hired': data.get('date_hired'),
            'hiring_end_date': data.get('hiring_end_date') if data.get('hiring_end_date') else None,
            'supervisor_nurse': data.getlist('supervisor_nurse'),
            'address': address.pk if address else None,
            'emergency_contact': emergency_contact.pk if emergency_contact else None,
        }
        print(nurse_data)
        serializer = NurseSerializer(data=nurse_data)

        if serializer.is_valid():
            print("Validation Passed: Data is valid.")
            nurse = serializer.save()
            # Set supervised nurses if provided
            supervisor_nurse = nurse_data.get('supervisor_nurse')
            if supervisor_nurse:
                nurse.supervisor_nurses.set(supervisor_nurse)
            else:
                nurse.supervisor_nurses.clear()

            print(f"Nurse Created: {nurse}")
        else:
            # If validation fails, print errors
            print("Validation Failed: Errors occurred.")
            print(serializer.errors)  # Debugging
            return serializer.errors


class NurseListView(ListView):
    model = Nurse
    template_name = 'nurse_list.html'  # Create this template
    context_object_name = 'nurses'  # The name to access the list in the template

class NurseDetailView(DetailView):
    model = Nurse
    template_name = 'nurse_detail.html'
    context_object_name = 'nurse'  # The name to access the list in the template

class NurseUpdateView(UpdateView):
    model = Nurse
    fields = '__all__'  # All fields will be editable
    template_name = 'nurse_update_form.html'  # The template to render the form
    success_url = reverse_lazy('nurse-list')  # Redirect to the list after successful update

class NurseDeleteView(DeleteView):
    model = Nurse
    template_name = 'nurse_confirm_delete.html'  # Create this template for delete confirmation
    success_url = reverse_lazy('nurse-list')  # Redirect to list after successful deletion
