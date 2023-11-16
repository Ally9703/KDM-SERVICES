from django.shortcuts import render
from .models import *


# vue principale Page d'accueil Affichage des produits
def shop(request):
    produits = Produit.objects.all()
    context={
        'produits':produits
    }
    return render(request, 'shop/index.html', context)


# Vue de la Page de panier de produit
def panier(request):

    if request.user.is_authenticated:
        client = request.user.client
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        articles = commande.commandearticle_set.all()

    else:
        articles = []
        commande = {
            'get_panier_total':0,
            'get_panier_article':0
        }

    context = {
        'articles':articles,
        'commande':commande
    }
    return render(request, 'shop/panier.html', context)


# Vue de la page de commande de produits
def commande(request):
    if request.user.is_authenticated:
        client = request.user.client
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        articles = commande.commandearticle_set.all()

    else:
        articles = []
        commande = {
            'get_panier_total':0,
            'get_panier_article':0
        }

    context = {
        'articles':articles,
        'commande':commande
    }
    return render(request, 'shop/commande.html', context)
