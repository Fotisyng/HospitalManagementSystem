import logging

from django.views.generic import ListView, UpdateView, DeleteView, DetailView, View
from django.urls import reverse_lazy
from .models import Nurse
from .serializers import NurseSerializer
from hospitalManagementSystem.views import BaseCreateView
from common.utils import create_address_and_contact, prepare_model_data
from django.shortcuts import redirect, render
from config.url_names import NURSE_LIST
from config.constants import APP_LOGER, DEPARTMENT_CHOICES

logger = logging.getLogger(APP_LOGER)

class NurseCreateView(BaseCreateView):
    """
    The view for the creation of a Nurse.
    """

    template_name = 'nurse_form.html'
    success_message = 'Nurse registered successfully!'

    def get_context_data(self):
        """
        Extends the base context with additional nurse-specific context data.
        """
        context = super().get_context_data()
        role_choices = Nurse.ROLE_CHOICES
        gender_choices = Nurse.GENDER_CHOICES
        head_nurses = Nurse.objects.filter(role__in=['charge', 'chief'])

        context.update({
            'role_choices': role_choices,
            'gender_choices': gender_choices,
            'department_choices': DEPARTMENT_CHOICES,
            'nurses': head_nurses,
        })

        return context

    def create_related_models(self, data: dict)-> dict:
        """
        Handles nurse-specific related model creation. The nurse address and
        emergency_contact are also created along with the nurse object.
        """
        address, emergency_contact, errors = create_address_and_contact(data)

        nurse_data = prepare_model_data(data, 'nurse', address, emergency_contact)
        serializer = NurseSerializer(data=nurse_data)

        if serializer.is_valid():
            nurse = serializer.save()
            # Set supervised nurses if provided
            supervisor_nurse = nurse_data.get('supervisor_nurse')
            if supervisor_nurse:
                nurse.supervisor_nurses.set(supervisor_nurse)
            else:
                nurse.supervisor_nurses.clear()
            logger.info(f"Nurse created successfully: {nurse}")
        else:
            # If validation fails, print errors
            logger.error(f"Nurse validation failed due to: {serializer.errors}")
            errors['nurse'] = serializer.errors
        logger.error(f"Nurse creation failed due to the following errors: {errors}")
        return errors


class NurseListView(ListView):
    """
    The class view to show a list of all nurses.
    """

    model = Nurse
    template_name = 'nurse_list.html'
    context_object_name = 'nurses'


class NurseDetailView(DetailView):
    """
    The class view to show a nurse's detail information.
    """

    model = Nurse
    template_name = 'nurse_detail.html'
    context_object_name = 'nurse'


class NurseUpdateView(UpdateView):
    """
    The view to update a nurse's information.
    If the supervisor_nurses field is included in POST data, it will be updated
    along with the rest of the form data.
    """

    model = Nurse
    fields = '__all__'
    template_name = 'nurse_update_form.html'
    success_url = reverse_lazy(NURSE_LIST)

    def form_valid(self, form):
        """
        Perform the update operation on the specified nurse and update
        the 'supervisor_nurses' field if included in POST data. This is in order
        not to overwrite existing fields.

        Args:
            form (forms.ModelForm): The form instance containing the updated data.
        """
        nurse = form.save(commit=False)
        nurse.save()

        # Handle 'supervisor_nurses' field separately if included in POST data
        if 'supervisor_nurses' in self.request.POST:
            supervisor_nurses = form.cleaned_data.get('supervisor_nurses')
            nurse.supervisor_nurses.set(supervisor_nurses)

        return redirect(self.success_url)

    def form_invalid(self, form):
        """
        Handle the invalid form submission.

        Args:
            form: The invalid form instance.
        """
        logger.error(f"The update of the nurse failed: {form.errors}")
        return super().form_invalid(form)


class NurseDeleteView(DeleteView):
    """
    A class that handles the deletion of a Nurse view.
    """

    model = Nurse
    template_name = 'nurse_confirm_delete.html'  # Create this template for delete confirmation
    success_url = reverse_lazy(NURSE_LIST)  # Redirect to list after successful deletion


class AssignNursesView(View):
    """
    A class that handles the view to assign nurses to a supervising nurse.
    """

    def get(self, request):
        """
        Display the form to assign nurses to a supervising nurse.

        Args:
            request (django.http.HttpRequest): The HTTP request object.

        Returns:
            django.http.HttpResponse: The rendered HTML template with the form.
        """
        return render(request, 'nurse_assign.html')