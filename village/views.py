from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count
from django.utils import timezone
from .models import (
    CategoriePatrimoine, Patrimoine, Activite,
    GalerieImage, PageInformation, ContactMessage
)


class AccueilView(TemplateView):
    template_name = 'village/accueil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Patrimoines par catégorie
        context['categories_patrimoine'] = CategoriePatrimoine.objects.filter(
            patrimoines__actif=True
        ).distinct().prefetch_related('patrimoines')[:6]

        # Prochaines activités
        context['prochaines_activites'] = Activite.objects.filter(
            statut='a_venir',
            date_debut__gte=timezone.now(),
            actif=True
        )[:3]

        # Activités passées récentes
        context['activites_passees'] = Activite.objects.filter(
            statut='passe',
            actif=True
        ).order_by('-date_debut')[:3]

        # Page d'information principale
        context['page_accueil'] = PageInformation.objects.filter(slug='accueil', actif=True).first()

        return context


class ListePatrimoinesView(ListView):
    model = Patrimoine
    template_name = 'village/patrimoines.html'
    context_object_name = 'patrimoines'
    paginate_by = 12

    def get_queryset(self):
        queryset = Patrimoine.objects.filter(actif=True)
        categorie_slug = self.kwargs.get('categorie_slug')
        if categorie_slug:
            queryset = queryset.filter(categorie__slug=categorie_slug)
        return queryset.select_related('categorie')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoriePatrimoine.objects.annotate(
            nombre_patrimoines=Count('patrimoines')
        ).filter(patrimoines__actif=True).distinct()
        return context


class DetailPatrimoineView(DetailView):
    model = Patrimoine
    template_name = 'village/detail_patrimoine.html'
    context_object_name = 'patrimoine'


class ListeActivitesView(ListView):
    model = Activite
    template_name = 'village/activites.html'
    context_object_name = 'activites'

    def get_queryset(self):
        statut = self.kwargs.get('statut', 'a_venir')
        return Activite.objects.filter(statut=statut, actif=True)


class DetailActiviteView(DetailView):
    model = Activite
    template_name = 'village/detail_activite.html'
    context_object_name = 'activite'


class ListePagesView(ListView):
    model = PageInformation
    template_name = 'village/liste_infos.html'
    context_object_name = 'pages'

    def get_queryset(self):
        return PageInformation.objects.filter(actif=True)


class DetailPageView(DetailView):
    model = PageInformation
    template_name = 'village/detail_page.html'
    context_object_name = 'page'

    def get_queryset(self):
        return PageInformation.objects.filter(actif=True)


class ContactView(TemplateView):
    template_name = 'village/contact.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            nom = request.POST.get('nom')
            email = request.POST.get('email')
            objet = request.POST.get('objet')
            message = request.POST.get('message')

            if nom and email and message:
                ContactMessage.objects.create(
                    nom=nom, email=email, objet=objet, message=message
                )
                return render(request, 'village/contact_success.html')

        return self.get(request, *args, **kwargs)


# Vues admin HTMX pour les galeries
@method_decorator(staff_member_required, name='dispatch')
class GalerieActiviteHTMXView(DetailView):
    model = Activite
    template_name = 'admin/village/partials/galerie_form.html'
    context_object_name = 'activite'