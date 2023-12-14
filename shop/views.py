from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from .models import *
from django.http import JsonResponse
import json
#from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .utile import *


# Page de Shop (Page d'accueil)
def shop(request, *args, **kwargs):
    produits = Produit.objects.all()

    if request.user.is_authenticated:
        client = request.user.client
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        nombre_article = commande.get_panier_article
            
    else:
        
        commande ={
            'get_panier_total':0,
            'get_panier_article':0,
            'produit_physique': True
        }
        
        nombre_article = commande['get_panier_article']

        try:
            panier = json.loads(request.COOKIES.get('panier'))
            for obj in panier:
                nombre_article += panier[obj]['qte']
               
        except:

            panier = {}

        print(panier)

    context ={

        'produits':produits,
        'nombre_article': nombre_article
    }

    return render(request, 'shop/home.html', context)


# Page  de panier 
def panier(request, *args, **kwargs):

    if request.user.is_authenticated:
        client = request.user.client
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        articles = commande.commandearticle_set.all()
        nombre_article = commande.get_panier_article
        
    else:
        articles = []

        commande ={
            'get_panier_total':0,
            'get_panier_article':0,
            'produit_physique': True
        }

        nombre_article = commande['get_panier_article']

    try:
        panier = json.loads(request.COOKIES.get('panier'))
        for obj in panier:
            nombre_article += panier[obj]['qte']
            produit = Produit.objects.get(id=obj)
            total   = produit.price * panier[obj]['qte']
            commande['get_panier_article'] += panier[obj]['qte']
            commande['get_panier_total'] += total

            article = {

                'produit':{
                    'pk':produit.id,
                    'name':produit.name,
                    'price':produit.price,
                    'imageUrl':produit.imageUrl
                },
                
                'quantite': panier[obj]['qte'],
                'get_total': total

            }

            articles.append(article)

            if produit.digital == False:
                commande['produit_physique'] = True
    except:
        panier = {}
    print(panier)

    context={
        'articles':articles,
        'commande':commande,
        'nombre_article': nombre_article
    }

    return render(request, 'shop/panier.html', context)

#Page commande 
def commande(request, *args, **kwargs):
    if request.user.is_authenticated:

        client = request.user.client
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        articles = commande.commandearticle_set.all()
        nombre_article = commande.get_panier_article

    else:
        articles = []

        commande ={
            'get_panier_total':0,
            'get_panier_article':0,
            'produit_physique': True
        }
        nombre_article = commande['get_panier_article']

    try:
        panier = json.loads(request.COOKIES.get('panier'))
        for obj in panier:
            nombre_article += panier[obj]['qte']
            produit = Produit.objects.get(id=obj)
            total   = produit.price * panier[obj]['qte']
            commande['get_panier_article'] += panier[obj]['qte']
            commande['get_panier_total'] += total

            article = {

                'produit':{
                    'pk':produit.id,
                    'name':produit.name,
                    'price':produit.price,
                    'imageUrl':produit.imageUrl
                },

                'quantite': panier[obj]['qte'],
                'get_total': total
            }
            articles.append(article)

            if produit.digital == False:
                commande['produit_physique'] = True
    except:
        panier = {}
    print(panier)

    context={
        'articles':articles,
        'commande':commande,
        'nombre_article': nombre_article
    }
    
    return render(request, 'shop/commande.html', context)

# Page de mise à jour de articles 
@login_required()
def update_article(request,*args, **kwargs ):
    data = json.loads(request.body)
    produit_id = data['produit_id']
    action = data['action']
    produit = Produit.objects.get(id=produit_id)
    print(action, produit_id)

    client = request.user.client
    commande, created = Commande.objects.get_or_create(client=client, complete=False)
    commande_article, created = CommandeArticle.objects.get_or_create(commande=commande, produit=produit)

    if action == "add":
        commande_article.quantite +=1
    if action == "remove":
        commande_article.quantite -=1
    commande_article.save()

    if commande_article.quantite <= 0:
        commande_article.delete()
    return JsonResponse("panier modifier", safe=False)


# Page de traitement des articles 
def traitement_commande(request,*args, **kwargs):
    data = json.loads(request.body)
    #print(data)
    transaction_id = datetime.now().timestamp()

    if request.user.is_authenticated:
        
        client = request.user.client
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        total = float(data['form']['total'])
        commande.transaction_id = transaction_id

        if commande.get_panier_total == total:
            commande.complete = True
        commande.save()

        # Vérifier si la commande est physique
        if commande.produit_physique:

            AddressChipping.objects.create(
                client=client,
                commande=commande,
                addresse=data['shipping']['address'],
                ville=data['shipping']['city'],
                zipcode=data['shipping']['zipcode']
            )
    else:
        print('Utilisateur non authentifier')
        
    return JsonResponse('Traitement complete', safe=False)

# Page produit
def produit(request, *args, **kwargs):
    context={}
    return render(request, 'shop/produit.html', context)

# Page Appros
def about(request, *args, **kwargs):
    context={}
    return render(request, 'shop/about.html', context)

# Page des question
def question(request, *args, **kwargs):
    context={}
    return render(request, 'shop/questions.html', context)


def carousel(request, *args, **kwargs):
    context={}
    return render(request, 'shop/carousel.html', context)