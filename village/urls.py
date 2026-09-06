from django.urls import path
from . import views
from .admin_views import admin_login

app_name = 'village'

urlpatterns = [
    path('', views.AccueilView.as_view(), name='accueil'),
    path('patrimoines/', views.ListePatrimoinesView.as_view(), name='patrimoines'),
    path('patrimoines/<slug:categorie_slug>/', views.ListePatrimoinesView.as_view(), name='patrimoines_categorie'),
    path('patrimoine/<int:pk>/', views.DetailPatrimoineView.as_view(), name='detail_patrimoine'),
    path('activites/', views.ListeActivitesView.as_view(), name='activites'),
    path('activites/<str:statut>/', views.ListeActivitesView.as_view(), name='activites_statut'),
    path('activite/<int:pk>/', views.DetailActiviteView.as_view(), name='detail_activite'),
    path('informations/', views.ListePagesView.as_view(), name='informations'),
    path('information/<slug:slug>/', views.DetailPageView.as_view(), name='detail_page'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('admin-login/', admin_login, name='admin_login'),
]
