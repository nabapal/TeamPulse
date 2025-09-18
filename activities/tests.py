from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from dropdowns.models import NodeName, ActivityType, Status
from .models import Activity
from datetime import date

class ActivityViewPermissionsTest(TestCase):
    def setUp(self):
        self.super_admin = CustomUser.objects.create_superuser('superadmin', 'super@admin.com', 'password')
        self.manager = CustomUser.objects.create_user('manager', 'manager@test.com', 'password', role='manager')
        self.member = CustomUser.objects.create_user('member', 'member@test.com', 'password', role='member')

        self.node_name = NodeName.objects.create(name='Test Node')
        self.activity_type = ActivityType.objects.create(name='Test Type')
        self.status_completed = Status.objects.create(name='Completed')
        self.status_inprogress = Status.objects.create(name='In Progress')

        self.activity_completed = Activity.objects.create(
            description='Completed test activity',
            node_name=self.node_name,
            activity_type=self.activity_type,
            status=self.status_completed,
            start_date=date.today(),
            end_date=date.today(),
            created_by=self.manager
        )
        self.activity_inprogress = Activity.objects.create(
            description='In-progress test activity',
            node_name=self.node_name,
            activity_type=self.activity_type,
            status=self.status_inprogress,
            start_date=date.today(),
            end_date=date.today(),
            created_by=self.manager
        )

    def test_member_cannot_delete_activity(self):
        self.client.login(username='member', password='password')
        response = self.client.get(reverse('activities:activity_delete', args=[self.activity_inprogress.pk]))
        self.assertEqual(response.status_code, 403) # Forbidden

    def test_manager_can_delete_activity(self):
        self.client.login(username='manager', password='password')
        response = self.client.get(reverse('activities:activity_delete', args=[self.activity_inprogress.pk]))
        self.assertEqual(response.status_code, 200)

    def test_member_can_edit_completed_activity(self):
        self.client.login(username='member', password='password')
        response = self.client.get(reverse('activities:activity_edit', args=[self.activity_completed.pk]))
        self.assertEqual(response.status_code, 200)

    def test_member_cannot_edit_inprogress_activity(self):
        self.client.login(username='member', password='password')
        response = self.client.get(reverse('activities:activity_edit', args=[self.activity_inprogress.pk]))
        self.assertEqual(response.status_code, 403)

    def test_manager_can_edit_any_activity(self):
        self.client.login(username='manager', password='password')
        response_completed = self.client.get(reverse('activities:activity_edit', args=[self.activity_completed.pk]))
        response_inprogress = self.client.get(reverse('activities:activity_edit', args=[self.activity_inprogress.pk]))
        self.assertEqual(response_completed.status_code, 200)
        self.assertEqual(response_inprogress.status_code, 200)
