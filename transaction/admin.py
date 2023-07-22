from django.contrib import admin
from .models import Transaction,Category,Balance
# Register your models here.

admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(Balance)