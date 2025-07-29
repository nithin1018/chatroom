from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db import OperationalError

class ChatappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chatapp"
    def ready(self):
        try:
            User = get_user_model()
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='1234'
                )
        except OperationalError:
            # DB might not be ready during migration
            pass