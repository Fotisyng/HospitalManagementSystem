from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import generics
from .models import Nurse
from addresses.models import Address, Country
from emergency_contacts.models import EmergencyContact
from .serializers import NurseSerializer

class NurseCreateView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        # Fetch countries and any other needed related data
        countries = Country.objects.all().order_by('name')
        nurses = Nurse.objects.filter(role__in=['charge', 'chief'])
        role_choices = Nurse.ROLE_CHOICES
        department_choices = Nurse.DEPARTMENT_CHOICES

        # Render the form template
        context = {
            'countries': countries,
            'role_choices': role_choices,
            'nurses': nurses,
            'department_choices': department_choices,
        }
        return render(request, 'nurse_form.html', context)

    def post(self, request, *args, **kwargs):
        # Extract nurse data and nested related data from request
        nurse_data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'date_of_birth': request.POST.get('date_of_birth'),
            'phone_number': request.POST.get('phone_number'),
            'email': request.POST.get('email'),
            'license_number': request.POST.get('license_number'),
            'role': request.POST.get('role'),
            'department': request.POST.get('department'),
            'date_hired': request.POST.get('date_hired'),
            'status': request.POST.get('status'),
            'supervised_nurse': request.POST.get('supervised_nurse'),
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
            }
        }

        countries = Country.objects.all().order_by('name')
        nurses = Nurse.objects.filter(role__in=['charge', 'chief'])
        role_choices = Nurse.ROLE_CHOICES
        department_choices = Nurse.DEPARTMENT_CHOICES

        try:
            with transaction.atomic():
                # Create address, emergency contact address, and emergency contact
                address = Address.objects.create(**nurse_data['address'])
                emergency_contact_address = Address.objects.create(**nurse_data['emergency_contact_address'])
                emergency_contact_data = nurse_data['emergency_contact']
                emergency_contact_data['address'] = emergency_contact_address  # Link the address
                emergency_contact = EmergencyContact.objects.create(**emergency_contact_data)

                # Prepare the data for the nurse serializer
                nurse_data['address'] = address.pk
                nurse_data['emergency_contact'] = emergency_contact.pk

                # Use the NurseSerializer to create the nurse
                serializer = NurseSerializer(data=nurse_data)

                if serializer.is_valid():
                    nurse = serializer.save()
                    supervised_nurses = nurse_data.get('supervised_nurse')

                    if supervised_nurses:  # Only call set if there are supervised nurses provided
                        nurse.supervised_nurses.set(supervised_nurses)
                    else:
                        nurse.supervised_nurses.clear()  # Optional: Clear the relation if none are provided
                    print(f"Nurse Created: {nurse}")  # Debugging
                    nurse.save()

                    return render(request, 'nurse_form.html', {
                        'success': 'Nurse registered successfully!',
                        'countries': countries,
                        'role_choices': role_choices,
                        'nurses': nurses,
                        'department_choices': department_choices,
                    })
                else:
                    print(serializer.errors)  # Print out errors for debugging
                    raise ValidationError(serializer.errors)

        except ValidationError as e:
            return render(request, 'nurse_form.html', {
                'errors': e.message_dict,
                'countries': countries,
                'role_choices': role_choices,
                'nurses': nurses,
                'department_choices': department_choices,
            })

        except Exception as e:
            import traceback
            print(f"Exception occurred: {str(e)}")
            print(traceback.format_exc())  # This will show the full traceback
            return render(request, 'nurse_form.html', {
                'errors': str(e),
                'countries': countries,
                'role_choices': role_choices,
                'department_choices': department_choices,
            })

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
