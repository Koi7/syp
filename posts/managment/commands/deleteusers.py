from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Deletes all users in database'

    def handle(self, *args, **options):
        all_users = User.objects.all()
        for user in all_users:
            if user.username != "koi":
                user.delete()