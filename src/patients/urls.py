from django.urls import path
from .views import PatientCreateView, PatientListView, PatientDetailView, PatientUpdateView, \
    PatientDeleteView
from config.url_names import PATIENT_CREATE, PATIENT_LIST, PATIENT_UPDATE, PATIENT_DELETE, PATIENT_DETAIL

urlpatterns = [
    # Other URL patterns for your app
    path('register-patient/', PatientCreateView.as_view(), name=PATIENT_CREATE),
    path('list/', PatientListView.as_view(), name=PATIENT_LIST),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name=PATIENT_DETAIL),
    path('patients/<int:pk>/edit/', PatientUpdateView.as_view(), name=PATIENT_UPDATE),
    path('patients/<int:pk>/delete/', PatientDeleteView.as_view(), name=PATIENT_DELETE),

]
