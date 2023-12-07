from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from shop.models import Client


# Create your views here.

def register(request):

    if request.method == "POST":

        username  =  request.POST['username']
        fname     =  request.POST['fname']
        lname     =  request.POST['lname']
        email     =  request.POST['email']
        pass1     =  request.POST['pass1']
        pass2     =  request.POST['pass2']

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name  = fname
        myuser.last_name = lname
        
       

        myuser.save()

        messages.success(request, "Ton compte est bien créer !")
        return redirect('auth:connexion')

    return render(request, 'userauth/register.html')



def connexion(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1    = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "userauth/test.html")    
            
        
        else:
            messages.error(request, "Mauvais mot de passe")
            return redirect('auth:connexion')

    return render(request, 'userauth/connexion.html')


def deconnexion(request):
    logout(request)
    messages.success(request, ("deconnexion"))
    return redirect('auth:connexion')


def test(request):
    return render(request, 'test.html')