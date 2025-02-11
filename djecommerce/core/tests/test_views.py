from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

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
