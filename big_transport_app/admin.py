from django.contrib import admin
from big_transport_app.models import ContacterNous, Produits, Commander

# Register your models here.
class ContacterNousTableau(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'message')

class ProduitsTableau(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')

class CommanderTableau(admin.ModelAdmin):
    list_display = ('name', 'lieu', 'phone', 'camion_type', 'nombre_cubage')
    
admin.site.register(ContacterNous, ContacterNousTableau)
admin.site.register(Commander, CommanderTableau)
admin.site.register(Produits, ProduitsTableau)