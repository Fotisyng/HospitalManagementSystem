from django.urls import path
from .views import PatientCreateView, PatientListView, PatientDetailView, PatientUpdateView, \
    PatientDeleteView  # Import your PatientCreateView

urlpatterns = [
    # Other URL patterns for your app
    path('register-patient/', PatientCreateView.as_view(), name='create_patient'),  # Register the patient create view
    path('list/', PatientListView.as_view(), name='patient-list'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('patients/<int:pk>/edit/', PatientUpdateView.as_view(), name='patient-update'),
    path('doctors/<int:pk>/delete/', PatientDeleteView.as_view(), name='patient-delete'),

]
