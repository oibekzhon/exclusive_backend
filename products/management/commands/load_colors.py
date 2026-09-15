import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from products.models import Color


class Command(BaseCommand):
    help = 'Load Color records from a JSON file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('--json-path', default='products/fixtures/colors.json', help='Path to JSON file containing color records.')
        parser.add_argument('--clear', action='store_true', help='Delete all existing color rows before loading the JSON file.')

    def handle(self, *args, **options):
        json_path = Path(options['json_path'])
        if not json_path.exists():
            raise CommandError(f'JSON file was not found: {json_path}')

        try:
            data = json.loads(json_path.read_text(encoding='utf-8'))
        except Exception as exc:
            raise CommandError(f'Could not parse JSON file: {exc}') from exc

        colors = data.get('colors') or data.get('data') or data
        if not isinstance(colors, list):
            raise CommandError('JSON file must contain a top-level "colors" list of objects.')

        if options['clear']:
            Color.objects.all().delete()

        created = 0
        updated = 0
        skipped = 0

        for row in colors:
            if not isinstance(row, dict):
                skipped += 1
                continue

            name = (row.get('name') or '').strip()
            hex_code = (row.get('hex_code') or '').strip().upper() or '#000000'
            if not name:
                skipped += 1
                continue

            # First match: same hex code regardless of name case
            existing_by_hex = Color.objects.filter(hex_code__iexact=hex_code).first()
            if existing_by_hex:
                if existing_by_hex.name != name:
                    # If a different canonical name already exists in the table, merge by replacing the record's label.
                    other = Color.objects.filter(name__iexact=name).first()
                    if other and other.pk != existing_by_hex.pk:
                        other.delete()
                    existing_by_hex.name = name
                    existing_by_hex.hex_code = hex_code
                    existing_by_hex.save(update_fields=['name', 'hex_code'])
                else:
                    existing_by_hex.hex_code = hex_code
                    existing_by_hex.save(update_fields=['hex_code'])
                updated += 1
                continue

            # Second match: same case-insensitive color name
            existing_by_name = Color.objects.filter(name__iexact=name).first()
            if existing_by_name:
                existing_by_name.hex_code = hex_code
                existing_by_name.save(update_fields=['hex_code'])
                updated += 1
                continue

            Color.objects.create(name=name, hex_code=hex_code)
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Loaded {created} new color records, updated {updated} color records, and skipped {skipped} invalid rows from {json_path}'
        ))
