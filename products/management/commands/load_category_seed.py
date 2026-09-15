import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from products.models import Category


class Command(BaseCommand):
    help = 'Load the required category seed list from a JSON file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('--json-path', default='products/fixtures/category_seed.json', help='Path to the seed JSON file.')
        parser.add_argument('--clear', action='store_true', help='Delete all existing categories before loading the seed.')

    def handle(self, *args, **options):
        json_path = Path(options['json_path'])
        if not json_path.exists():
            raise CommandError(f'JSON file was not found: {json_path}')

        try:
            data = json.loads(json_path.read_text(encoding='utf-8'))
        except Exception as exc:
            raise CommandError(f'Could not parse JSON file: {exc}') from exc

        categories = data.get('categories') or data.get('data') or data
        if not isinstance(categories, list):
            raise CommandError('JSON file must contain a top-level "categories" list of strings.')

        if options['clear']:
            Category.objects.all().delete()

        created = 0
        skipped = 0
        for raw in categories:
            if not isinstance(raw, str):
                skipped += 1
                continue
            name = raw.strip()
            if not name:
                skipped += 1
                continue
            obj, was_created = Category.objects.get_or_create(name=name)
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Loaded {created} new category records and skipped {skipped} invalid rows from {json_path}'
        ))
