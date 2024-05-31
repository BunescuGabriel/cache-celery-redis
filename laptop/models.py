from django.db import models

class Laptop(models.Model):
    model = models.CharField(max_length=200)
    anul = models.DateTimeField(auto_now_add=True)
    producator = models.CharField(max_length=200)
    procesor = models.CharField(max_length=30)
    descriere = models.TextField()
    price = models.FloatField()
    greutatea = models.FloatField()
    image = models.ImageField(upload_to='laptop/', max_length=300, null=True, default='')

    def __str__(self):
        return f" {self.model} {self.producator}"
    
    
class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.name
    
