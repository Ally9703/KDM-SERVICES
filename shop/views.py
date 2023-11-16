from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json


# vue principale Page d'accueil Affichage des produits
def shop(request, *args, **kwargs):
    produits = Produit.objects.all()
    if request.user.is_authenticated:
        client = request.user.client
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        nombre_article = commande.get_panier_article

    else:
        articles = []
        commande = {
            'get_panier_total':0,
            'get_panier_article':0
        }
        nombre_article = commande['get_panier_article']

    context = {
        
        'nombre_article': nombre_article,
        'produits':produits
    }
    
    return render(request, 'shop/index.html', context)


# Vue de la Page de panier de produit
def panier(request, *args, **kwargs):

    if request.user.is_authenticated:
        client = request.user.client
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        articles = commande.commandearticle_set.all()
        nombre_article = commande.get_panier_article

    else:
        articles = []
        commande = {
            'get_panier_total':0,
            'get_panier_article':0
        }
        nombre_article = commande['get_panier_article']

    context = {
        'articles':articles,
        'commande':commande,
        'nombre_article':nombre_article
    }
    return render(request, 'shop/panier.html', context)


# Vue de la page de commande de produits
def commande(request, *args, **kwargs):
    if request.user.is_authenticated:
        client = request.user.client
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        articles = commande.commandearticle_set.all()
        nombre_article = commande.get_panier_article

    else:
        articles = []
        commande = {
            'get_panier_total':0,
            'get_panier_article':0
        }
        nombre_article = commande['get_panier_article']

    context = {
        'articles':articles,
        'commande':commande,
        'nombre_article': nombre_article
    }

    return render(request, 'shop/commande.html', context)


@login_required
def update_article(request, *args, **kwargs):

    data       = json.loads(request.body)
    produit_id = data['produit_id']
    action     = data['action']
    #print(action, produit_id)

    produit = Produit.objects.get(id=produit_id)
    client = request. user.client 
    commande, created = Commande.objects.get_or_create(client=client, complete=False)
    commande_article, created  = CommandeArticle.objects.get_or_create(commande=commande, produit=produit)

    #Ajout et retrait des articles dans le panier
    if action == "add":
        commande_article.quantite +=1

    if action == "remove":
        commande_article.quantite -=1

    commande_article.save()


    if commande_article.quantite <=0:
        commande_article.delete()

    
    return JsonResponse("Panier modifier", safe=False)

#traitement,  validation de la com;ande  et verification de l'integrite des donnees(detection de fraude)
def traitementCommande(request, *args, **kwargs):

    data = json.loads(request.body)
    print(data)
    return JsonResponse("Votre paiement a été effectué avec succès, vous recevrez votre commande dans un instant !", safe=False)