import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Remove migrations and drop sqllite database'

    def handle(self, *args, **options):
        self.stdout.write('GET FRESH! Start over.')
        confirm = input(
            'You are about to nuke your database. Proceed? (Y/n) '
        )
        while 1:
            if confirm not in ('Y', 'n', 'yes', 'no'):
                confirm = input('Please enter either "yes" or "no": ')
                continue
            if confirm in ('Y', 'yes'):
                break
            else:
                return

        base_path = Path(settings.BASE_DIR)

        sqllite_path = base_path / 'db.sqlite3'
        if sqllite_path.exists():
            sqllite_path.unlink()

        for file in base_path.rglob('migrations/*.py'):
            if file.name != '__init__.py':
                file.unlink()

        os.system('python manage.py makemigrations')
        os.system('python manage.py migrate')

        self.stdout.write('All done!')
