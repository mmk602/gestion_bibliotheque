from django.contrib import admin
from .models import Livre, UtilisateurBibliotheque, Emprunt


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'genre', 'annee_publication', 'exemplaires_disponibles')
    search_fields = ('titre', 'auteur')


@admin.register(UtilisateurBibliotheque)
class UtilisateurBibliothequeAdmin(admin.ModelAdmin):
    list_display = ('get_utilisateur_name',)  # Fixed: Use a custom method
    search_fields = ('utilisateur__username',)

    # Custom method to display the user's username safely
    def get_utilisateur_name(self, obj):
        return obj.utilisateur.username if obj.utilisateur else "Aucun utilisateur"
    get_utilisateur_name.short_description = 'Utilisateur'


@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ('livre', 'utilisateur', 'date_emprunt', 'date_retour', 'est_retourne')
    search_fields = ('livre__titre', 'utilisateur__utilisateur__username')
    list_filter = ('est_retourne', 'date_emprunt')
