from django.shortcuts import render

# Create your views here.

def shop(request):
    return render(request, 'shop/home.html')

def produit(request):
    return render(request, 'shop/main.html')

def panier(request):
    return render(request, 'shop/panier.html')

def commande(request):
    return render(request, 'shop/testCommande.html')

def about(request):
    return render(request, 'shop/about.html')

def question(request):
    return render(request, 'shop/questions.html')