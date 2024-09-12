from django.db import models
import requests
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Address(models.Model):
    class Meta:
        db_table = 'addresses'

    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.country}"

    def validate_country(self):
        """
        Validates if the provided country is valid using the REST Countries API.

        Parameters:
        self (Address): The instance of the Address model where this method is being called.

        Returns:
        None: This method does not return any value. It raises a ValidationError if the country is not valid.

        Raises:
        ValidationError: If the country is not valid or if there is an error while making the API request.
        """
        api_url = f"https://restcountries.com/v3.1/name/{self.country}"
        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                raise ValidationError(_("Invalid country name."), code='invalid_country')
        except requests.RequestException:
            raise ValidationError(_("Unable to validate the country at this time."), code='api_error')


    def validate_postal_code_with_google_maps(self):
        """
        Validate the postal code using Google Maps Address Validation API.
        """
        # Query the Country model to get the ISO Alpha-2 code for the country name
        try:
            country_obj = Country.objects.get(name=self.country)
            region_code = country_obj.iso_alpha_2  # Use the ISO Alpha-2 code
        except Country.DoesNotExist:
            raise ValidationError(f"Country '{self.country}' not found in the database.")

        api_key = settings.GOOGLE_MAPS_API_KEY # Replace with your actual API key
        api_url = f"https://addressvalidation.googleapis.com/v1:validateAddress?key={api_key}"

        # Prepare the request body
        request_body = {
            "address": {
                "regionCode": region_code,  # CLDR country code (e.g., "US" for the United States)
                "postalCode": self.postal_code,
                "locality": self.city,
                "addressLines": [self.street_address]  # Include the street address in addressLines
            },
            "enableUspsCass": False  # USPS CASS validation only applies for US addresses
        }

        try:
            print(f"Sending API request to Google Maps: {request_body}")

            # Make the API call
            response = requests.post(api_url, json=request_body)

            # Log the response
            print(f"Response status code: {response.status_code}")
            print(f"Response body: {response.json()}")

            # Check if the status code is not 200
            if response.status_code != 200:
                response_data = response.json()

                # Check for specific error message about unsupported region code
                if response_data.get("error", {}).get("message", "").startswith("Unsupported region code"):
                    # Skip validation and continue the process
                    print(f"Skipping validation for unsupported region code: {region_code}")
                    return

                # For other API errors, raise a ValidationError
                raise ValidationError("Postal code validation failed due to an API error.")

            # Check for validation status in the response
            response_data = response.json()
            if response_data.get("validationResult") and response_data["validationResult"]["result"] != "VALID":
                raise ValidationError("Invalid postal code for the specified country.")

        except requests.RequestException:
            # Handle API connection errors gracefully
            raise ValidationError("Error connecting to Google Maps API for postal code validation.")


    def clean(self):
        """
        Override the clean method to validate the country, city, and postal code together.
        """
        self.validate_country()
        self.validate_postal_code_with_google_maps()


class Country(models.Model):
    name = models.CharField(max_length=100)
    iso_alpha_2 = models.CharField(max_length=2, unique=True)  # Two-letter country code
    iso_alpha_3 = models.CharField(max_length=3, unique=True)  # Three-letter country code

    class Meta:
        db_table = 'countries'

    def __str__(self):
        return self.name
