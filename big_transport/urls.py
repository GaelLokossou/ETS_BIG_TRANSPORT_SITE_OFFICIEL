from big_transport import settings
from .views import index, search
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('search/', search, name='search'),
]

# Ajoutez cette ligne pour servir les fichiers médias
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)