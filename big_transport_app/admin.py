from django.contrib import admin
from big_transport_app.models import ContacterNous, Produits

# Register your models here.
class ContacterNousTableau(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'message')

class ProduitsTableau(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')
    
admin.site.register(ContacterNous, ContacterNousTableau)
admin.site.register(Produits, ProduitsTableau)