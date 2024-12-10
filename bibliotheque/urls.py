from django.urls import path
from django.views.generic import DetailView

from . import views
from .models import Livre
from .views import connexion, accueil
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('livres/', views.liste_livres, name='liste_livres'),
    path('livre/<int:pk>/', DetailView.as_view(model=Livre), name='livre_detail'),
    path('livres/create/', views.create_livre, name='create_livre'),  # Créer un livre
    path('livres/update/<int:livre_id>/', views.update_livre, name='update_livre'),  # Modifier un livre
    path('livres/delete/<int:livre_id>/', views.delete_livre, name='delete_livre'),  # Supprimer un livre
    path('', views.accueil, name='accueil'),
    path('emprunter/<int:livre_id>/', views.emprunter_livre, name='emprunter_livre'),

    path('retourner/<int:emprunt_id>/', views.retourner_livre, name='retourner_livre'),
    path('historique/', views.historique_emprunts, name='historique_emprunts'),

    path('utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('utilisateurs/creer/', views.creer_utilisateur, name='creer_utilisateur'),
    path('connexion/', connexion, name='connexion'),
    path('', accueil, name='accueil'),  # L'URL pour la page d'accueil
    path('emprunter/<int:livre_id>/', views.emprunter_livre, name='emprunter_livre'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('search/', views.search_books, name='search_books'),
]
