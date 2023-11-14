from django.shortcuts import render

# Vue des produits
def shop_view(request, *args, **kwargs):
    context = {}
    return render(request, 'shop/index.html', context)


# Vue du panier
def panier_view(request, *args, **kwargs):
    context = {}
    return render(request, 'shop/panier.html')

# Vue du commande
def commande_view(request, *args, **kwargs):
    context = {}
    return render(request, 'shop/commande.html')