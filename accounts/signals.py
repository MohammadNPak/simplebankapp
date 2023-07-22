from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from transaction.models import Balance

@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    Balance.objects.create(user=instance,Amount="0.00")
