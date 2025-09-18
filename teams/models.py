from django.conf import settings
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_teams'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='teams'
    )

    def __str__(self):
        return self.name
