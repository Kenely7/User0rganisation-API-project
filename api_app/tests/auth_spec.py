from django.test import TestCase
from rest_framework.test import APIClient
from api_app.models import Organisation, User

class RegisterEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_register_successfully(self):
        response = self.client.post('/auth/register/', {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'phone': '34514'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('accessToken', response.data['data'])
        user = User.objects.get(email='john.doe@example.com')
        organisation = Organisation.objects.get(name="John's Organisation")
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(organisation.name, "John's Organisation")

    def test_user_login_successfully(self):
        User.objects.create_user(email='testuser', password='password')
        response = self.client.post('/auth/login/', {'email': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('accessToken', response.data['data'])

    def test_user_missing_required_fields(self):
        response = self.client.post('/auth/register/', {})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Registration unsuccessful', response.data['message'])

    def test_user_duplicate_email(self):
        User.objects.create_user(email='test@example.com', password='password')
        response = self.client.post('/auth/register/', {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'password': 'password123',
            'phone': '454'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Registration unsuccessful', response.data['message'])
