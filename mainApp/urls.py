from django.contrib import admin
from django.urls import path
from mainApp import views
from os import name
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    
    
    path("logout/", views.log_out, name="logout"),
    path('', views.loadHome, name='home'),
    path('ingredients/', views.showIngredients, name="show/ingredients"),
    path('ingredients/new', views.addIngredients, name="add/addingredient"),
    path('ingredients/update/<slug:pk>', views.updateIngredient, name="update/updateingredient"),
    path('menu/', views.MenuView.as_view(), name="menu"),
    path('menu/new', views.addMenuItem, name="add/addtomenu"),
    path('reciperequirement/new', views.addRequirement, name="add_recipe_requirement"),
    path('purchases/', views.showPurchases, name="show/purchases"),
    path('purchases/new', views.addPurchase, name="add/addpurchase"),
    path('reports/', views.showReports, name="show/reports")
]

