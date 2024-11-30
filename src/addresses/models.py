import logging
import requests

from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from config.constants import APP_LOGER

logger = logging.getLogger(APP_LOGER)

class Address(models.Model):
    """
    Represents an address with country, city, postal code, street address, and state attributes.
    """

    class Meta:
        db_table = 'addresses'

    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.country}"


    def validate_address_with_google_maps(self):
        """
        Validate the country, city, postal code and street address for the countries supported
        using Google Maps Address Validation API.
        """
        # Query the Country model to get the ISO Alpha-2 code for the country name
        try:
            country_obj = Country.objects.get(name=self.country)
            region_code = country_obj.iso_alpha_2  # Use the ISO Alpha-2 code
        except Country.DoesNotExist:
            logger.error(f"Country '{self.country}' not found in the database.")
            raise ValidationError(f"Country '{self.country}' not found in the database.")

        api_key = settings.GOOGLE_MAPS_API_KEY
        api_url = f"https://addressvalidation.googleapis.com/v1:validateAddress?key={api_key}"

        # Prepare the request body
        request_body = {
            "address": {
                "regionCode": region_code,  # CLDR country code (e.g., "US" for the United States)
                "postalCode": self.postal_code,
                "locality": self.city,
                "addressLines": [self.street_address] if self.street_address else []
                # Include the street address in addressLines
            },
            "enableUspsCass": False  # USPS CASS validation only applies for US addresses
        }

        try:
            logger.debug(f"Sending API request to Google Maps: {request_body}")

            # Make the API call
            response = requests.post(api_url, json=request_body)

            # Log the response
            logger.debug(f"Google Maps Response - Status Code: {response.status_code}, Body: {response.json()}")

            # Check if the status code is not 200
            if response.status_code != 200:
                response_data = response.json()

                # Check for specific error message about unsupported region code
                if response_data.get("error", {}).get("message", "").startswith("Unsupported region code"):
                    logger.info(f"Skipping validation for unsupported region code: {region_code}")
                    return

                # For other API errors, raise a ValidationError
                raise ValidationError("Address could not be validated.")

            response_data = response.json()

            # Check for unconfirmed postal code in the response
            address = response_data.get('result', {}).get('address', {})
            address_components = address.get('addressComponents', [])

            # Iterate through the address components to check for unconfirmed postal code
            for component in address_components:
                if component['componentType'] == 'postal_code':
                    confirmation_level = component.get('confirmationLevel')

                    # Raise an error if the postal code is unconfirmed but plausible
                    if confirmation_level != 'CONFIRMED':
                        raise ValidationError(
                            f"Postal code '{self.postal_code}' could not be confirmed for the address provided."
                        )

        except requests.RequestException:
            # Handle API connection errors gracefully
            raise ValidationError("Error connecting to Google Maps API for postal code validation.")


    def clean(self):
        """
        Override the clean method to validate the country, city, and postal code together.
        """
        if settings.ADDRESS_VALIDATION_ENABLED:
            self.validate_address_with_google_maps()


class Country(models.Model):
    """
    Model representing countries supported by the application.
    """

    name = models.CharField(max_length=100)
    iso_alpha_2 = models.CharField(max_length=2, unique=True)  # Two-letter country code
    iso_alpha_3 = models.CharField(max_length=3, unique=True)  # Three-letter country code

    class Meta:
        db_table = 'countries'

    def __str__(self):
        return self.name
