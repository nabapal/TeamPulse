from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from activities.models import Activity
from users.models import CustomUser
from dropdowns.models import Status, NodeName, ActivityType
from django.db.models import Count, Q
from openpyxl import Workbook
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test

class ManagerOrSuperAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['manager', 'super_admin']

def is_manager_or_super_admin(user):
    return user.is_authenticated and user.role in ['manager', 'super_admin']

class ReportView(LoginRequiredMixin, ManagerOrSuperAdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        activities = Activity.objects.all()
        if request.user.role == 'manager':
            if request.user.managed_teams.exists():
                team_members = request.user.managed_teams.first().members.all()
                activities = activities.filter(assigned_users__in=team_members)
            else:
                activities = Activity.objects.none()

        grouped_activities = activities.values('node_name__name', 'activity_type__name').annotate(count=Count('pk')).order_by('node_name__name', 'activity_type__name')

        if request.user.role == 'manager' and request.user.managed_teams.exists():
            members = request.user.managed_teams.first().members.all()
        else:
            members = CustomUser.objects.all()

        activity_counts = members.annotate(total_activities=Count('activities', filter=Q(activities__in=activities))).values('username', 'total_activities')

        try:
            inprogress_status = Status.objects.get(name='In Progress')
            inprogress_counts = members.annotate(inprogress_activities=Count('activities', filter=Q(activities__status=inprogress_status, activities__in=activities))).values('username', 'inprogress_activities')
        except Status.DoesNotExist:
            inprogress_counts = members.annotate(inprogress_activities=Count('activities', filter=Q(pk__in=[]))).values('username', 'inprogress_activities')


        status_distribution = activities.values('status__name').annotate(count=Count('pk')).order_by('status__name')

        context = {
            'grouped_activities': grouped_activities,
            'activity_counts': activity_counts,
            'inprogress_counts': inprogress_counts,
            'status_distribution': status_distribution,
        }
        return render(request, 'reports/report.html', context)

@login_required
@user_passes_test(is_manager_or_super_admin)
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
            activity.activity_id,
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
