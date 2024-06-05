from django.db import models
from users.models import CustomUser
from decimal import Decimal
from django.utils import timezone


class Telefon(models.Model):
    model = models.CharField(max_length=200)
    anul = models.DateTimeField(auto_now_add=True)
    producator = models.CharField(max_length=200)
    procesor = models.CharField(max_length=30)
    descriere = models.TextField()
    price = models.FloatField()

    
    def __str__(self):
        return f" {self.model} {self.producator}"
    
    
class Images(models.Model):
    image = models.ImageField(upload_to='telefon/', max_length=300, null=True, default='')
    telefon = models.ForeignKey(Telefon, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.telefon}"
    
    
class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    telefon = models.ForeignKey(Telefon, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.telefon.model} - {self.quantity}"
    
class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return f"Payment {self.id} by {self.user.username}"


    

