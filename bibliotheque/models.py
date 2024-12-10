# models.py
from django.db import models
from django.contrib.auth.models import User

from tp_django import settings


# Gestion des livres
class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    annee_publication = models.IntegerField()
    exemplaires_disponibles = models.IntegerField()
    image = models.ImageField(upload_to='livres/', null=True, blank=True)  # Champ pour l'image du livre
    summary = models.TextField(blank=True, null=True)  # Add this field
    def __str__(self):
        return self.titre


# Gestion des utilisateurs
from django.contrib.auth.models import AbstractUser
from django.db import models


class UtilisateurBibliotheque(AbstractUser):
    # Ajout de champs spécifiques si nécessaire
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='utilisateur_bibliotheque', null=True, blank=True)

    adresse = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


# Gestion des emprunts
class Emprunt(models.Model):
    utilisateur = models.ForeignKey(UtilisateurBibliotheque, on_delete=models.CASCADE, related_name='emprunts')
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='emprunts_utilisateur')
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour = models.DateTimeField(null=True, blank=True)
    est_retourne = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.livre.titre}"
