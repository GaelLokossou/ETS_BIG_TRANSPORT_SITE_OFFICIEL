from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Categories(models.Model):
    titre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.titre

class Annonces(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
    
class AnnoncePhoto(models.Model):
    annonce = models.ForeignKey(Annonces, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="annonces/")

from django.db import models

class Agents(models.Model):
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=100)
    poste = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='agents/')  # Dossier où seront stockées les images

    def __str__(self):
        return f"{self.nom} {self.prenoms} - {self.poste}"


class Commander(models.Model):
    # Attributs pour le modèle
    name = models.CharField(max_length=100, verbose_name="Nom")
    lieu = models.CharField(max_length=200, verbose_name="Lieu / Quartier")
    phone = models.CharField(max_length=30, verbose_name="Numéro de téléphone")
    annonce = models.ForeignKey(
        Annonces, 
        on_delete=models.CASCADE, 
        verbose_name="Annonce associée", 
        related_name="commandes"
    )

    
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
        help_text="Spécifier si le choix principal est 'Type de camion'",
    )
    nombre_voyage = models.PositiveIntegerField(max_length=1000000, verbose_name="Nombre de voyage", null=True, blank=True)
    nombre_cubage = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        verbose_name="Nombre de cubage",
        help_text="Spécifier si le choix principal est 'Nombre de cubage",
        default=0
    )

    def __str__(self):
        return f"Commande de {self.name}"
