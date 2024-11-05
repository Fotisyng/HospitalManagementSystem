from addresses.models import Address
from patients.models import EmergencyContact

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
