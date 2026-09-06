"""DjangoProject URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.contrib.auth.views import LogoutView

from village.admin_views import admin_login

urlpatterns = [
    path('admin/login/', admin_login, name='admin_login'),
    path('admin/logout/', LogoutView.as_view(next_page='/admin/login/'), name='admin_logout'),
    path('admin/', admin.site.urls),
    path('', include('village.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Admin HTMX endpoints for gallery management
def htmx_galerie(request, pk):
    """Return the gallery management HTML for an activity"""
    from village.models import Activite
    activite = Activite.objects.get(pk=pk)
    images = activite.images.all()

    html = f'''
    <h3>Images de "{activite.titre}"</h3>
    <p style="color: #6C757D; margin-bottom: 12px;">
        {images.count} image(s) dans la galerie
    </p>

    <div class="gallery-grid">
    '''

    for img in images:
        html += f'''
        <div class="gallery-item" id="img-{img.pk}">
            <img src="{img.image.url}" alt="{img.legende}">
            <button type="button"
                    hx-delete="/admin/village/galerie/{img.pk}/delete/"
                    hx-confirm="Supprimer cette image ?"
                    hx-target="#img-{img.pk}"
                    hx-swap="delete"
                    style="position:absolute; top:2px; right:2px; background:rgba(183,65,14,0.9); color:white; border:none; border-radius:50%; width:22px; height:22px; cursor:pointer; font-size:12px;">
                ×
            </button>
        </div>
        '''

    html += '</div>'

    html += f'''
    <div style="margin-top: 16px; padding: 12px; background: #F8F9FA; border-radius: 6px;">
        <p style="margin: 0 0 8px; font-size: 12px; color: #6C757D;">
            Pour ajouter des images, ajoutez un "GalerieImage" avec ce lien d'activite.
        </p>
    </div>
    '''

    return HttpResponse(html)


def htmx_galerie_delete(request, pk):
    """Delete a gallery image via HTMX"""
    from village.models import GalerieImage
    try:
        img = GalerieImage.objects.get(pk=pk)
        img.delete()
        return HttpResponse('')
    except GalerieImage.DoesNotExist:
        return HttpResponse('')


# Add custom HTMX URLs to admin
original_get_urls = admin.site.get_urls


def get_urls():
    from django.urls import path as url_path
    urls = original_get_urls()
    custom_urls = [
        url_path('village/activite/<int:pk>/galerie/', admin.site.admin_view(htmx_galerie), name='village_galerie_htmx'),
        url_path('village/galerie/<int:pk>/delete/', admin.site.admin_view(htmx_galerie_delete), name='village_galerie_delete'),
    ]
    return custom_urls + urls


admin.site.get_urls = get_urls