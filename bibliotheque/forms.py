from django import forms
from .models import UtilisateurBibliotheque
from .models import Livre


class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['titre', 'auteur', 'genre', 'annee_publication', 'exemplaires_disponibles', 'image']


class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = UtilisateurBibliotheque
        fields = ['username', 'email', 'adresse', 'telephone', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
