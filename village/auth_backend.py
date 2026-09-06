"""
Backend d'authentification avec limitation de tentatives de connexion.
Après 5 echecs, bloque l'IP pendant 5 minutes.
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import LoginAttempt

User = get_user_model()

# Configuration du blocage
MAX_ATTEMPTS = 5
LOCKOUT_MINUTES = 5


class RateLimitedAuthBackend(ModelBackend):
    """
    Backend d'authentification qui limite les tentatives de connexion.
    - 5 tentatives max par IP dans la derniere heure
    - Blocage de 5 minutes apres 5 echecs
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if request is None:
            return None

        ip_address = self._get_client_ip(request)

        # Verifier si l'IP est bloquée
        if self._is_ip_locked_out(ip_address):
            return None

        # Authentifier normalement
        user = super().authenticate(request, username=username, password=password, **kwargs)

        # Enregistrer la tentative
        self._record_attempt(ip_address, username, success=(user is not None))

        return user

    def _get_client_ip(self, request):
        """Recupere l'adresse IP du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        return ip

    def _is_ip_locked_out(self, ip_address):
        """Verifie si l'IP est actuellement bloquée"""
        cutoff_time = timezone.now() - timedelta(minutes=LOCKOUT_MINUTES)

        failed_attempts = LoginAttempt.objects.filter(
            ip_address=ip_address,
            success=False,
            attempt_time__gte=cutoff_time
        ).count()

        return failed_attempts >= MAX_ATTEMPTS

    def _record_attempt(self, ip_address, username, success):
        """Enregistre la tentative de connexion"""
        LoginAttempt.objects.create(
            ip_address=ip_address,
            username=username or '',
            success=success
        )

        # Nettoyer les anciennes tentatives (plus de 24h)
        old_cutoff = timezone.now() - timedelta(hours=24)
        LoginAttempt.objects.filter(attempt_time__lt=old_cutoff).delete()


def get_lockout_remaining_minutes(ip_address):
    """Retourne le nombre de minutes restantes de blocage pour une IP"""
    cutoff_time = timezone.now() - timedelta(minutes=LOCKOUT_MINUTES)

    last_failed = LoginAttempt.objects.filter(
        ip_address=ip_address,
        success=False,
        attempt_time__gte=cutoff_time
    ).order_by('-attempt_time').first()

    if last_failed:
        elapsed = timezone.now() - last_failed.attempt_time
        remaining = LOCKOUT_MINUTES - int(elapsed.total_seconds() / 60)
        return max(0, remaining)

    return 0


def get_failed_attempts(ip_address):
    """Retourne le nombre de tentatives echouees restantes avant blocage"""
    cutoff_time = timezone.now() - timedelta(minutes=LOCKOUT_MINUTES)

    count = LoginAttempt.objects.filter(
        ip_address=ip_address,
        success=False,
        attempt_time__gte=cutoff_time
    ).count()

    return max(0, MAX_ATTEMPTS - count)
