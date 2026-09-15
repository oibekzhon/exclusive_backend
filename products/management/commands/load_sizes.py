import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from products.models import Size


class Command(BaseCommand):
    help = 'Load Size records from a JSON file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('--json-path', default='products/fixtures/sizes.json', help='Path to the JSON file containing the sizes list.')
        parser.add_argument('--clear', action='store_true', help='Delete all existing sizes before loading the JSON file.')

    def handle(self, *args, **options):
        json_path = Path(options['json_path'])
        if not json_path.exists():
            raise CommandError(f'JSON file was not found: {json_path}')

        try:
            data = json.loads(json_path.read_text(encoding='utf-8'))
        except Exception as exc:
            raise CommandError(f'Could not parse JSON file: {exc}') from exc

        sizes = data.get('sizes') or data.get('data') or data
        if not isinstance(sizes, list):
            raise CommandError('JSON file must contain a top-level "sizes" list or a list of strings.')

        if options['clear']:
            Size.objects.all().delete()

        created = 0
        skipped = 0
        for name in sizes:
            if not isinstance(name, str):
                skipped += 1
                continue
            name = name.strip()
            if not name:
                skipped += 1
                continue
            obj, was_created = Size.objects.get_or_create(name=name)
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Loaded {created} new size records and skipped {skipped} invalid rows from {json_path}'
        ))
