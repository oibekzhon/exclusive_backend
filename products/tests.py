from datetime import timedelta
from decimal import Decimal
import json
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from products.admin import ProductAdmin
from products.forms import ProductForm
from products.models import Category, Product, Size


class SizeJSONLoaderTest(TestCase):
    def test_load_sizes_command_reads_json_and_creates_size_records(self):
        fixture = Path('products/fixtures/sizes.json')
        created = []

        with fixture.open(encoding='utf-8') as fp:
            payload = json.load(fp)
            created = payload['sizes']

        call_command('load_sizes', json_path=str(fixture))

        self.assertEqual(Size.objects.filter(name__in=created).count(), len(created))


class ProductTimeWindowTest(TestCase):
    def test_product_allows_optional_time_window_fields_for_flash_sale_only(self):
        category = Category.objects.create(name='Demo Category')
        end = timezone.now() + timedelta(hours=3)

        product = Product.objects.create(
            name='Demo Product',
            description='Demo product description',
            price=Decimal('100.00'),
            old_price=Decimal('120.00'),
            discount=0,
            temporary_discount=15,
            sale_end_at=end,
        )
        product.categories.add(category)

        self.assertEqual(product.temporary_discount, 15)
        self.assertEqual(product.sale_end_at, end)

    def test_product_form_and_admin_expose_optional_time_window_fields(self):
        self.assertNotIn('sale_start_at', ProductForm._meta.fields)
        self.assertIn('sale_end_at', ProductForm._meta.fields)

        basic_fields = dict(ProductAdmin.fieldsets)["Basic Information"]['fields']
        pricing_fields = dict(ProductAdmin.fieldsets)["Pricing"]['fields']

        self.assertNotIn('sale_start_at', basic_fields)
        self.assertIn('sale_end_at', pricing_fields)

    def test_project_timezone_is_uzbekistan_local(self):
        self.assertEqual(settings.TIME_ZONE, 'Asia/Tashkent')
