from django.urls import path
from .views import (
    DoctorCreateFormView,
    DoctorListView,
    DoctorDetailView,
    DoctorUpdateView,
    DoctorDeleteView,
    AssignPatientsView
)
from .api_views import CreateDoctorAPIView, AssignPatientsAPIView
from config.url_names import DOCTOR_CREATE, DOCTOR_LIST, DOCTOR_UPDATE, DOCTOR_DELETE, DOCTOR_DETAIL, ASSIGN_PATIENT

urlpatterns = [
    path('create/', DoctorCreateFormView.as_view(), name=DOCTOR_CREATE),
    path('list/', DoctorListView.as_view(), name=DOCTOR_LIST),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name=DOCTOR_DETAIL),
    path('doctors/<int:pk>/edit/', DoctorUpdateView.as_view(), name=DOCTOR_UPDATE),
    path('api/create/', CreateDoctorAPIView.as_view(), name='api-doctor-create'),
    path('doctors/<int:pk>/delete/', DoctorDeleteView.as_view(), name=DOCTOR_DELETE),
    path('assign-patients/', AssignPatientsView.as_view(), name=ASSIGN_PATIENT),
    path('api/assign-patients/', AssignPatientsAPIView.as_view(), name='assign_patients_api'),  # For DRF API view

]
