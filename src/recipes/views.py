from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import RecipeSearchForm
from .models import Recipe
import pandas as pd
from .utils import get_chart

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

class RecipeListView(LoginRequiredMixin, ListView):
  model = Recipe
  template_name = 'recipes/recipes_main.html'

class RecipeDetailView(LoginRequiredMixin, DetailView):
  model = Recipe
  template_name = 'recipes/recipes_detail.html'