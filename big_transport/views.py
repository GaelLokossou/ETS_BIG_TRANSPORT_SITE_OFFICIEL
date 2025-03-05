from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from big_transport_app.models import Commander, ContactMessage, Categories, Annonces, AnnoncePhoto
from django.core.mail import send_mail

def index(request):
# Récupérer les annonces les plus récentes (ou selon tes besoins)
    annonces = Annonces.objects.all().order_by('-id')[:5]  # 5 annonces les plus récentes

    return render(request, 'index.html', {'annonces': annonces})

def search(request):
    query = request.GET.get('search', '')  # Récupère la valeur de la recherche
    donnees = Annonces.objects.filter(titre__icontains=query) if query else []  # Recherche dans la base de données

    context = {
        'donnees': donnees,
        'query': query,
        'aucune_recherche': not donnees.exists() if query else False  # Vérifie s'il y a des résultats
    }
    return render(request, "search.html", context)

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from django.contrib import messages
import uuid

def commander(request):
    if request.method == 'POST':
        # Récupération des données du formulaire
        name = request.POST.get('name', 'Inconnu')
        lieu = request.POST.get('lieu', 'Non spécifié')
        phone = request.POST.get('number', 'Non spécifié')
        choix_principal = request.POST.get('choix_principal', 'Non spécifié')
        camion_type = request.POST.get('camion_type', 'Non spécifié') if choix_principal == 'type_camion' else 'N/A'
        nombre_cubage = request.POST.get('nombre_cubage', 'Non spécifié') if choix_principal == 'nombre_cubage' else 'N/A'
        nombre_voyage = request.POST.get('nombre_voyage', 'Non spécifié') if choix_principal == 'type_camion' else 'N/A'

        # Générer un ID unique pour la commande
        commande_id = str(uuid.uuid4())[:8]  # ID court pour référence

        # Création de la commande en base de données
        Commander.objects.create(
            name=name,
            lieu=lieu,
            phone=phone,
            choix_principal=choix_principal,
            camion_type=camion_type if choix_principal == 'type_camion' else None,
            nombre_voyage=nombre_voyage if choix_principal == 'type_camion' else None,
            nombre_cubage=nombre_cubage if choix_principal == 'nombre_cubage' else None
        )

        # Construction du corps du message HTML
        html_message = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .header {{
                        background-color: #663399;
                        color: white;
                        padding: 10px;
                        text-align: center;
                    }}
                    .content {{ padding: 10px; }}
                    .footer {{
                        text-align: center;
                        background-color: #6A0DAD;
                        color: white;
                        padding: 10px;
                        margin-top: 20px;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 10px;
                    }}
                    th, td {{
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #663399;
                        color: white;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h2>📢 Nouvelle Commande Reçue !</h2>
                </div>
                <div class="content">
                    <p>Une nouvelle commande a été passée par <strong>{name}</strong>.</p>
                    <h3>Détails de la commande :</h3>
                    <table>
                        <tr><th>Référence</th><td>{commande_id}</td></tr>
                        <tr><th>Nom</th><td>{name}</td></tr>
                        <tr><th>Lieu</th><td>{lieu}</td></tr>
                        <tr><th>Téléphone</th><td>{phone}</td></tr>
                        <tr><th>Choix principal</th><td>{choix_principal}</td></tr>
                        <tr><th>Type de camion</th><td>{camion_type}</td></tr>
                        <tr><th>Nombre de voyages</th><td>{nombre_voyage}</td></tr>
                        <tr><th>Nombre de cubage</th><td>{nombre_cubage}</td></tr>
                    </table>
                </div>
                <div class="footer">
                    <p>Merci de traiter cette commande rapidement.</p>
                </div>
            </body>
            </html>
        """

        # Version texte brut pour les clients qui ne supportent pas HTML
        plain_message = strip_tags(html_message)

        # Envoi de l'email
        email = EmailMessage(
            subject=f"Nouvelle commande #{commande_id} de {name}",
            body=html_message,
            from_email="lxolalikokouguel@gmail.com",
            to=["lxolalikokouguel@gmail.com"],
        )
        email.content_subtype = "html"  # Indique que le contenu est HTML
        email.send()

        messages.success(request, "Votre commande a été enregistrée avec succès !")
        return redirect('index')  # Redirection après soumission

    return render(request, 'commander.html')

def admin_site(request):
    return render(request, 'admin/admin.html')

def annonce_index(request):
        # Récupérer toutes les annonces, tu peux ajouter des filtres ici si nécessaire
    annonces = Annonces.objects.all().order_by('-id')  # Tri par ID décroissant

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(annonces, 6)  # 6 annonces par page
    page_number = request.GET.get('page')
    annonces_page = paginator.get_page(page_number)

    # Passer les annonces à la vue
    return render(request, 'admin/annonce_index.html', {'annonces': annonces_page})

def detail_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonces, id=annonce_id)
    return render(request, 'annonce_single.html', {'annonce': annonce})
def create_annonce(request):
    categories = Categories.objects.all()  # Récupère toutes les catégories

    if request.method == "POST":
        titre = request.POST.get("titre")
        description = request.POST.get("description")
        category_id = request.POST.get("categoryId")
        prix = request.POST.get("prix")
        photos = request.FILES.getlist("photos")

        # Vérification des champs obligatoires
        if not titre or not description or not category_id or not prix:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return render(request, "admin/create_annonce.html", {"categories": categories})

        # Vérifier si la catégorie existe
        try:
            category = Categories.objects.get(id=category_id)
        except Categories.DoesNotExist:
            messages.error(request, "La catégorie sélectionnée est invalide.")
            return render(request, "admin/create_annonce.html", {"categories": categories})

        # Création de l'annonce
        annonce = Annonces.objects.create(
            titre=titre,
            description=description,
            category=category,
            prix=prix,
        )

        # Enregistrer les images (dans le modèle AnnoncePhoto)
        for photo in photos:
            annonce_photo = AnnoncePhoto.objects.create(annonce=annonce, image=photo)

        messages.success(request, "Votre annonce a été créée avec succès !")

    return render(request, "admin/create_annonce.html", {"categories": categories})

def supprimer_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonces, id=annonce_id)
    if request.method == "POST":
        annonce.delete()
        messages.success(request, "L'annonce a été supprimée avec succès.")
    return redirect('annonce-index')

def edit_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonces, id=annonce_id)
    categories = Categories.objects.all()
    
    if request.method == "POST":
        titre = request.POST.get("titre")
        description = request.POST.get("description")
        prix = request.POST.get("prix")
        category_id = request.POST.get("categoryId")
        image = request.FILES.get("photos")
        
        # Mise à jour des champs
        annonce.titre = titre
        annonce.description = description
        annonce.prix = prix
        annonce.category_id = category_id if category_id else annonce.category_id
        
        # Mise à jour de l'image uniquement si une nouvelle image est fournie
        if image:
            annonce.image = image
        
        annonce.save()
        messages.success(request, "L'annonce a été mise à jour avec succès.")
        return redirect("annonce-index")  # Remplace par ta vue de redirection
    
    return render(request, "admin/edit_annonce.html", {"annonce": annonce, "categories": categories})

def create_categorie(request):
    if request.method == "POST":
        titre = request.POST.get("titre").strip()  # Supprime les espaces inutiles

        if not titre:
            messages.error(request, "Le titre est obligatoire.")
        elif Categories.objects.filter(titre=titre).exists():
            messages.error(request, "Cette catégorie existe déjà.")
        else:
            Categories.objects.create(titre=titre)
            messages.success(request, "Votre catégorie a été créée avec succès !")

    return render(request, 'admin/create_categorie.html')

def categorie_index(request):
    categories = Categories.objects.all()
    context = {'categories': categories}
    return render(request, 'admin/categorie_index.html', context)


from django.shortcuts import render, redirect
from django.contrib import messages

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('comment')

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            messages.success(request, "Votre message a été envoyée avec succès!")
            html_message = f"""
                <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; }}
                        .header {{
                            background-color: #663399;
                            color: white;
                            padding: 10px;
                            text-align: center;
                        }}
                        .content {{ padding: 10px; }}
                        .footer {{
                            text-align: center;
                            background-color: #6A0DAD;
                            color: white;
                            padding: 10px;
                            margin-top: 20px;
                        }}
                        table {{
                            width: 100%;
                            border-collapse: collapse;
                            margin-top: 10px;
                        }}
                        th, td {{
                            border: 1px solid #ddd;
                            padding: 8px;
                            text-align: left;
                        }}
                        th {{
                            background-color: #663399;
                            color: white;
                        }}
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h2>📢 Nouvelle Commande Reçue !</h2>
                    </div>
                    <div class="content">
                        <p>Une nouvelle commande a été passée par <strong>{name}</strong>.</p>
                        <h3>Détails de la commande :</h3>
                        <table>
                            <tr><th>Nom</th><td>{name}</td></tr>
                            <tr><th>Téléphone</th><td>{phone}</td></tr>
                            <tr><th>Email</th><td>{email}</td></tr>
                            <tr><th>Object</th><td>{subject}</td></tr>
                            <tr><th>Message</th><td>{message}</td></tr>
                        </table>
                    </div>
                    <div class="footer">
                        <p>Merci de traiter cette commande rapidement.</p>
                    </div>
                </body>
                </html>
            """

            # Version texte brut pour les clients qui ne supportent pas HTML
            plain_message = strip_tags(html_message)

            # Envoi de l'email
            email = EmailMessage(
                subject=f"Nouvelle message de {name}",
                body=html_message,
                from_email="lxolalikokouguel@gmail.com",
                to=["lxolalikokouguel@gmail.com"],
            )
            email.content_subtype = "html"  # Indique que le contenu est HTML
            email.send()
            return redirect('index')
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, 'contactus.html')

def produits(request):
    # Exemple de filtrage selon la catégorie
    category_name = "Location1"  # Tu peux adapter cette variable pour qu'elle provienne d'une requête ou d'une logique dynamique
    annonces = Annonces.objects.filter(category__titre=category_name)

    context = {
        'annonces': annonces,
    }

    return render(request, "produits.html", context)

def locations(request):
    # Exemple de filtrage selon la catégorie
    category_name = "Location2"  # Tu peux adapter cette variable pour qu'elle provienne d'une requête ou d'une logique dynamique
    annonces = Annonces.objects.filter(category__titre=category_name)

    context = {
        'annonces': annonces,
    }

    return render(request, "locations.html", context)

def agents(request):
    # agents = Agents.objects.select.all()
    # context = {
    #     'agents' : agents,
    # }

    return render(request, "agents.html")