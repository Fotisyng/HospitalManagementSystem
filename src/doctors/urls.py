from django.urls import path
from .views import DoctorCreateFormView, DoctorListView, DoctorDetailView, DoctorUpdateView, DoctorDeleteView
from .api_views import CreateDoctorAPIView
from config.url_names import DOCTOR_CREATE, DOCTOR_LIST, DOCTOR_UPDATE, DOCTOR_DELETE, DOCTOR_DETAIL

urlpatterns = [
    path('create/', DoctorCreateFormView.as_view(), name=DOCTOR_CREATE),
    path('list/', DoctorListView.as_view(), name=DOCTOR_LIST),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name=DOCTOR_DETAIL),
    path('doctors/<int:pk>/edit/', DoctorUpdateView.as_view(), name=DOCTOR_UPDATE),
    path('api/create/', CreateDoctorAPIView.as_view(), name='api-doctor-create'),
    path('doctors/<int:pk>/delete/', DoctorDeleteView.as_view(), name=DOCTOR_DELETE),
]
