import random
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django_seed import Seed
from users.models import User
from posts.models import Post
from comments.models import Comment


DEFAULT_COUNT = 50

class Command(BaseCommand):
    help = 'this command hello'

    def add_arguments(self, parser):
        parser.add_argument('--count', default=DEFAULT_COUNT, type=int, help='how many time show message')

    def handle(self, *args, **options):
        count = options.get('count', 50)

        users = User.objects.all()
        posts = Post.objects.all()
        commentable = ContentType.objects.get(model='post')

        seeder = Seed.seeder('ko_KR')
        seeder.add_entity(Comment, count, {
            'user': lambda x: random.choice(users),
            'commentable_id': lambda x: random.choice(posts).id,
            'commentable_type': commentable,
            'deleted_at': None
        })

        seeder.execute()