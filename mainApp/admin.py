from django.contrib import admin
from mainApp.models import Ingredient, MenuItem, Purchase, RecipeRequirement
# Register your models here.
admin.site.register(Ingredient)
admin.site.register(RecipeRequirement)
admin.site.register(Purchase)
admin.site.register(MenuItem)