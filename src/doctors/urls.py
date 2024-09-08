from django.urls import path
from .views import DoctorCreateFormView, DoctorListView
from .api_views import CreateDoctorAPIView

urlpatterns = [
    path('create/', DoctorCreateFormView.as_view(), name='create-doctor'),
    path('list/', DoctorListView.as_view(), name='doctor-list'),
    path('api/create/', CreateDoctorAPIView.as_view(), name='api-doctor-create'),
]
