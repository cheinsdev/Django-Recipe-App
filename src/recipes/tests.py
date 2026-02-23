from django.test import TestCase
from .models import Recipe
from ingredients.models import Ingredient

class RecipeModelTest(TestCase):
  def setUpTestData():
    ingredient1 = Ingredient.objects.create(name='Egg')
    ingredient2 = Ingredient.objects.create(name='Oil')

    testrecipe = Recipe.objects.create(
      name='Fried Egg',
      cooking_time=5,
      difficulty='easy',
    )

    testrecipe.ingredients.add(ingredient1, ingredient2)
  
  def test_recipe_name(self):
    recipe = Recipe.objects.get(id=1)
    field_label = recipe._meta.get_field('name').verbose_name
    self.assertEqual(field_label, 'name')
  
  def test_recipe_max_length(self):
    recipe = Recipe.objects.get(id=1)
    max_length = recipe._meta.get_field('name').max_length
    self.assertEqual(max_length, 120)
  
  def test_ingredients(self):
    recipe = Recipe.objects.get(id=1)
    field_label = recipe._meta.get_field('ingredients').verbose_name
    self.assertEqual(field_label, 'ingredients')
  
  def test_cooking_time(self):
    recipe = Recipe.objects.get(id=1)
    field_label = recipe._meta.get_field('cooking_time').verbose_name
    self.assertEqual(field_label, 'cooking_time')
  
  def test_difficulty(self):
    recipe = Recipe.objects.get(id=1)
    field_label = recipe._meta.get_field('difficulty').verbose_name
    self.assertEqual(field_label, 'difficulty')

  def test_get_absolute_url(self):
    recipe = Recipe.objects.get(id=1)
    self.assertEqual(recipe.get_absolute_url(), '/recipes/list/1')