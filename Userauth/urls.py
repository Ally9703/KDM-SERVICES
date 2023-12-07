from django.urls import path
from . import views

app_name = "auth"

urlpatterns = [

    path('register/', views.register, name="register"),
    path('connexion/', views.connexion, name="connexion"),
    path('logout/', views.deconnexion, name="logout"),
    path('test/', views.test, name="test"),

]