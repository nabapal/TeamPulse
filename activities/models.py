from django.conf import settings
from django.db import models
from dropdowns.models import NodeName, ActivityType, Status

class Activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    description = models.TextField()
    node_name = models.ForeignKey(NodeName, on_delete=models.PROTECT)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.IntegerField(editable=False)
    assigned_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='activities'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_activities'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.duration = (self.end_date - self.start_date).days
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.activity_id}: {self.description}"
