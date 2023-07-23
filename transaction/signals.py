from decimal import Decimal
from django.db import models
from django.db.models import DecimalField,F
from django.db.models.signals import post_save,pre_save,pre_delete
from django.dispatch import receiver
from .models import Transaction

@receiver(pre_save,sender=Transaction)
def transaction_post_save(sender,instance,**kwargs):
    if instance.pk is not None:
        old_object = Transaction.objects.get(pk=instance.pk)
        new_object_amount = Decimal(instance.Amount)
        old_object_amount = Decimal(old_object.Amount)
        old_amount = Decimal(instance.user.balance.Amount)
        
        if instance.Type != old_object.Type:
            if instance.Type == 'I': 
                instance.user.balance.Amount =old_amount + new_object_amount+old_object_amount
            elif instance.Type == 'E':
                instance.user.balance.Amount =old_amount - new_object_amount-old_object_amount
        else:
            if instance.Type == 'I':
                instance.user.balance.Amount =old_amount + new_object_amount-old_object_amount
            else:
                instance.user.balance.Amount =old_amount - new_object_amount+old_object_amount

        instance.user.balance.save()

@receiver(post_save,sender=Transaction)
def transaction_post_save(sender,instance,created,**kwargs):
    if created:
        new_amount = Decimal(instance.Amount)
        old_amount = Decimal(instance.user.balance.Amount)
        # print(dir(instance.user.balance.up))
        if instance.Type=='I':
            instance.user.balance.Amount=old_amount+new_amount
        else:
            instance.user.balance.Amount=old_amount-new_amount
        instance.user.balance.save()


@receiver(pre_delete,sender=Transaction)
def transaction_pre_delete(sender,instance,**kwargs):
    amount = instance.Amount
    if instance.Type=='I':
        instance.user.balance.Amount-=amount
    else:
        instance.user.balance.Amount+=amount
    instance.user.balance.save()