from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from carts.models import CartItem
from orders.forms import OrderForm
from orders.models import Order
from .views import place_order, order_complete


# Unit tests on views
class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.cart_item = CartItem.objects.create(user=self.user)
        self.order_form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '1234567890',
            'email': 'john@example.com',
            'address_line_1': '123 Main St',
            'address_line_2': 'Apt 456',
            'country': 'USA',
            'state': 'CA',
            'city': 'Cityville',
            'order_note': 'Test order note'
        }

    def test_place_order_with_empty_cart(self):
        request = self.factory.post('/place-order/')
        request.user = self.user
        response = place_order(request)
        self.assertEqual(response.status_code, 302)  # Redirect response

    def test_place_order_with_valid_form(self):
        request = self.factory.post('/place-order/', data=self.order_form_data)
        request.user = self.user
        response = place_order(request)
        self.assertEqual(response.status_code, 200)  # Successful response

        # Check if the order was created
        order_count = Order.objects.count()
        self.assertEqual(order_count, 1)

        # Check if the cart was cleared
        cart_item_count = CartItem.objects.filter(user=self.user).count()
        self.assertEqual(cart_item_count, 0)

    def test_place_order_with_invalid_form(self):
        invalid_form_data = self.order_form_data.copy()
        invalid_form_data['email'] = 'invalid_email'
        request = self.factory.post('/place-order/', data=invalid_form_data)
        request.user = self.user
        response = place_order(request)
        self.assertEqual(response.status_code, 302)  # Redirect response

    def test_order_complete_view(self):
        request = self.factory.get('/order-complete/')
        response = order_complete(request)
        self.assertEqual(response.status_code, 200)  # Successful response

    def tearDown(self):
        CartItem.objects.all().delete()
        Order.objects.all().delete()
