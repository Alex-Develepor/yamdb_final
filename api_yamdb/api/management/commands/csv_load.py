import csv
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.exceptions import FieldError
from django.core.management.base import BaseCommand

SOURCE_DIR = Path(settings.BASE_DIR) / 'static/data/'

# Follow the inheritance of primary Keys, rabbit...
SOURCE_APP_DICT = {
    'user': 'users',
    'category': 'reviews',
    'genre': 'reviews',
    'title': 'reviews',
    'title_genre': 'reviews',
    'review': 'reviews',
    'comment': 'reviews',
}


class Command(BaseCommand):
    help = 'Load initial data to sqllite from .csv'

    def handle(self, *args, **options):
        confirm = input(
            'You are about to bloat your database. Proceed? (Y/n) '
        )
        while 1:
            if confirm not in ('Y', 'n', 'yes', 'no'):
                confirm = input('Please enter either "yes" or "no": ')
                continue
            if confirm in ('Y', 'yes'):
                break
            else:
                return
        for file_short_name in SOURCE_APP_DICT.keys():
            file_path = SOURCE_DIR / (file_short_name + '.csv')
            parse_csv_file(file_path, file_short_name)


def parse_csv_file(file_path: Path, file_short_name: str) -> None:
    """Parse csv file and load it to DB."""
    with open(file_path) as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            print(f'Wrong or empty file. Please check: \n {file_path.name}')
            exit()

        model = apps.get_model(
            app_label=SOURCE_APP_DICT[file_short_name],
            model_name=file_short_name)

        for row in reader:
            object_dict = {key: value for key, value in zip(header, row)}
            try:
                model.objects.update_or_create(**object_dict)
            except FieldError:
                print(f'Wrong file type: Please check: \n {file_path.name}')
                exit()
        print(f'Data from file {file_path.name} successfully loaded to DB')
