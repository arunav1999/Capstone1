from typing import ContextManager
from django.shortcuts import render,HttpResponse
from django.shortcuts import redirect

from django.db.models import Sum, F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.core.exceptions import SuspiciousOperation

from .models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .forms import IngredientForm, MenuItemForm

# My Custom Views

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        context["menu_items"] = MenuItem.objects.all()
        context["purchases"] = Purchase.objects.all()
        return context


class IngredientsView(ListView):
    template_name = "show/ingredients.html"
    model = Ingredient


class NewIngredientView(CreateView):
    template_name = "inventory/addingredient.html"
    model = Ingredient
    form_class = IngredientForm


class UpdateIngredientView(UpdateView):
    template_name = "update/updateingredient.html"
    model = Ingredient
    form_class = IngredientForm


class MenuView(ListView):
    template_name = "show/menu.html"
    model = MenuItem


############################################################################

def loadHome(request):
    ingredients = Ingredient.objects.all()
    purchases = Purchase.objects.all()
    menuItems = MenuItem.objects.all()
    context = {
        'ings':ingredients,
        'menitems':menuItems,
        'purchs':purchases
    }
    return HttpResponse(render(request,'home.html',context))

def addMenuItem(request):
    if(request.method == "POST"):
        title = request.POST['title']
        price = request.POST['price']
        menuObj = MenuItem(title=title,price=price)
        menuObj.save()
    return HttpResponse(render(request,'add/addtomenu.html'))

def addRequirement(request):
    '''
    #Requirement Model: 

    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)

    '''
    menuItems = MenuItem.objects.all()
    ingredients = Ingredient.objects.all()
    context = {'menuItems':menuItems,
                'ingredients':ingredients}
    selectedMenuItem = None
    selectedIngredient = None
    if(request.method == "POST"):
        
        entered_menu_item = request.POST['menu_item']
        entered_ingredient = request.POST['ingredient']
        quantity = request.POST['quantity']
        for item in menuItems:
            if(item.title == entered_menu_item):
                selectedMenuItem = item
                break
        for iter in ingredients:
            if(iter.name == entered_ingredient):
                selectedIngredient = iter
                break
        requirementObj = RecipeRequirement(menu_item=selectedMenuItem,ingredient=selectedIngredient,quantity=quantity)
        requirementObj.save()
    return HttpResponse(render(request,'add/addreciperequirement.html',context))

def showIngredients(request):
    ingredientsData = Ingredient.objects.all()
    context = {'ingredientsData':ingredientsData}
    return HttpResponse(render(request,'show/ingredients.html',context))


def addIngredients(request):
    '''
    name = models.CharField(max_length=200, unique=True)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=200)
    price_per_unit = models.FloatField(default=0)

    '''
   
    ingredientList = Ingredient.objects.all()
    if(request.method == "POST"):
        name = request.POST['name']
        quantity = request.POST['quantity']
        unit = request.POST['unit']
        price_per_unit = request.POST['price_per_unit']
        ingredientObj = Ingredient(name=name,quantity=quantity,unit=unit,price_per_unit=price_per_unit)
        ingredientObj.save()
    return HttpResponse(render(request,'add/addingredient.html'))

def updateIngredient(request,pk):
    context = {'selected':pk}
    if(request.method == 'POST'):
        
        entered_quantity = request.POST['quantity']
        entered_unit = request.POST['unit']
        entered_price_per_unit = request.POST['price_per_unit']
        Ingredient.objects.filter(name=pk).update(quantity=entered_quantity,unit=entered_unit,price_per_unit=entered_price_per_unit)
    return HttpResponse(render(request,'update/updateingredient.html',context))

def showPurchases(request):
    purchases = Purchase.objects.all()
    context = {'purchases':purchases}
    return HttpResponse(render(request,'show/purchases.html',context))

def addPurchase(request):
    menuItemsObj = MenuItem.objects.all()
    context = {'menuItems':menuItemsObj}
    if(request.method == 'POST'):
        item_title = request.POST['menu_item']
        selectedMenuItem = MenuItem.objects.get(title=item_title)
        newPurchaseObj = Purchase(menu_item=selectedMenuItem)
        newPurchaseObj.save()
    return HttpResponse(render(request,'add/addpurchase.html',context))

def showReports(request):
    purchasesObj = Purchase.objects.all()
    context = {'purchases':purchasesObj}
    return HttpResponse(render(request,'show/reports.html',context))

#############################################################################




def log_out(request):
    logout(request)
    return redirect("/")