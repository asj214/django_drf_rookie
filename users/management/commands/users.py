from uuid import uuid4
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django_seed import Seed
from users.models import User


DEFAULT_PASSWORD = 'rewq1234'
DEFAULT_COUNT = 50

class Command(BaseCommand):
    help = 'this command hello'

    def add_arguments(self, parser):
        parser.add_argument('--count', default=DEFAULT_COUNT, type=int, help='how many time show message')

    def handle(self, *args, **options):
        count = options.get('count', 50)
        seeder = Seed.seeder('ko_KR')
        seeder.add_entity(User, count, {
            'name': lambda x: seeder.faker.name(),
            'password': make_password(DEFAULT_PASSWORD),
            'is_superuser': False,
            'access_token': lambda x: uuid4(),
            'deleted_at': None
        })

        seeder.execute()