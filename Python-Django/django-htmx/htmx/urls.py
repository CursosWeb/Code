from django.urls import path
from . import views
urlpatterns = [

    path("", views.main),
    path("image", views.image),
    path("image_html", views.image_html),
    path("image_embedded", views.image_embedded),
]
