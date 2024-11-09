from config.url_names import (
    PATIENT_CREATE,
    PATIENT_LIST,
    PATIENT_DETAIL,
    PATIENT_UPDATE,
    PATIENT_DELETE,
    DOCTOR_CREATE,
    DOCTOR_LIST,
    DOCTOR_DETAIL,
    DOCTOR_UPDATE,
    DOCTOR_DELETE,
    ASSIGN_PATIENT,
    NURSE_CREATE,
    NURSE_LIST,
    NURSE_DETAIL,
    NURSE_UPDATE,
    NURSE_DELETE,
    SEARCH_PATIENT,
    SEARCH_DOCTOR,
)

def url_names(request):
    """
    Returns a dictionary of URL names used in the application and is used a context_processor for accessing
    the constants in templates.

    Args:
        request: Django request object.

    Returns:
        dict: A dictionary containing URL names.
    """
    return {
        'PATIENT_CREATE': PATIENT_CREATE,
        'PATIENT_LIST': PATIENT_LIST,
        'PATIENT_DETAIL': PATIENT_DETAIL,
        'PATIENT_UPDATE': PATIENT_UPDATE,
        'PATIENT_DELETE': PATIENT_DELETE,
        'DOCTOR_CREATE': DOCTOR_CREATE,
        'DOCTOR_LIST': DOCTOR_LIST,
        'DOCTOR_DETAIL': DOCTOR_DETAIL,
        'DOCTOR_UPDATE': DOCTOR_UPDATE,
        'DOCTOR_DELETE': DOCTOR_DELETE,
        'ASSIGN_PATIENT': ASSIGN_PATIENT,
        'NURSE_CREATE': NURSE_CREATE,
        'NURSE_LIST': NURSE_LIST,
        'NURSE_DETAIL': NURSE_DETAIL,
        'NURSE_UPDATE': NURSE_UPDATE,
        'NURSE_DELETE': NURSE_DELETE,
        'SEARCH_PATIENT': SEARCH_PATIENT,
        'SEARCH_DOCTOR': SEARCH_DOCTOR,
    }
