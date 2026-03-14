from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Reset admin password"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        email = "admin@example.com"
        new_password = "admin123"

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            self.stdout.write(self.style.SUCCESS("Admin password reset"))
        except User.DoesNotExist:
            self.stdout.write("Admin user not found")