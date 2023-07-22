from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=50,unique=True)
    def __str__(self):
        return f"{self.name}"

class Transaction(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Amount=models.DecimalField(max_digits=15,decimal_places=2)
    Type=models.CharField(max_length=1,choices=[('I','Income'),('E','Expense')])
    Category=models.ForeignKey(Category,on_delete=models.CASCADE)
    Date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} {"-" if self.Type=="E" else "+" }{self.Amount}'
    
class Balance(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Amount=models.DecimalField(max_digits=15,decimal_places=2)
    def __str__(self):
        return f"{self.user.username} - {self.Amount}"
