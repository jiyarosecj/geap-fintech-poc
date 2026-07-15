from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.run_governance_gates, name='dashboard'),
    path('download-report/', views.generate_report, name='download-report'),
]