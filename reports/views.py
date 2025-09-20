from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from activities.models import Activity
from users.models import CustomUser
from dropdowns.models import Status, NodeName, ActivityType
from django.utils import timezone
from django.db.models import Count, Q
from openpyxl import Workbook
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test

class ManagerOrLeadRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['manager', 'lead']

def is_manager_or_lead(user):
    return user.is_authenticated and user.role in ['manager', 'lead']

class ReportView(LoginRequiredMixin, View):
    template_name = 'reports/report.html'
    report_type = None # 'daily', 'weekly', 'monthly'

    def get_queryset(self):
        user = self.request.user
        activities = Activity.objects.all()

        if user.role == 'manager':
            if user.managed_teams.exists():
                team_members = user.managed_teams.first().members.all()
                activities = activities.filter(assigned_users__in=team_members)
            else:
                activities = Activity.objects.none()
        elif user.role == 'member':
            activities = activities.filter(assigned_users=user)

        # Filter by report type
        today = timezone.now().date()
        if self.report_type == 'daily':
            activities = activities.filter(start_date=today)
        elif self.report_type == 'weekly':
            start_of_week = today - timezone.timedelta(days=today.weekday())
            end_of_week = start_of_week + timezone.timedelta(days=6)
            activities = activities.filter(start_date__range=[start_of_week, end_of_week])
        elif self.report_type == 'monthly':
            activities = activities.filter(start_date__month=today.month, start_date__year=today.year)

        return activities

    def get_context_data(self, **kwargs):
        activities = self.get_queryset()
        context = {
            'activities': activities,
            'report_type': self.report_type,
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

class DailyReportView(ReportView):
    report_type = 'daily'

class WeeklyReportView(ReportView):
    report_type = 'weekly'

class MonthlyReportView(ReportView):
    report_type = 'monthly'

import csv
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

@login_required
@user_passes_test(is_manager_or_lead)
def export_activities_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="activities_report.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Activities Report"

    activities = Activity.objects.all()
    if request.user.role == 'manager':
        if request.user.managed_teams.exists():
            team_members = request.user.managed_teams.first().members.all()
            activities = activities.filter(assigned_users__in=team_members)
        else:
            activities = Activity.objects.none()

    # Headers
    headers = ["Activity ID", "Description", "Node Name", "Activity Type", "Status", "Start Date", "End Date", "Assigned Users"]
    ws.append(headers)

    for activity in activities:
        assigned_users = ", ".join([user.username for user in activity.assigned_users.all()])
        row = [
            activity.pk,
            activity.description,
            activity.node_name.name,
            activity.activity_type.name,
            activity.status.name,
            activity.start_date,
            activity.end_date,
            assigned_users
        ]
        ws.append(row)

    wb.save(response)
    return response

@login_required
@user_passes_test(is_manager_or_lead)
def export_activities_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="activities_report.csv"'

    writer = csv.writer(response)

    activities = Activity.objects.all()
    if request.user.role == 'manager':
        if request.user.managed_teams.exists():
            team_members = request.user.managed_teams.first().members.all()
            activities = activities.filter(assigned_users__in=team_members)
        else:
            activities = Activity.objects.none()

    # Headers
    writer.writerow(["Activity ID", "Description", "Node Name", "Activity Type", "Status", "Start Date", "End Date", "Assigned Users"])

    for activity in activities:
        assigned_users = ", ".join([user.username for user in activity.assigned_users.all()])
        writer.writerow([
            activity.pk,
            activity.description,
            activity.node_name.name,
            activity.activity_type.name,
            activity.status.name,
            activity.start_date,
            activity.end_date,
            assigned_users
        ])

    return response

@login_required
@user_passes_test(is_manager_or_lead)
def export_activities_json(request):
    activities = Activity.objects.all()
    if request.user.role == 'manager':
        if request.user.managed_teams.exists():
            team_members = request.user.managed_teams.first().members.all()
            activities = activities.filter(assigned_users__in=team_members)
        else:
            activities = Activity.objects.none()

    data = []
    for activity in activities:
        assigned_users = [user.username for user in activity.assigned_users.all()]
        data.append({
            'activity_id': activity.pk,
            'description': activity.description,
            'node_name': activity.node_name.name,
            'activity_type': activity.activity_type.name,
            'status': activity.status.name,
            'start_date': str(activity.start_date),
            'end_date': str(activity.end_date),
            'assigned_users': assigned_users,
        })

    response = HttpResponse(json.dumps(data, indent=4), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="activities_report.json"'
    return response

@login_required
@user_passes_test(is_manager_or_lead)
def export_activities_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="activities_report.pdf"'

    activities = Activity.objects.all()
    if request.user.role == 'manager':
        if request.user.managed_teams.exists():
            team_members = request.user.managed_teams.first().members.all()
            activities = activities.filter(assigned_users__in=team_members)
        else:
            activities = Activity.objects.none()

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    data = [["Activity ID", "Description", "Status", "Assigned To"]]
    for activity in activities:
        assigned_users = ", ".join([user.username for user in activity.assigned_users.all()])
        data.append([
            activity.pk,
            activity.description,
            activity.status.name,
            assigned_users,
        ])

    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    elements.append(table)
    doc.build(elements)

    return response
