from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportView.as_view(), name='report'),
    path('export/excel/', views.export_activities_excel, name='export_excel'),
]
