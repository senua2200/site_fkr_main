from django.db import models

class Purchase_history(models.Model):
    type = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    date = models.DateField(auto_now_add=True)
    price = models.IntegerField()
    link_file = models.URLField()
    
class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
    number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    purchase_history_id = models.ForeignKey(to=Purchase_history, on_delete=models.CASCADE, null=True, blank=True)


