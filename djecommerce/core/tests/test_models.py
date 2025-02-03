from django.test import TestCase
from django.contrib.auth.models import User
from core.models import UserProfile


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='password123')
        self.user_profile = UserProfile.objects.create(user=self.user)
    
    def test_user_profile_creation(self):
        user = User.objects.create(username='testuser2', password='password1234')
        user_profile = UserProfile.objects.create(user=user)
        self.assertTrue(isinstance(user_profile, UserProfile))
        self.assertEqual(user_profile.__str__(), user.username)

    def test_str_method(self):
        self.assertEqual(str(self.user_profile), self.user.username)

    def test_default_one_click_purchasing(self):
        self.assertFalse(self.user_profile.one_click_purchasing)

    def test_stripe_customer_id(self):
        self.user_profile.stripe_customer_id = 'cus_12345'
        self.user_profile.save()
        self.assertEqual(self.user_profile.stripe_customer_id, 'cus_12345')
        
    