from rest_framework import generics
from .models import Doctor
from .serializers import DoctorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from patients.models import Patient

class CreateDoctorAPIView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class AssignPatientsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        doctor_id = request.data.get('doctor_id')
        patient_ids = request.data.get('patient_ids')

        try:
            doctor = Doctor.objects.get(id=doctor_id)
            patients = Patient.objects.filter(id__in=patient_ids)

            # Assign patients to the doctor
            doctor.patients.add(*patients)

            return Response({'message': 'Patient assigned successfully!'}, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)