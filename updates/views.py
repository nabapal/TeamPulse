from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Update
from activities.models import Activity

class UpdateCreateView(LoginRequiredMixin, CreateView):
    model = Update
    fields = ['update_text', 'date']
    template_name = 'updates/update_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.activity = Activity.objects.get(pk=self.kwargs['activity_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('activities:activity_detail', kwargs={'pk': self.kwargs['activity_pk']})
