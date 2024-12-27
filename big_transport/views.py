from django.shortcuts import redirect, render
from django.contrib import messages
from big_transport_app.models import ContacterNous, Produits
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
