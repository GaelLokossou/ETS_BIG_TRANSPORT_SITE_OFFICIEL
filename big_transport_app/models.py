from django.db import models

class ContacterNous(models.Model):
    name = models.fields.CharField(max_length=100)
    email = models.fields.EmailField()
    phone = models.fields.CharField(max_length=30)
    message = models.fields.TextField()

    def __str__(self):
        return self.name
    
class Produits(models.Model):
    name = models.CharField(max_length=255)  # Nom du produit
    description = models.TextField(blank=True)  # Description facultative
    image = models.ImageField(upload_to='produits/', blank=True)  # Image du produit

    def __str__(self):
        return self.name