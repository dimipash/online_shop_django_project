from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Account
from .forms import RegistrationForm
from django.test import TestCase
from .models import Account, UserProfile


# Unit Tests views.py

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


# Integration Tests model.py

class AccountModelTestCase(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="john@example.com",
            password="password123"
        )

    def test_create_user(self):
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.username, "johndoe")
        self.assertEqual(self.user.email, "john@example.com")
        self.assertTrue(self.user.check_password("password123"))

    def test_create_superuser(self):
        superuser = Account.objects.create_superuser(
            first_name="Admin",
            last_name="User",
            username="adminuser",
            email="admin@example.com",
            password="admin123"
        )
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_full_name(self):
        self.assertEqual(self.user.full_name(), "John Doe")

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), "john@example.com")

    def test_user_has_perm(self):
        self.assertTrue(self.user.has_perm("test_perm"))

    def test_user_has_module_perms(self):
        self.assertTrue(self.user.has_module_perms("test_module"))


class UserProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            first_name="Jane",
            last_name="Smith",
            username="janesmith",
            email="jane@example.com",
            password="password456"
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            address_line_1="123 Main St",
            city="Cityville",
            state="State",
            country="Country"
        )

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user, self.user)
        self.assertEqual(self.user_profile.address_line_1, "123 Main St")
        self.assertEqual(self.user_profile.city, "Cityville")
        self.assertEqual(self.user_profile.state, "State")
        self.assertEqual(self.user_profile.country, "Country")

    def test_user_profile_full_address(self):
        self.assertEqual(
            self.user_profile.full_address(), "123 Main St "
                                              "Cityville"
        )


class SignalsTestCase(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            first_name="Alice",
            last_name="Johnson",
            username="alicejohnson",
            email="alice@example.com",
            password="password789"
        )

    def test_user_profile_created_signal(self):
        self.assertEqual(UserProfile.objects.filter(user=self.user).count(), 1)

    def test_user_profile_saved_signal(self):
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.user_profile.address_line_1 = "456 Elm St"
        self.user_profile.save()
        self.assertEqual(self.user_profile.full_address(), "456 Elm St ")

    def tearDown(self):
        UserProfile.objects.all().delete()
