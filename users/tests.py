from django.test import TestCase
from django.urls import reverse
from .models import CustomUser

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            password='password123',
            email='test@example.com',
            role='member'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'member')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

class SignUpViewTest(TestCase):
    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_form(self):
        data = {
            'username': 'newuser',
            'password1': 'a-much-more-secure-password-123!',
            'password2': 'a-much-more-secure-password-123!',
            'email': 'newuser@example.com',
            'role': 'member'
        }

        # The UserCreationForm expects fields named 'password' and 'password2'
        # in the POST data, which it then uses for validation.
        response = self.client.post(reverse('signup'), data)

        # Check for redirect on successful submission
        self.assertEqual(response.status_code, 302)

        # Check that the user was created
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())
        user = CustomUser.objects.get(username='newuser')

        # Check that the user is inactive by default
        self.assertFalse(user.is_active)
