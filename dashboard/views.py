from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from activities.models import Activity
from dropdowns.models import Status, NodeName, ActivityType
from users.models import CustomUser

class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        user = self.request.user
        if user.role == 'lead':
            return 'dashboard/lead_dashboard.html'
        elif user.role == 'manager':
            return 'dashboard/manager_dashboard.html'
        else:
            return 'dashboard/member_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Role-based filtering
        if user.role == 'manager':
            if user.managed_teams.exists():
                team_members = user.managed_teams.first().members.all()
                activities = Activity.objects.filter(assigned_users__in=team_members)
            else:
                activities = Activity.objects.none()
        elif user.role == 'member':
            activities = Activity.objects.filter(assigned_users=user)
        else: # lead
            activities = Activity.objects.all()

        # Handle search and filtering
        search_query = self.request.GET.get('q')
        status_filter = self.request.GET.get('status')
        activity_type_filter = self.request.GET.get('activity_type')
        node_name_filter = self.request.GET.get('node_name')
        assignee_filter = self.request.GET.get('assignee')
        start_date_filter = self.request.GET.get('start_date')
        end_date_filter = self.request.GET.get('end_date')

        if search_query:
            activities = activities.filter(description__icontains=search_query)
        if status_filter:
            activities = activities.filter(status__id=status_filter)
        if activity_type_filter:
            activities = activities.filter(activity_type__id=activity_type_filter)
        if node_name_filter:
            activities = activities.filter(node_name__id=node_name_filter)
        if assignee_filter:
            activities = activities.filter(assigned_users__id=assignee_filter)
        if start_date_filter:
            activities = activities.filter(start_date__gte=start_date_filter)
        if end_date_filter:
            activities = activities.filter(end_date__lte=end_date_filter)

        context['activities'] = activities
        context['statuses'] = Status.objects.all()
        context['activity_types'] = ActivityType.objects.all()
        context['node_names'] = NodeName.objects.all()
        context['assignees'] = CustomUser.objects.all()

        # Pie chart data
        status_counts = {status.name: 0 for status in context['statuses']}
        for activity in activities:
            status_counts[activity.status.name] += 1

        context['pie_chart_labels'] = list(status_counts.keys())
        context['pie_chart_data'] = list(status_counts.values())

        # Add context for report tabs
        context['report_type'] = 'dashboard'

        return context
