from django.urls import path
from .views import DoctorCreateFormView
from .api_views import CreateDoctorAPIView

urlpatterns = [
    path('create/', DoctorCreateFormView.as_view(), name='doctor-create'),
    path('api/create/', CreateDoctorAPIView.as_view(), name='api-doctor-create'),
]
