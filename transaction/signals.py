from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction

@receiver(post_save,sender=Transaction)
def transaction_post_save(sender,instance,**kwargs):
    if instance.Type=='I':
        instance.user.balance.amount+=instance.Amount
    else:
        instance.user.balance.amount-=instance.Amount
    instance.user.balance.save()
