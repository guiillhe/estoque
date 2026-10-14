from django.test import TestCase
from django.urls import reverse
from apps.users.models import User


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='password123')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('password123'))

    def test_login_page_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

