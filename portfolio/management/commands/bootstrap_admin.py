import os

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create a Django admin from deployment environment variables if the username is new."

    def handle(self, *args, **options):
        username = os.getenv("PORTFOLIO_ADMIN_USERNAME", "").strip()
        password = os.getenv("PORTFOLIO_ADMIN_PASSWORD", "")
        if not username and not password:
            return
        if not username or not password:
            raise CommandError("Set both PORTFOLIO_ADMIN_USERNAME and PORTFOLIO_ADMIN_PASSWORD.")

        users = get_user_model()
        if users.objects.filter(username=username).exists():
            self.stdout.write("Bootstrap username already exists. Its credentials and permissions were preserved.")
            return

        try:
            user = users(username=username)
            user.full_clean(exclude=["password"], validate_unique=False)
            validate_password(password, user)
        except ValidationError as exc:
            raise CommandError("Choose a valid username and a strong, unique admin password.") from exc

        _, created = users.objects.get_or_create(
            username=username,
            defaults={"password": make_password(password), "is_staff": True, "is_superuser": True},
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Admin account created. Remove the bootstrap environment variables."))
