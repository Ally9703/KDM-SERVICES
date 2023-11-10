from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [

    path('shop/', views.shop_view, name="shop"),
    path('panier/', views.panier_view, name="panier"),
    path('commande/', views.commande_view, name="commande"),

]