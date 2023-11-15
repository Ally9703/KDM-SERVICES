from django.shortcuts import render


def shop(request):
    """ vue principale """

    context = {}

    return render(request, 'shop/index.html', context)


def panier(request):
    """ panier """

    context = {}

    return render(request, 'shop/panier.html', context)


def commande(request):
    """ Commande """
    context = {}

    return render(request, 'shop/commande.html', context)    
