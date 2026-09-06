from django.contrib import admin
from .models import CategoriePatrimoine, Patrimoine, Activite, GalerieImage, PageInformation, ContactMessage


@admin.register(CategoriePatrimoine)
class CategoriePatrimoineAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ordre']
    list_editable = ['ordre']
    search_fields = ['nom', 'description']


@admin.register(Patrimoine)
class PatrimoineAdmin(admin.ModelAdmin):
    list_display = ['titre', 'categorie', 'actif', 'date_ajout']
    list_filter = ['categorie', 'actif', 'date_ajout']
    search_fields = ['titre', 'description', 'localisation']
    date_hierarchy = 'date_ajout'


@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ['titre', 'statut', 'date_debut', 'lieu', 'organisateur']
    list_filter = ['statut', 'actif', 'date_debut']
    search_fields = ['titre', 'description', 'lieu']
    date_hierarchy = 'date_debut'
    # Utiliser HTMX pour les formulaires
    change_form_template = 'admin/change_form_htmx.html'


@admin.register(GalerieImage)
class GalerieImageAdmin(admin.ModelAdmin):
    list_display = ['activite', 'ordre', 'image_thumb']
    list_editable = ['ordre']
    search_fields = ['activite__titre', 'legende']

    def image_thumb(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" style="object-fit:cover;">'
        return "Pas d'image"
    image_thumb.allow_tags = True
    image_thumb.short_description = "Image"


@admin.register(PageInformation)
class PageInformationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'slug', 'actif']
    list_editable = ['slug', 'actif']
    search_fields = ['titre', 'slug', 'contenu']
    prepopulated_fields = {'slug': ('titre',)}


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'objet', 'lu', 'date_envoi']
    list_filter = ['lu', 'date_envoi']
    search_fields = ['nom', 'email', 'objet', 'message']
    readonly_fields = ['date_envoi']