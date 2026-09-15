from decimal import Decimal

from django.test import TestCase

from products.models import Category, Product


class ProductCategoryManyToManyTest(TestCase):
    def test_product_can_have_multiple_categories(self):
        category_a = Category.objects.create(name='Electronics')
        category_b = Category.objects.create(name='Mobiles')

        product = Product.objects.create(
            name='Phone',
            description='Demo product',
            price=Decimal('1000.00'),
            old_price=Decimal('1100.00'),
            discount=0,
        )
        product.categories.add(category_a, category_b)

        self.assertEqual(product.categories.count(), 2)
        self.assertTrue(product.categories.filter(name='Electronics').exists())
        self.assertTrue(product.categories.filter(name='Mobiles').exists())
