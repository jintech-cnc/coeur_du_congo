from django.db import models
from django.utils.text import slugify


class CategoriePatrimoine(models.Model):
    """Catégorie de patrimoine (ex: artisanat, musique, danse, cuisine)"""
    nom = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Catégorie de patrimoine"
        verbose_name_plural = "Catégories de patrimoine"
        ordering = ['ordre']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class Patrimoine(models.Model):
    """Élément du patrimoine culturel du village"""
    titre = models.CharField(max_length=200, verbose_name="Titre")
    categorie = models.ForeignKey(
        CategoriePatrimoine, on_delete=models.SET_NULL, null=True,
        blank=True, verbose_name="Catégorie", related_name='patrimoines'
    )
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(upload_to='patrimoine/', blank=True, null=True, verbose_name="Image")
    video_url = models.URLField(blank=True, verbose_name="URL de la vidéo")
    localisation = models.CharField(max_length=200, blank=True, verbose_name="Localisation")
    createur = models.CharField(max_length=150, blank=True, verbose_name="Créateur / Détenteur du savoir")
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    actif = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Élément de patrimoine"
        verbose_name_plural = "Éléments de patrimoine"
        ordering = ['-date_ajout']

    def __str__(self):
        return self.titre


class Activite(models.Model):
    """Activité ou événement du village"""
    STATUT_CHOICES = [
        ('a_venir', 'À venir'),
        ('en_cours', 'En cours'),
        ('passe', 'Déjà eu lieu'),
    ]
    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    date_debut = models.DateTimeField(verbose_name="Date de début")
    date_fin = models.DateTimeField(blank=True, null=True, verbose_name="Date de fin")
    lieu = models.CharField(max_length=200, verbose_name="Lieu")
    organisateur = models.CharField(max_length=150, blank=True, verbose_name="Organisateur")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='a_venir')
    image_principale = models.ImageField(upload_to='activites/', blank=True, null=True, verbose_name="Image principale")
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    actif = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        ordering = ['date_debut']

    def __str__(self):
        return self.titre


class GalerieImage(models.Model):
    """Galerie d'images pour une activité"""
    activite = models.ForeignKey(
        Activite, on_delete=models.CASCADE, related_name='images', verbose_name="Activité"
    )
    image = models.ImageField(upload_to='activites/galerie/', verbose_name="Image")
    legende = models.CharField(max_length=200, blank=True, verbose_name="Légende")
    ordre = models.IntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "Image de galerie"
        verbose_name_plural = "Images de galerie"
        ordering = ['ordre']

    def __str__(self):
        return f"Image de {self.activite.titre}"


class PageInformation(models.Model):
    """Page d'information sur le village"""
    titre = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    contenu = models.TextField(verbose_name="Contenu")
    image_tete = models.ImageField(upload_to='pages/', blank=True, null=True, verbose_name="Image d'en-tête")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    actif = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Page d'information"
        verbose_name_plural = "Pages d'information"
        ordering = ['titre']

    def __str__(self):
        return self.titre


class ContactMessage(models.Model):
    """Message de contact"""
    nom = models.CharField(max_length=150, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    objet = models.CharField(max_length=200, verbose_name="Objet")
    message = models.TextField(verbose_name="Message")
    date_envoi = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    lu = models.BooleanField(default=False, verbose_name="Lu")

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-date_envoi']

    def __str__(self):
        return f"{self.nom} - {self.objet}"


class VisitCounter(models.Model):
    """Compteur de visites par page"""
    path = models.CharField(max_length=500, unique=True, verbose_name="Chemin URL")
    count = models.PositiveIntegerField(default=0, verbose_name="Nombre de visites")
    last_visit = models.DateTimeField(auto_now=True, verbose_name="Dernière visite")

    class Meta:
        verbose_name = "Compteur de visite"
        verbose_name_plural = "Compteurs de visite"
        ordering = ['-count']

    def __str__(self):
        return f"{self.path}: {self.count} visites"


class LoginAttempt(models.Model):
    """Suivi des tentatives de connexion pour le compte admin"""
    ip_address = models.GenericIPAddressField(verbose_name="Adresse IP")
    username = models.CharField(max_length=150, verbose_name="Nom d'utilisateur")
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Heure de la tentative")
    success = models.BooleanField(default=False, verbose_name="Réussie")

    class Meta:
        verbose_name = "Tentative de connexion"
        verbose_name_plural = "Tentatives de connexion"
        ordering = ['-attempt_time']

    def __str__(self):
        status = "✅" if self.success else "❌"
        return f"{status} {self.username} ({self.ip_address})"
