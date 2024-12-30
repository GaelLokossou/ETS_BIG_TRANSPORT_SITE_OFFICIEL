from django.shortcuts import redirect, render
from django.contrib import messages
from big_transport_app.models import Commander, ContacterNous, Produits
from django.core.mail import send_mail

def index(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        # Créer un nouvel objet ContacterNous et l'enregistrer
        ContacterNous.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )

        # Composition de l'email
        subject = f"Nouveau message de {name}"
        email_message = f"De: {name}.\nNumero de telephone : {phone}.\nEmail : <{email}>.\n\n{message}"
        from_email = 'lxolalikokouguek@gmail.com'
        recipient_list = ['lxolalikokouguel@gmail.com']
        # Envoi de l'email
        send_mail(subject, email_message, from_email, recipient_list)

        messages.success(request, "Votre message a été envoyé avec succès!")
        return redirect('index')
    return render(request, 'index.html')

def search(request):
    query = request.GET.get('search', '')  # Récupère la valeur de la recherche
    donnees = Produits.objects.filter(name__icontains=query) if query else []  # Recherche dans la base de données

    context = {
        'donnees': donnees,
        'query': query,
        'aucune_recherche': not donnees.exists() if query else False  # Vérifie s'il y a des résultats
    }
    return render(request, "search.html", context)

def commander(request):
    if request.method == 'POST':
        # Récupération des données du formulaire
        name = request.POST['name']
        lieu = request.POST['lieu']
        phone = request.POST['number']
        choix_principal = request.POST['choix_principal']
        camion_type = request.POST.get('camion_type')  # Peut être None si non fourni
        nombre_cubage = request.POST.get('nombre_cubage')  # Peut être None si non fourni

        # Création d'un nouvel objet Commander
        Commander.objects.create(
            name=name,
            lieu=lieu,
            phone=phone,
            choix_principal=choix_principal,
            camion_type=camion_type if choix_principal == 'type_camion' else None,
            nombre_cubage=nombre_cubage if choix_principal == 'nombre_cubage' else None
        )

        # Composition de l'email
        subject = f"Nouvelle commande de {name}"
        email_message = (
            f"Nom : {name}\n"
            f"Lieu : {lieu}\n"
            f"Téléphone : {phone}\n"
            f"Choix principal : {choix_principal}\n"
            f"Type de camion : {camion_type if camion_type else 'Non spécifié'}\n"
            f"Nombre de cubage : {nombre_cubage if nombre_cubage else 'Non spécifié'}"
        )
        from_email = 'lxolalikokouguek@gmail.com'
        recipient_list = ['lxolalikokouguel@gmail.com']
        
        # Envoi de l'email
        send_mail(subject, email_message, from_email, recipient_list)

        messages.success(request, "Votre commande a été enregistrée avec succès!")
        return redirect('index')  # Rediriger vers la page d'accueil ou une autre page

    return render(request, 'commander.html')