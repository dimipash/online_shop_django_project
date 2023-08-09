from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Account
from .forms import RegistrationForm


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertIsInstance(response.context['form'], RegistrationForm)

    def test_register_post_valid_data(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '1234567890',
            'email': 'john@example.com',
            'password': 'testpassword123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        user = get_user_model().objects.get(email=data['email'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.phone_number, data['phone_number'])
        self.assertEqual(user.username, 'john')
        self.assertTrue(user.check_password(data['password']))

    def test_register_post_invalid_data(self):
        data = {
            'first_name': '',
            'last_name': 'Doe',
            'phone_number': '1234567890',
            'email': 'invalid_email',
            'password': 'testpassword123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertFormError(response, 'form', 'first_name', 'This field is required.')
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_register_with_existing_email(self):
        existing_user = Account.objects.create_user(
            first_name='Jane',
            last_name='Doe',
            username='jane_doe',
            email='jane@example.com',
            password='testpassword456',
        )
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '1234567890',
            'email': 'jane@example.com',  # Use existing email
            'password': 'testpassword123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'A user with that email address already exists.')
