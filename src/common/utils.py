from addresses.models import Address
from insurances.models import Insurance
from emergency_contacts.models import EmergencyContact
from django.core.exceptions import ValidationError as DjangoValidationError
from typing import Tuple, Optional, Any, Dict, Union

# Constants for Address and Emergency Contact fields
ADDRESS_REQUIRED_FIELDS = ['country', 'city', 'postal_code']
ADDRESS_FIELDS = ['country', 'city', 'state', 'postal_code', 'street_address']

EMERGENCY_CONTACT_REQUIRED_FIELDS = [
    'emergency_contact_first_name',
    'emergency_contact_last_name',
    'emergency_contact_phone_number',
    'emergency_contact_relationship',
    'emergency_contact_secondary_phone_number',
    'emergency_contact_date_of_birth',
    'emergency_contact_gender',
    'emergency_contact_email'
]
EMERGENCY_CONTACT_FIELDS = [
    'first_name',
    'last_name',
    'email',
    'date_of_birth',
    'gender',
    'phone_number',
    'secondary_phone_number',
    'relationship'
]

# Constants for model field names
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
PHONE_NUMBER = 'phone_number'
EMAIL = 'email'
DATE_OF_BIRTH = 'date_of_birth'
GENDER = 'gender'
ADDRESS = 'address'
EMERGENCY_CONTACT = 'emergency_contact'
SPECIALTY = 'specialty'
DATE_HIRED = 'date_hired'
HIRING_END_DATE = 'hiring_end_date'
LICENSE_NUMBER = 'license_number'
ROLE = 'role'
DEPARTMENT = 'department'
STATUS = 'status'
INSURANCE_PROVIDER = 'insurance_provider'
DOCTORS = 'doctors'
SUPERVISOR_NURSE = 'supervisor_nurse'

# Helper to create an address and handle errors
def create_address_helper(data, prefix="") -> Tuple[Optional[Address], Optional[dict]]:
    """
    Creates an Address instance if sufficient data is provided.

    Parameters:
        data (dict): A dictionary containing address-related fields.
        prefix (str): An optional prefix for field names (default is an empty string).

    Returns:
        Tuple[Optional[Address], Optional[dict]]:
            - Address instance if created successfully, else None.
            - Error dictionary with validation error messages, or None if no errors.
    """
    # Check if all required fields have values
    required_fields = [f'{prefix}{field}' for field in ADDRESS_REQUIRED_FIELDS]
    if all(data.get(field) for field in required_fields):
        # Extract address data from provided fields
        address_data = {field: data.get(f'{prefix}{field}') for field in ADDRESS_FIELDS}

        try:
            # Attempt to create and return the Address instance
            return create_address(address_data), None
        except DjangoValidationError as e:
            # Return errors if validation fails
            return None, {'messages': [str(error) for error in e.error_list]}
    # Return None if not all required fields are provided
    return None, None


# Helper to create an emergency contact and handle errors
def create_emergency_contact_helper(data, address) -> Tuple[Optional[EmergencyContact], Optional[dict]]:
    """
    Creates an EmergencyContact instance if sufficient data is provided.

    Parameters:
        data (dict): A dictionary containing emergency contact-related fields.
        address (Address): The Address instance to link to the emergency contact.

    Returns:
        Tuple[Optional[EmergencyContact], Optional[dict]]:
            - EmergencyContact instance if created successfully, else None.
            - Error dictionary with validation error messages, or None if no errors.
    """
    # Check if all required emergency contact fields have values
    if all(data.get(field, '').strip() for field in EMERGENCY_CONTACT_REQUIRED_FIELDS):
        # Extract emergency contact data from provided fields
        emergency_contact_data = {field: data.get(f'emergency_contact_{field}') for field in EMERGENCY_CONTACT_FIELDS}

        try:
            # Attempt to create and return the EmergencyContact instance
            return create_emergency_contact(emergency_contact_data, address), None
        except DjangoValidationError as e:
            # Return errors if validation fails
            return None, {'messages': [str(error) for error in e.error_list]}
    # Return None if not all required fields are provided
    return None, None

def create_address_and_contact(data, prefix=""):
    """
    Creates an Address and EmergencyContact instance if sufficient data is provided.

    Parameters:
        data (dict): A dictionary containing address and emergency contact-related fields.
        prefix (str): An optional prefix for field names (default is an empty string).

    Returns:
        Tuple[Optional[Address], Optional[EmergencyContact], Optional[dict]]:
            - Address instance if created successfully, else None.
            - EmergencyContact instance if created successfully, else None.
            - Error dictionary with validation error messages, or None if no errors.
    """
    errors = {}

    # Create address for the main person (Doctor/Nurse)
    address, address_errors = create_address_helper(data, prefix=prefix)
    if address_errors:
        errors['address'] = address_errors

    # Create address for emergency contact
    emergency_contact_address, emergency_contact_address_errors = create_address_helper(
        data,
        prefix=f'{prefix}emergency_contact_'
    )
    if emergency_contact_address_errors:
        errors['emergency_contact_address'] = emergency_contact_address_errors

    # Create emergency contact
    emergency_contact, emergency_contact_errors = create_emergency_contact_helper(data, emergency_contact_address)
    if emergency_contact_errors:
        errors['emergency_contact'] = emergency_contact_errors

    return address, emergency_contact, errors



def prepare_model_data(
        data: Dict[str, Any],
        model_type: str,
        address: Optional[Address],
        emergency_contact: Optional[EmergencyContact],
        insurance: Optional[Insurance] = None
) -> Dict[str, Union[str, int, None]]:
    """
    Prepares model data for the given model type.

    Parameters:
        data (dict): A dictionary containing model-related fields.
        model_type (str): The type of model (doctor, nurse, or patient).
        address (Address): The Address instance to link to the model.
        emergency_contact (EmergencyContact): The EmergencyContact instance to link to the model.
        insurance (Insurance): The Insurance instance to link to the patient.

    Returns:
        dict: A dictionary containing the prepared model data.

    """
    model_data = {
        FIRST_NAME: data.get(FIRST_NAME),
        LAST_NAME: data.get(LAST_NAME),
        PHONE_NUMBER: data.get(PHONE_NUMBER),
        EMAIL: data.get(EMAIL),
        DATE_OF_BIRTH: data.get(DATE_OF_BIRTH),
        GENDER: data.get(GENDER),
        ADDRESS: address.pk if address else None,
        EMERGENCY_CONTACT: emergency_contact.pk if emergency_contact else None,
    }

    if model_type == 'doctor':
        model_data.update({
            SPECIALTY: data.get(SPECIALTY),
            DATE_HIRED: data.get(DATE_HIRED),
            HIRING_END_DATE: data.get(HIRING_END_DATE) if data.get(HIRING_END_DATE) else None,
            LICENSE_NUMBER: data.get(LICENSE_NUMBER),
        })
    elif model_type == 'nurse':
        model_data.update({
            LICENSE_NUMBER: data.get(LICENSE_NUMBER),
            ROLE: data.get(ROLE),
            DEPARTMENT: data.get(DEPARTMENT),
            DATE_HIRED: data.get(DATE_HIRED),
            HIRING_END_DATE: data.get(HIRING_END_DATE) if data.get(HIRING_END_DATE) else None,
            SUPERVISOR_NURSE: data.getlist(SUPERVISOR_NURSE),
        })
    elif model_type == 'patient':
        model_data.update({
            STATUS: data.get(STATUS),
            INSURANCE_PROVIDER: insurance.pk,
            DOCTORS: [int(doctor) for doctor in data.getlist(DOCTORS) if doctor.isdigit()],
        })
    return model_data


def create_address(address_data):
    address = Address(**address_data)
    address.clean()
    address.save()
    return address


def create_emergency_contact(emergency_contact_data, address):
    emergency_contact_data['address'] = address
    emergency_contact = EmergencyContact(**emergency_contact_data)
    emergency_contact.clean()
    emergency_contact.save()
    return emergency_contact
