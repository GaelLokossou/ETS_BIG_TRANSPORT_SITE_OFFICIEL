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
    

class Commander(models.Model):
    # Attributs pour le modèle
    name = models.CharField(max_length=100, verbose_name="Nom")
    lieu = models.CharField(max_length=200, verbose_name="Lieu / Quartier")
    phone = models.CharField(max_length=30, verbose_name="Numéro de téléphone")
    
    # Pour le choix principal : type de camion ou nombre de cubage
    CHOIX_PRINCIPAL = [
        ('type_camion', 'Type de camion'),
        ('nombre_cubage', 'Nombre de cubage'),
    ]
    choix_principal = models.CharField(max_length=20, choices=CHOIX_PRINCIPAL, verbose_name="Choix principal")

    # Détails supplémentaires
    camion_type = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name="Type de camion",
        help_text="Spécifier si le choix principal est 'Type de camion'"
    )
    nombre_cubage = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        verbose_name="Nombre de cubage",
        help_text="Spécifier si le choix principal est 'Nombre de cubage'"
    )

    def __str__(self):
        return f"Commande de {self.name}"
