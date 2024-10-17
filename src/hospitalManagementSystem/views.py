from django.core.exceptions import ValidationError
from django.views import View
from django.shortcuts import render
from django.db import transaction
from addresses.models import Country

class BaseCreateView(View):
    template_name = None  # To be defined by the subclass
    success_message = None  # To be defined by the subclass

    def get_context_data(self):
        """Returns shared context data like countries."""
        countries = Country.objects.all().order_by('name')
        context = {
            'countries': countries,
            # Add more common context data here if needed
        }
        return context

    def get(self, request, *args, **kwargs):
        """Handles GET requests to render the form."""
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def create_related_models(self, data):
        """Create related models like address and emergency contact."""
        # This will be overridden by subclasses to define specific model creation logic
        raise NotImplementedError("Subclasses must implement create_related_models")

    def post(self, request, *args, **kwargs):
        """Handles POST requests to process the form submission."""
        data = request.POST
        try:
            with transaction.atomic():
                # Delegate the creation of related models to the subclass method
                errors = self.create_related_models(data)
                print("The errors that occurred: %s" % errors)

                if errors:
                    # If errors are returned, render the form with error messages
                    context = self.get_context_data()
                    context['errors'] = errors
                    return render(request, self.template_name, context)

                # If no errors, pass success message and context to the template
                context = self.get_context_data()
                context['success'] = self.success_message
                return render(request, self.template_name, context)
        except Exception as e:
            # Handle errors
            import traceback
            print(f"Exception occurred: {str(e)}")
            print(traceback.format_exc())  # This will show the full traceback
            context = self.get_context_data()
            context['errors'] = str(e)
            return render(request, self.template_name, context)

    def render_form(self, request, template_name, context):
        return render(request, template_name, context)
