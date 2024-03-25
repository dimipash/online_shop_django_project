from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import Product, Variation, Cart, CartItem
from .views import add_cart, remove_cart, remove_cart_item, cart, checkout


class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(name='Test Product', price=10.0)
        self.variation = Variation.objects.create(product=self.product, variation_category='Size',
                                                  variation_value='Small')

    def test_add_cart_authenticated_user(self):
        request = self.factory.post('/add-cart/1/')
        request.user = self.user
        response = add_cart(request, product_id=1)
        self.assertEqual(response.status_code, 302)  # Redirect response

    def test_remove_cart_authenticated_user(self):
        cart_item = CartItem.objects.create(product=self.product, user=self.user)
        request = self.factory.post('/remove-cart/1/1/')
        request.user = self.user
        response = remove_cart(request, product_id=1, cart_item_id=1)
        self.assertEqual(response.status_code, 302)  # Redirect response

    def test_remove_cart_item_authenticated_user(self):
        cart_item = CartItem.objects.create(product=self.product, user=self.user)
        request = self.factory.post('/remove-cart-item/1/1/')
        request.user = self.user
        response = remove_cart_item(request, product_id=1, cart_item_id=1)
        self.assertEqual(response.status_code, 302)  # Redirect response

    def test_cart_view_authenticated_user(self):
        cart_item = CartItem.objects.create(product=self.product, user=self.user, quantity=2)
        request = self.factory.get('/cart/')
        request.user = self.user
        response = cart(request)
        self.assertEqual(response.status_code, 200)  # Successful response
        self.assertContains(response, 'Test Product')
        self.assertContains(response, 'Total: 20.0')
        self.assertContains(response, 'Quantity: 2')

    def test_checkout_view_authenticated_user(self):
        cart_item = CartItem.objects.create(product=self.product, user=self.user, quantity=2)
        request = self.factory.get('/checkout/')
        request.user = self.user
        response = checkout(request)
        self.assertEqual(response.status_code, 200)  # Successful response
        self.assertContains(response, 'Test Product')
        self.assertContains(response, 'Total: 20.0')
        self.assertContains(response, 'Quantity: 2')

    def tearDown(self):
        CartItem.objects.all().delete()
        Product.objects.all().delete()
        Variation.objects.all().delete()
        User.objects.all().delete()
        Cart.objects.all().delete()
