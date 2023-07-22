from django.db import models
from django.db.models.signals import post_save,pre_save,pre_delete
from django.dispatch import receiver
from .models import Transaction

@receiver(post_save,sender=Transaction)
def transaction_post_save(sender,instance,created,**kwargs):
    if created:
        amount = instance.Amount
        if instance.Type=='I':
            instance.user.balance.Amount+=amount
        else:
            instance.user.balance.Amount-=amount
    else:
        # Retrieve the old object from the database
        old_object = Transaction.objects.get(pk=instance.pk)
        if instance.Type != old_object.Type:
            # Handle the change in Type
            if instance.Type == 'I':
                # The transaction changed to Income
                # Increase the user's balance by the difference in Amount
                balance_diff = instance.Amount - old_object.Amount
                instance.user.balance += balance_diff
            elif instance.Type == 'E':
                # The transaction changed to Expense
                # Decrease the user's balance by the difference in Amount
                balance_diff = old_object.Amount - instance.Amount
                instance.user.balance -= balance_diff
        else:
            balance_diff = instance.Amount - old_object.Amount
            instance.user.balance += balance_diff

        # Save the updated user's balance
    instance.user.balance.save()

@receiver(pre_delete,sender=Transaction)
def transaction_pre_delete(sender,instance,**kwargs):
    amount = instance.Amount
    if instance.Type=='I':
        instance.user.balance.Amount-=amount
    else:
        instance.user.balance.Amount+=amount
    instance.user.balance.save()