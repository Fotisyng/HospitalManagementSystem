from django.urls import path
from .views import DoctorCreateFormView, DoctorListView, DoctorDetailView, DoctorUpdateView, DoctorDeleteView
from .api_views import CreateDoctorAPIView

urlpatterns = [
    path('create/', DoctorCreateFormView.as_view(), name='create-doctor'),
    path('list/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('doctors/<int:pk>/edit/', DoctorUpdateView.as_view(), name='doctor-update'),
    path('api/create/', CreateDoctorAPIView.as_view(), name='api-doctor-create'),
    path('doctors/<int:pk>/delete/', DoctorDeleteView.as_view(), name='doctor-delete'),
]
