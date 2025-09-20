from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Activity

class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = 'activities/activity_list.html'
    context_object_name = 'activities'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'lead':
            return Activity.objects.all()
        elif user.role == 'manager':
            return Activity.objects.filter(assigned_users__in=user.managed_teams.first().members.all())
        else:
            return Activity.objects.filter(assigned_users=user)

class ActivityDetailView(LoginRequiredMixin, DetailView):
    model = Activity
    template_name = 'activities/activity_detail.html'

class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    fields = ['description', 'node_name', 'activity_type', 'status', 'start_date', 'end_date', 'assigned_users']
    template_name = 'activities/activity_form.html'
    success_url = reverse_lazy('activities:activity_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ActivityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Activity
    fields = ['description', 'node_name', 'activity_type', 'status', 'start_date', 'end_date', 'assigned_users']
    template_name = 'activities/activity_form.html'
    success_url = reverse_lazy('activities:activity_list')

    def test_func(self):
        user = self.request.user
        activity = self.get_object()
        if user.role in ['lead', 'manager']:
            return True
        return activity.assigned_users.filter(pk=user.pk).exists()

class ActivityDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Activity
    template_name = 'activities/activity_confirm_delete.html'
    success_url = reverse_lazy('activities:activity_list')

    def test_func(self):
        user = self.request.user
        return user.role in ['lead', 'manager']
