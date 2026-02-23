from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe

def home(request):
  return render(request, 'recipes/recipes_home.html')

class RecipeListView(ListView):
  model = Recipe
  template_name = 'recipes/recipes_main.html'

class RecipeDetailView(DetailView):
  model = Recipe
  template_name = 'recipes/recipes_detail.html'