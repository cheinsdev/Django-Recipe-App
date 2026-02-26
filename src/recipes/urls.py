from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, RecipeDeleteView, search, create, ingredients, delete_ingredients

app_name = 'recipes'

urlpatterns = [
  path('', home),
  path('list/', RecipeListView.as_view(), name='list'),
  path('list/<pk>', RecipeDetailView.as_view(), name='detail'),
  path('delete/<int:pk>/', RecipeDeleteView.as_view(), name='delete'),
  path('search/', search, name='search'),
  path('create/', create, name='create'),
  path('ingredients/', ingredients, name='ingredients'),
  path('ingredients/delete/<int:pk>/', delete_ingredients, name='delete_ingredients')
]