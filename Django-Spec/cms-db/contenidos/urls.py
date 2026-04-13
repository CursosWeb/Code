from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_principal, name='pagina_principal'),
    path('<str:recurso>/', views.pagina_recurso, name='pagina_recurso'),
]
