from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView
from .models import Recipe, Ingredient
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import RecipeSearchForm, RecipeForm, IngredientForm
import pandas as pd
from .utils import get_chart
from django.urls import reverse_lazy

def home(request):
  return render(request, 'recipes/recipes_home.html')

@login_required
def search(request):
  form = RecipeSearchForm(request.POST or None)
  recipes_df = None
  chart = None

  if request.method == 'POST':
    recipe_name = request.POST.get('recipe_name')
    chart_type = request.POST.get('chart_type')

    if recipe_name: 
      qs = Recipe.objects.filter(name__icontains=recipe_name)
    else: 
      qs = Recipe.objects.all()
  
    if qs:
      recipes_df = pd.DataFrame(qs.values())
      chart = get_chart(chart_type, recipes_df, labels=recipes_df['difficulty'].values)
      recipes_df = recipes_df.to_html()

  context={
    'form': form,
    'recipes_df': recipes_df,
    'chart': chart,
  }

  return render(request, 'recipes/recipes_search.html', context)

@login_required
def create(request):
  form = RecipeForm(request.POST or None, request.FILES or None)
  ingredients = Ingredient.objects.all()

  if form.is_valid():
    form.save()
    return redirect('recipes:list')
  
  return render(request, 'recipes/recipes_create.html', {'form': form, 'ingredients': ingredients})

@login_required
def ingredients(request):
  form = IngredientForm(request.POST or None)

  if form.is_valid():
    form.save()
    return redirect('recipes:create')
  
  return render(request, 'recipes/recipes_ingredients.html', {'form': form})

@login_required
def delete_ingredients(request, pk):
  try:
    ingredient = Ingredient.objects.get(pk=pk)
    ingredient.delete()
  except Ingredient.DoesNotExist:
    pass
  return redirect('recipes:create')

class RecipeListView(LoginRequiredMixin, ListView):
  model = Recipe
  template_name = 'recipes/recipes_main.html'

class RecipeDetailView(LoginRequiredMixin, DetailView):
  model = Recipe
  template_name = 'recipes/recipes_detail.html'

class RecipeDeleteView(LoginRequiredMixin, DeleteView):
  model = Recipe
  template_name = 'recipes/recipes_delete.html'
  success_url = reverse_lazy('recipes:list')