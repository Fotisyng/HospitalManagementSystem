from django.http import JsonResponse
from doctors.models import Doctor
from patients.models import Patient

# Search views as functions
def search_doctor_view(request):
    query = request.GET.get("q", "")
    doctors = Doctor.objects.filter(first_name__icontains=query)[:10]
    results = [{"id": doc.id, "name": f"{doc.first_name} {doc.last_name}", "specialty": doc.specialty} for doc in doctors]
    return JsonResponse({"results": results})

def search_patient_view(request):
    query = request.GET.get("q", "")
    patients = Patient.objects.filter(first_name__icontains=query)[:10]
    results = [{"id": pat.id, "name": f"{pat.first_name} {pat.last_name}", "status": pat.status} for pat in patients]
    return JsonResponse({"results": results})
