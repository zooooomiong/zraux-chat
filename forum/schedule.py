from django.db import transaction
from .models import OrdinaryUser, Messages
from django.utils import timezone


def delete_last_day_messages():
    with transaction.atomic():
        messages = Messages.objects.all()
        for message in messages:
            try:
                if message.timestamp < timezone.now() - timezone.timedelta(days=1):
                    message.delete()
            except Exception as e:
                print(f"Error deleting message: {e}")

def make_users_offline():
    with transaction.atomic():
        online_users = OrdinaryUser.objects.filter(status=1)
        for user in online_users:
            try:
                print(user)
                if user.time < timezone.now() - timezone.timedelta(seconds=10):
                    user.status = 0
                    user.save()
            except Exception as e:
                print(f"Error updating user status: {e}")

