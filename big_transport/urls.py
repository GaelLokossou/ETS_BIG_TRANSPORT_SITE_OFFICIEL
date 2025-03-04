from big_transport import settings
from big_transport import views
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('commander/', views.commander, name='commander'),
    path('admin-site/', views.admin_site, name='admin-site'),
    path('admin-site/annonces/', views.annonce_index, name='annonce-index'),
    path('admin-site/categories/', views.categorie_index, name='categorie-index'),
    path('admin-site/create-annonce/', views.create_annonce, name='create-annonce'),
    path('admin-site/create-categorie/', views.create_categorie, name='create-categorie'),
    path('admin-site/annonce/<int:annonce_id>/supprimer/', views.supprimer_annonce, name='supprimer-annonce'),
    path('annonce/modifier/<int:annonce_id>/', views.edit_annonce, name='edit-annonce'),
    path('contacter/', views.contact_view, name='contact-us'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)