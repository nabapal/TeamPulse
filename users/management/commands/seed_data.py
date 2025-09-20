import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import CustomUser
from teams.models import Team
from activities.models import Activity
from dropdowns.models import NodeName, ActivityType, Status

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Clean up existing data
        Activity.objects.all().delete()
        Team.objects.all().delete()
        CustomUser.objects.all().delete()
        NodeName.objects.all().delete()
        ActivityType.objects.all().delete()
        Status.objects.all().delete()

        # Create Lead
        lead = CustomUser.objects.create_user(
            username='lead',
            password='password',
            email='lead@example.com',
            role='lead',
            is_staff=True,
            is_superuser=True
        )
        self.stdout.write(self.style.SUCCESS('Successfully created lead user'))

        # Create Managers
        managers = []
        for i in range(1, 5):
            manager = CustomUser.objects.create_user(
                username=f'manager{i}',
                password='password',
                email=f'manager{i}@example.com',
                role='manager',
                is_staff=True
            )
            managers.append(manager)
        self.stdout.write(self.style.SUCCESS('Successfully created manager users'))

        # Create Teams
        team_names = ['Telco', 'IPSE', 'IP-MPLS-Access', 'IP-MPLS-Core', 'FTTX', 'Enterprise', 'Optical', 'Microwave-Clocking']
        teams = []
        for i, team_name in enumerate(team_names):
            team = Team.objects.create(name=team_name, manager=managers[i % len(managers)])
            teams.append(team)
        self.stdout.write(self.style.SUCCESS('Successfully created teams'))

        # Create Team Members
        for team in teams:
            for i in range(1, 6):
                member = CustomUser.objects.create_user(
                    username=f'{team.name.lower()}_member{i}',
                    password='password',
                    email=f'{team.name.lower()}_member{i}@example.com',
                    role='member'
                )
                team.members.add(member)
        self.stdout.write(self.style.SUCCESS('Successfully created team members'))

        # Create Dropdown Values
        node_names = [NodeName.objects.create(name=f'Node {i}') for i in range(1, 6)]
        activity_types = [ActivityType.objects.create(name=f'Type {i}') for i in range(1, 4)]
        statuses = [
            Status.objects.create(name='In Progress'),
            Status.objects.create(name='Completed'),
            Status.objects.create(name='Yet to Start'),
            Status.objects.create(name='On Hold')
        ]
        self.stdout.write(self.style.SUCCESS('Successfully created dropdown values'))

        # Create Activities
        for team in teams:
            members = team.members.all()
            for member in members:
                for i in range(10):
                    activity = Activity.objects.create(
                        description=f'Activity {i} for {member.username}',
                        node_name=random.choice(node_names),
                        activity_type=random.choice(activity_types),
                        status=random.choice(statuses),
                        start_date=timezone.now().date(),
                        end_date=timezone.now().date() + timezone.timedelta(days=random.randint(1, 10)),
                        created_by=member
                    )
                    # Assign users
                    if i < 6: # 6 solo activities
                        activity.assigned_users.add(member)
                    else: # 4 multi-assigned activities
                        activity.assigned_users.add(member)
                        other_member = members.exclude(pk=member.pk).order_by('?').first()
                        if other_member:
                            activity.assigned_users.add(other_member)
        self.stdout.write(self.style.SUCCESS('Successfully created activities'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
