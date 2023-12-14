from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from shop import *


# Create your views here.

def register(request):

    if request.method == "POST":

        nom_utilisateur  =  request.POST['nom_utilisateur']
        prenom     =  request.POST['prenom']
        nom     =  request.POST['nom']
        email     =  request.POST['email']
        pass1     =  request.POST['pass1']
        pass2     =  request.POST['pass2']

        utilisateur = User.objects.create_user(nom_utilisateur, email, pass1)
        utilisateur.first_name  = prenom
        utilisateur.last_name   = nom
        
       

        utilisateur.save()

        messages.success(request, "Ton compte est bien créer !")
        return redirect('auth:connexion')

    return render(request, 'userauth/register.html')



def connexion(request):
    if request.method == "POST":
        nom_utilisateur = request.POST['nom_utilisateur']
        pass1    = request.POST['pass1']
        user = authenticate(request, nom_utilisateur=nom_utilisateur, password=pass1)
        
        if user is not None:
            login(request, user)
            messages.success(request,('Vous êtes connecté'))
            return redirect('shop:shop')
            #return render(request, "userauth/test.html")    
            
        
        else:
            messages.error(request, "Mauvais mot de passe")
            return redirect('auth:connexion')

    return render(request, 'userauth/connexion.html')


def deconnexion(request):
    logout(request)
    messages.success(request, ("deconnexion"))
    return redirect('auth:connexion')


