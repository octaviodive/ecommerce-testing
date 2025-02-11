from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.forms import SignUpForm

class LoginTestCase(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_login_page_status_code(self):
        # Check if the login page loads correctly
        response = self.client.get(reverse('core:login'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        # Test the login functionality
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('core:login'), login_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:home'))

    def test_login_failed(self):
        # Test failed login
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('core:login'), login_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There was an error, please try again...")
        

class UserRegistrationTest(TestCase):
    
    def setUp(self):
        self.register_url = reverse('core:register')
    
    def test_registration_page_status_code(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_registration_form(self):
        response = self.client.get(self.register_url)
        self.assertIsInstance(response.context['form'], SignUpForm)

    def test_register_user_success(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_user_invalid_password(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'differentpassword'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)  # Form should re-render with errors
        self.assertFalse(User.objects.filter(username='testuser').exists())

