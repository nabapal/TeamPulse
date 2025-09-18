from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import NodeName, ActivityType, Status

class SuperAdminOrManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.role == 'super_admin' or self.request.user.role == 'manager'
        )

class DropdownListView(SuperAdminOrManagerRequiredMixin, ListView):
    model = NodeName
    template_name = 'dropdowns/dropdown_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['node_names'] = NodeName.objects.all()
        context['activity_types'] = ActivityType.objects.all()
        context['statuses'] = Status.objects.all()
        return context

# NodeName Views
class NodeNameCreateView(SuperAdminOrManagerRequiredMixin, CreateView):
    model = NodeName
    fields = ['name']
    template_name = 'dropdowns/dropdown_form.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')

class NodeNameUpdateView(SuperAdminOrManagerRequiredMixin, UpdateView):
    model = NodeName
    fields = ['name']
    template_name = 'dropdowns/dropdown_form.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')

class NodeNameDeleteView(SuperAdminOrManagerRequiredMixin, DeleteView):
    model = NodeName
    template_name = 'dropdowns/dropdown_confirm_delete.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')

# ActivityType Views
class ActivityTypeCreateView(SuperAdminOrManagerRequiredMixin, CreateView):
    model = ActivityType
    fields = ['name']
    template_name = 'dropdowns/dropdown_form.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')

class ActivityTypeUpdateView(SuperAdminOrManagerRequiredMixin, UpdateView):
    model = ActivityType
    fields = ['name']
    template_name = 'dropdowns/dropdown_form.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')

class ActivityTypeDeleteView(SuperAdminOrManagerRequiredMixin, DeleteView):
    model = ActivityType
    template_name = 'dropdowns/dropdown_confirm_delete.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')

# Status Views
class StatusCreateView(SuperAdminOrManagerRequiredMixin, CreateView):
    model = Status
    fields = ['name']
    template_name = 'dropdowns/dropdown_form.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')

class StatusUpdateView(SuperAdminOrManagerRequiredMixin, UpdateView):
    model = Status
    fields = ['name']
    template_name = 'dropdowns/dropdown_form.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')

class StatusDeleteView(SuperAdminOrManagerRequiredMixin, DeleteView):
    model = Status
    template_name = 'dropdowns/dropdown_confirm_delete.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')
