from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

# User = get_user_model()
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(email=settings.SUPERUSER_EMAIL, username=settings.SUPERUSER_USERNAME).exists():
            User.objects.create_superuser(
                username=settings.SUPERUSER_USERNAME,
                first_name=settings.SUPERUSER_FIRSTNAME,
                last_name=settings.SUPERUSER_LASTNAME,
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD
            )
            print("Created superuser!")