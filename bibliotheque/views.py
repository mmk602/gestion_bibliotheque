from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Livre, Emprunt, UtilisateurBibliotheque
from django.utils.timezone import now
from .forms import UtilisateurForm, LivreForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib import messages  # Pour les messages d'erreur
from .forms import LoginForm  # Assurez-vous que le formulaire est bien importé
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test

current_date = datetime.now()


def is_admin(user):
    return user.is_staff


def connexion(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accueil')  # Redirect to the accueil page
            else:
                messages.error(request, "Identifiants invalides, veuillez réessayer.")
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


# Liste des livres
@user_passes_test(is_admin)
def liste_livres(request):
    livres = Livre.objects.all()
    return render(request, 'bibliotheque/liste_livres.html', {'livres': livres})


def create_livre(request):
    if request.method == 'POST':
        form = LivreForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_livres')  # Redirection vers la liste des livres
    else:
        form = LivreForm()

    return render(request, 'bibliotheque/creer_livre.html', {'form': form})


def update_livre(request, livre_id):
    livre = Livre.objects.get(id=livre_id)
    if request.method == 'POST':
        form = LivreForm(request.POST, request.FILES, instance=livre)
        if form.is_valid():
            form.save()
            return redirect('liste_livres')  # Redirection vers la liste des livres
    else:
        form = LivreForm(instance=livre)

    return render(request, 'bibliotheque/modifier_livre.html', {'form': form})


def delete_livre(request, livre_id):
    livre = Livre.objects.get(id=livre_id)
    if request.method == 'POST':
        livre.delete()
        return redirect('liste_livres')  # Redirection vers la liste des livres
    return render(request, 'bibliotheque/supprimer_livre.html', {'livre': livre})



def accueil(request):
    genres = Livre.objects.values_list('genre', flat=True).distinct()  # Fetch unique genres
    livres_by_genre = {genre: Livre.objects.filter(genre=genre) for genre in genres}  # Group books by genre
    return render(request, 'bibliotheque/accueil.html', {'livres_by_genre': livres_by_genre})

@login_required
def emprunter_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)

    # Check if the user already borrowed this book
    if Emprunt.objects.filter(utilisateur=request.user, livre=livre, date_retour__isnull=True).exists():
        messages.error(request, "Vous avez déjà emprunté un exemplaire de ce livre.")
        return redirect('accueil')

    # Check if there are copies available
    if livre.exemplaires_disponibles > 0:
        # Create a new loan entry
        Emprunt.objects.create(utilisateur=request.user, livre=livre, date_emprunt=current_date)
        livre.exemplaires_disponibles -= 1
        livre.save()
        messages.success(request, "Livre emprunté avec succès !")
    else:
        messages.error(request, "Aucun exemplaire disponible pour ce livre.")

    return redirect('accueil')


@login_required
def retourner_livre(request, emprunt_id):
    emprunt = get_object_or_404(Emprunt, id=emprunt_id)

    # Vérifier que l'emprunt appartient à l'utilisateur connecté et qu'il n'a pas encore été retourné
    if emprunt.utilisateur == request.user and emprunt.date_retour is None:
        # Marquer l'emprunt comme retourné
        emprunt.date_retour = current_date
        emprunt.save()

        # Rendre l'exemplaire disponible à nouveau
        livre = emprunt.livre
        livre.exemplaires_disponibles += 1
        livre.save()

        messages.success(request, f"Vous avez retourné le livre '{livre.titre}' avec succès.")
    else:
        messages.error(request, "Vous ne pouvez pas retourner ce livre.")

    return redirect('historique_emprunts')  # Rediriger vers la page de l'historique des emprunts


@login_required
def historique_emprunts(request):
    emprunts = Emprunt.objects.filter(utilisateur=request.user, date_retour__isnull=True)
    return render(request, 'bibliotheque/historique_emprunts.html', {'emprunts': emprunts})


@user_passes_test(is_admin)
def liste_utilisateurs(request):
    utilisateurs = UtilisateurBibliotheque.objects.all()
    return render(request, 'bibliotheque/liste_utilisateurs.html', {'utilisateurs': utilisateurs})


from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .forms import UtilisateurForm


def creer_utilisateur(request):
    if request.method == 'POST':
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            # Create the user instance but do not save yet
            user = form.save(commit=False)

            # Manually hash the password
            user.password = make_password(user.password)

            # Save the user instance
            user.save()

            # Redirect to the user list after creation
            return redirect('liste_utilisateurs')
    else:
        form = UtilisateurForm()

    return render(request, 'bibliotheque/creer_utilisateur.html', {'form': form})


def livre_detail(request, livre_id):
    livre = get_object_or_404(Livre, pk=pk)
    return render(request, 'bibliotheque/livre_detail.html', {'livre': livre})


def search_books(request):
    query = request.GET.get('query', '')  # Get the search query from the URL
    if query:
        livres = Livre.objects.filter(titre__icontains=query)  # Case-insensitive search
    else:
        livres = Livre.objects.none()  # Empty QuerySet if no search term

    return render(request, 'bibliotheque/search_results.html', {'livres': livres, 'query': query})


