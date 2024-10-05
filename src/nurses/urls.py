from django.urls import path
from .views import NurseListView, NurseUpdateView, NurseCreateView, NurseDetailView, NurseDeleteView

urlpatterns = [
    path('list/', NurseListView.as_view(), name='nurse-list'),
    path('add/', NurseCreateView.as_view(), name='create_nurse'),
    path('nurses/<int:pk>/', NurseDetailView.as_view(), name='nurse-detail'),
    path('edit/<int:pk>/', NurseUpdateView.as_view(), name='nurse-update'),
    path('nurses/<int:pk>/delete', NurseDeleteView.as_view(), name='nurse-delete'),
]
