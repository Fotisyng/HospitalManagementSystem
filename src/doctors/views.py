from .models import Doctor
from .serializers import DoctorSerializer
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from hospitalManagementSystem.views import BaseCreateView
from common.utils import create_address_and_contact, prepare_model_data
from config.url_names import DOCTOR_LIST, DOCTOR_DETAIL
from config.constants import APP_LOGER
from django.shortcuts import redirect, render
import logging

logger = logging.getLogger(APP_LOGER)

class DoctorCreateFormView(BaseCreateView):
    """
    Form view for creating a new doctor.
    """

    template_name = 'doctor_form.html'
    success_message = 'Doctor registered successfully!'

    def get_context_data(self):
        """
        Extends the base context with additional doctor-specific context data.
        """
        context = super().get_context_data()
        specialty_choices = Doctor.SPECIALTY_CHOICES
        gender_choices = Doctor.GENDER_CHOICES

        context.update({
            'gender_choices': gender_choices,
            'specialty_choices': specialty_choices,
        })

        return context

    def create_related_models(self, data: dict) -> dict:
        """
        Handles doctor-specific related model creation. The doctor address and
        emergency_contact are also created along with the doctor object.

        Args:
            data (dict): The data from the request to process to create the doctor

        Returns:
            dict: The errors from the procedure. In case no errors are thrown, an empty dict is returned
        """
        address, emergency_contact, errors = create_address_and_contact(data)

        # Extract doctor data
        doctor_data = prepare_model_data(data, 'doctor', address, emergency_contact)
        serializer = DoctorSerializer(data=doctor_data)

        if serializer.is_valid():
            doctor = serializer.save()
            logger.info(f"Doctor created successfully: {doctor}")
        else:
            logger.error(f"Doctor validation failed due to: {serializer.errors}")
            errors['doctor'] = serializer.errors
        logger.error(f"Doctor creation failed due to the following errors: {errors}")
        return errors


class DoctorListView(ListView):
    """
    List view for all doctors.
    """

    model = Doctor
    template_name = 'doctor_list.html'  # The template that will render the list
    context_object_name = 'doctors'  # The name to access the list in the template


class DoctorDetailView(DetailView):
    """
    Detail view for a doctor.
    """

    model = Doctor
    template_name = 'doctor_detail.html'
    context_object_name = 'doctor'


class DoctorUpdateView(UpdateView):
    """
    Update the details of a doctor view.
    """

    model = Doctor
    fields = '__all__'
    template_name = 'doctor_update_form.html'
    success_url = reverse_lazy(DOCTOR_LIST)

    def form_valid(self, form):
        """
        Perform the update operation on the specified doctor and update
        the 'patients' field if included in POST data.

        Note: The 'patients' field is not updated directly in this view,
        but rather in the form_valid method. This is done to avoid clearing
        the 'patients' field during the update operation.

        Args:
            form (forms.ModelForm): The form instance containing the updated data.
        """
        doctor = form.save(commit=False)
        doctor.save()

        # Handle 'patients' field separately if it's included in POST data
        if 'patients' in self.request.POST:
            patients = form.cleaned_data.get('patients')
            doctor.patients.set(patients)

        return redirect(DOCTOR_LIST)

    def form_invalid(self, form):
        """
        Handle the invalid form submission.

        Args:
            form (forms.ModelForm): The form instance containing the invalid data.
        """
        logger.error(f"The update of the doctor failed: {form.errors}")
        return super().form_invalid(form)


class DoctorDeleteView(DeleteView):
    """
    A class for deleting a doctor operation.
    """

    model = Doctor
    template_name = 'doctor_confirm_delete.html'
    success_url = reverse_lazy(DOCTOR_LIST)


class AssignPatientsView(View):
    """
    A class for the assigning patients to a doctor operation.
    """

    def get(self, request):
        """
        Display the form to assign patients to a doctor.

        Args:
            request (django.http.HttpRequest): The HTTP request object.

        Returns:
            django.http.HttpResponse: The rendered HTML template with the form.
        """
        return render(request, 'assign_patients.html')