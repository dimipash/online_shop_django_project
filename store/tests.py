from django.test import TestCase
from .models import Product, Category
from .views import store, product_detail, search


class TestViews(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='Category', slug='category')
        self.product = Product.objects.create(
            category=self.category,
            name='Product', slug='product', price=100, is_available=True
        )

        self.client.get('/')  # create session

    def test_store_view(self):
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/store.html')

    def test_product_detail_view(self):
        response = self.client.get('/category/product/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_detail.html')

    def test_search_view(self):
        response = self.client.get('/search/', {'keyword': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/store.html')

    def test_store_pagination(self):
        # Create pagination
        products = Product.objects.bulk_create([Product() for i in range(9)])
        response = self.client.get('/store/')
        self.assertEqual(len(response.context['products']), 3)  # 3 products per page

    def test_product_detail_in_cart(self):
        # Add product to cart
        self.cart.add(self.product)
        response = self.client.get('/category/product/')
        self.assertTrue(response.context['in_cart'])
