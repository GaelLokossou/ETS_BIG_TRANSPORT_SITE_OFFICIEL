from django.contrib import admin
from big_transport_app.models import ContactMessage, Categories, Commander, Annonces, AnnoncePhoto

# Register your models here.
class ContacterNousTableau(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'message')

class AnnoncesTableau(admin.ModelAdmin):
    list_display = ('titre','date_creation', 'prix', 'category', 'description')

class CommanderTableau(admin.ModelAdmin):
    list_display = ('name', 'lieu', 'phone', 'camion_type', 'nombre_cubage')
    
admin.site.register(ContactMessage, ContacterNousTableau)
admin.site.register(Commander, CommanderTableau)
admin.site.register(Annonces, AnnoncesTableau)