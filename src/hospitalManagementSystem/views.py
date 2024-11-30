import logging

from django.views import View
from django.shortcuts import render
from django.db import transaction
from addresses.models import Country
from config.constants import APP_LOGER

logger = logging.getLogger(APP_LOGER)

def render_form(request, template_name, context):
    """
    Renders a form with the given template name and context.

    Parameters:
    request (HttpRequest): The HTTP request object.
    template_name (str): The name of the template to render.
    context (dict): The context data to pass to the template.

    Returns:
    HttpResponse: The rendered template with the given context data.
    """
    return render(request, template_name, context)


def format_errors(errors: dict)-> list:
    """
    Flattens and formats error messages for easier rendering.

    Parameters:
    errors (dict): A dictionary containing model keys as keys and field errors as values.
    Each field error is a dictionary with field names as keys and error messages as values.
    Error messages can be either a string or a list of strings.

    Returns:
    list: A list of formatted error messages. Each error message is a string.
    """
    formatted_errors = []
    for model_key, field_errors in errors.items():
        for field, error_list in field_errors.items():
            for error in error_list:
                if isinstance(error, list) or isinstance(error, str):
                    clean_error = error.strip("[]'\"")
                    formatted_errors.append(clean_error)
                else:
                    formatted_errors.append(str(error))
    return formatted_errors


class BaseCreateView(View):
    template_name = None  # To be defined by the subclass
    success_message = None  # To be defined by the subclass

    def get_context_data(self):
        """
        Returns shared context data like countries.
        """
        countries = Country.objects.all().order_by('name')
        context = {
            'countries': countries,
            'errors': [],
        }
        return context

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to render the form.

        Parameters:
        request (HttpRequest): The incoming request object.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

        Returns:
        HttpResponse: The rendered form as an HttpResponse object.
        """
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def create_related_models(self, data: dict) -> dict:
        """
        This method is intended to be overridden by subclasses to define specific
        model creation logic. It takes a dictionary of form data as input and is
        expected to return a dictionary of validation errors.

        Parameters:
        data (dict): A dictionary containing form data. The keys represent field names,
        and the values represent the corresponding field values.

        Returns:
        dict: A dictionary of validation errors. The keys represent model names, and
        the values are dictionaries containing field names as keys and error
        messages as values. If no errors occur, an empty dictionary is returned.

        Raises:
        NotImplementedError: If this method is not overridden by a subclass.
        """
        raise NotImplementedError("Subclasses must implement create_related_models")

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to process the form submission.

        Parameters:
        request (HttpRequest): The incoming request object.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

        Returns:
        HttpResponse: The rendered form as an HttpResponse object in case of errors or success.
        In case of errors, the rendered form includes error messages.
        In case of success, the rendered form includes a success message.

        Raises:
        Exception: If an unhandled exception occurs during the processing of the form submission.

        The function performs the following steps:
        1. Retrieves form data from the incoming POST request.
        2. Calls the handle_transaction method to create related models within a transaction.
        3. Prepares the context data by calling the get_context_data method.
        4. If errors occur during the creation of related models, formats the errors, adds them to the context,
           and renders the form with error messages.
        5. If no errors occur, renders the form with a success message.
        6. If an unhandled exception occurs, handles the exception by rendering the form with an error message.
        """
        data = request.POST
        try:
            errors = self.handle_transaction(data)

            # Prepare the context
            context = self.get_context_data()

            if errors:
                formatted_errors = format_errors(errors)
                context['errors'] = formatted_errors
                return self.render_with_errors(request, context)

            # Success scenario
            context['errors'] = []
            return self.render_with_success(request, context)

        except Exception as e:
            return self.handle_exception(request, e)

    def handle_transaction(self, data: dict)-> dict:
        """
        Handles the creation of related models within a transaction. It returns
        the validation errors that may occur within the transaction and in this case
        it is rolled back.

        Parameters:
            data (dict): A dictionary containing form data. The keys represent field names,
            and the values represent the corresponding field values.

        Returns:
            dict: A dictionary of validation errors. The keys represent model names, and
            the values are dictionaries containing field names as keys and error
            messages as values. If no errors occur, an empty dictionary is returned.
        """
        with transaction.atomic():
            errors = self.create_related_models(data)
            if errors:
                transaction.set_rollback(True)
            return errors

    def render_with_errors(self, request, context: dict):
        """
        Renders the template with error messages.

        Parameters:
            request (HttpRequest): The incoming request object.
            context (dict): The context data to pass to the template.

        """
        return render(request, self.template_name, context)

    def render_with_success(self, request, context: dict):
        """
        Renders the template with a success message.
        """
        context['success'] = self.success_message
        return render(request, self.template_name, context)

    def handle_exception(self, request, exception):
        """
        Handles exceptions and renders the error message.
        """
        import traceback
        logger.error(f"Exception occurred: {str(exception)}\n{traceback.format_exc()}")
        context = self.get_context_data()
        context['errors'] = [str(exception)]
        return render(request, self.template_name, context)
