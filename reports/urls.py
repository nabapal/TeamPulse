from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('daily/', views.DailyReportView.as_view(), name='daily_report'),
    path('weekly/', views.WeeklyReportView.as_view(), name='weekly_report'),
    path('monthly/', views.MonthlyReportView.as_view(), name='monthly_report'),
    path('export/excel/', views.export_activities_excel, name='export_excel'),
    path('export/csv/', views.export_activities_csv, name='export_csv'),
    path('export/json/', views.export_activities_json, name='export_json'),
    path('export/pdf/', views.export_activities_pdf, name='export_pdf'),
]
