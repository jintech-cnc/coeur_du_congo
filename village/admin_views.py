"""
Vues personnalisees pour l'authentification admin avec limitation de tentatives.
"""
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views import decorators
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .auth_backend import (
    get_lockout_remaining_minutes,
    get_failed_attempts,
    MAX_ATTEMPTS,
    LOCKOUT_MINUTES,
)
from .models import LoginAttempt


def get_client_ip(request):
    """Recupere l'adresse IP du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    return ip


def admin_login(request):
    """
    Vue de connexion admin avec limitation de tentatives.
    Affiche un message clair quand l'IP est bloquee.
    """
    template_name = 'admin/login.html'

    # Redirection si deja connecte
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('admin:index'))

    # Recupere l'IP du client
    ip_address = get_client_ip(request)

    # Contexte de base
    context = {
        'title': 'Connexion',
        'app_path': request.get_full_path(),
        'next': request.GET.get('next', reverse('admin:index')),
    }

    # Verifier si l'IP est bloquee
    lockout_minutes = get_lockout_remaining_minutes(ip_address)
    if lockout_minutes > 0:
        context['lockout'] = True
        context['lockout_minutes'] = lockout_minutes
        context['remaining_attempts'] = 0
        return render(request, template_name, context)

    # Verifier les tentatives restantes
    remaining = get_failed_attempts(ip_address)
    context['remaining_attempts'] = remaining

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        # Verifier a nouveau apres soumission
        lockout_minutes = get_lockout_remaining_minutes(ip_address)
        if lockout_minutes > 0:
            context['lockout'] = True
            context['lockout_minutes'] = lockout_minutes
            return render(request, template_name, context)

        if form.is_valid():
            user = form.get_user()

            # Enregistrer la tentative reussie
            LoginAttempt.objects.create(
                ip_address=ip_address,
                username=user.username,
                success=True
            )

            login(request, user)
            next_url = request.POST.get('next', request.GET.get('next', reverse('admin:index')))
            return HttpResponseRedirect(next_url)
        else:
            # Enregistrer la tentative echouee
            username = request.POST.get('username', '')
            LoginAttempt.objects.create(
                ip_address=ip_address,
                username=username,
                success=False
            )

            # Recalculer les tentatives restantes
            remaining = get_failed_attempts(ip_address)
            context['remaining_attempts'] = remaining
            context['form'] = form

            # Verifier si maintenant bloque apres l'echec
            lockout_minutes = get_lockout_remaining_minutes(ip_address)
            if lockout_minutes > 0:
                context['lockout'] = True
                context['lockout_minutes'] = lockout_minutes

    else:
        context['form'] = AuthenticationForm(request)

    return render(request, template_name, context)
