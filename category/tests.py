from django.test import TestCase
from .models import Category


# Unit tests on models.py
class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            category_name='Test Category',
            slug='test-category',
            description='This is a test category description'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.category_name, 'Test Category')
        self.assertEqual(self.category.slug, 'test-category')
        self.assertEqual(self.category.description, 'This is a test category description')

    def test_category_get_url(self):
        url = self.category.get_url()
        expected_url = f'/products/{self.category.slug}/'
        self.assertEqual(url, expected_url)

    def test_category_str_representation(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_category_unique_slug(self):
        new_category = Category.objects.create(
            category_name='New Category',
            slug='test-category',
            description='This is a new category description'
        )
        with self.assertRaises(Exception):
            new_category.save()

    def tearDown(self):
        Category.objects.all().delete()
