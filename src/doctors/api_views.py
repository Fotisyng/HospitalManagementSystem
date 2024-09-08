from rest_framework import generics
from .models import Doctor
from .serializers import DoctorSerializer


class CreateDoctorAPIView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
