from django.urls import path
from .views import NurseListView, NurseUpdateView, NurseCreateView, NurseDetailView, NurseDeleteView
from config.url_names import NURSE_CREATE, NURSE_DELETE, NURSE_UPDATE, NURSE_DETAIL, NURSE_LIST

urlpatterns = [
    path('list/', NurseListView.as_view(), name=NURSE_LIST),
    path('add/', NurseCreateView.as_view(), name=NURSE_CREATE),
    path('nurses/<int:pk>/', NurseDetailView.as_view(), name=NURSE_DETAIL),
    path('edit/<int:pk>/', NurseUpdateView.as_view(), name=NURSE_UPDATE),
    path('nurses/<int:pk>/delete', NurseDeleteView.as_view(), name=NURSE_DELETE),
]
