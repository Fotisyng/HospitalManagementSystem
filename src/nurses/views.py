from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Nurse
from .serializers import NurseSerializer
from hospitalManagementSystem.views import BaseCreateView
from common.utils import create_address_and_contact, prepare_model_data


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
        address, emergency_contact, errors = create_address_and_contact(data)

        nurse_data = prepare_model_data(data, 'nurse', address, emergency_contact)
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
            print(serializer.errors)
            errors['nurse'] = serializer.errors
        print("The errors are:")
        print(errors)
        return errors


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
