from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import NodeName, ActivityType, Status

class LeadOrManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.role == 'lead' or self.request.user.role == 'manager'
        )

class DropdownListView(LeadOrManagerRequiredMixin, ListView):
    model = NodeName
    template_name = 'dropdowns/dropdown_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['node_names'] = NodeName.objects.all()
        context['activity_types'] = ActivityType.objects.all()
        context['statuses'] = Status.objects.all()
        return context

# NodeName Views
class NodeNameCreateView(LeadOrManagerRequiredMixin, CreateView):
    model = NodeName
    fields = ['name']
    template_name = 'dropdowns/dropdown_form.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')

class NodeNameUpdateView(LeadOrManagerRequiredMixin, UpdateView):
    model = NodeName
    fields = ['name']
    template_name = 'dropdowns/dropdown_form.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')

class NodeNameDeleteView(LeadOrManagerRequiredMixin, DeleteView):
    model = NodeName
    template_name = 'dropdowns/dropdown_confirm_delete.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')

# ActivityType Views
class ActivityTypeCreateView(LeadOrManagerRequiredMixin, CreateView):
    model = ActivityType
    fields = ['name']
    template_name = 'dropdowns/dropdown_form.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')

class ActivityTypeUpdateView(LeadOrManagerRequiredMixin, UpdateView):
    model = ActivityType
    fields = ['name']
    template_name = 'dropdowns/dropdown_form.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')

class ActivityTypeDeleteView(LeadOrManagerRequiredMixin, DeleteView):
    model = ActivityType
    template_name = 'dropdowns/dropdown_confirm_delete.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')

# Status Views
class StatusCreateView(LeadOrManagerRequiredMixin, CreateView):
    model = Status
    fields = ['name']
    template_name = 'dropdowns/dropdown_form.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')

class StatusUpdateView(LeadOrManagerRequiredMixin, UpdateView):
    model = Status
    fields = ['name']
    template_name = 'dropdowns/dropdown_form.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')

class StatusDeleteView(LeadOrManagerRequiredMixin, DeleteView):
    model = Status
    template_name = 'dropdowns/dropdown_confirm_delete.html'
    success_url = reverse_lazy('dropdowns:dropdown_list')
