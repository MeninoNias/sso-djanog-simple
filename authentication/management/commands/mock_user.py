from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = 'Cria 1000 usuários'

    def handle(self, *args, **options):
        for i in range(1000):
            username = f'user_{i}'
            email = f'user_{i}@example.com'
            User.objects.create_user(username=username, email=email, password='123456')
            self.stdout.write(self.style.SUCCESS(f'Usuário criado: {username}'))
        
