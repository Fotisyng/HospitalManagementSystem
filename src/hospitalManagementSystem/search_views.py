from django.http import JsonResponse
from doctors.models import Doctor
from patients.models import Patient
from nurses.models import Nurse

# Search views as functions
def search_doctor_view(request)-> JsonResponse:
    """
    Search for doctors by their first name

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the search results.
    """
    query = request.GET.get("q", "")
    doctors = Doctor.objects.filter(first_name__icontains=query)[:10]
    results = [{"id": doc.id, "name": f"{doc.first_name} {doc.last_name}", "specialty": doc.specialty} for doc in doctors]
    return JsonResponse({"results": results})

def search_patient_view(request)-> JsonResponse:
    """
    Search for patients by their first name

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the search results.
    """
    query = request.GET.get("q", "")
    patients = Patient.objects.filter(first_name__icontains=query)[:10]
    results = [{"id": pat.id, "name": f"{pat.first_name} {pat.last_name}", "status": pat.status} for pat in patients]
    return JsonResponse({"results": results})


def search_supervisor_nurse_view(request)-> JsonResponse:
    """
    Search for nurses by their first name who are supervisors (either Chief or Charge)

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the search results.
    """
    query = request.GET.get("q", "")
    supervisor_nurses = Nurse.objects.filter(
        first_name__icontains=query,
        role__in=['chief', 'charge']
    )[:10]
    results = [
        {"id": nurse.id, "name": f"{nurse.first_name} {nurse.last_name}", "role": nurse.role}
        for nurse in supervisor_nurses]
    return JsonResponse({"results": results})

def search_nurse_view(request)-> JsonResponse:
    """
    Search for nurses by their first name who are staff or charge (may have supervisor nurse).

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the search results.
    """
    query = request.GET.get("q", "")
    staff_nurses = Nurse.objects.filter(
        first_name__icontains=query,
        role__in=['staff', 'charge']
    )[:10]
    results = [
        {"id": nurse.id, "name": f"{nurse.first_name} {nurse.last_name}", "role": nurse.role}
        for nurse in staff_nurses
    ]
    return JsonResponse({"results": results})
