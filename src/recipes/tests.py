from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe
from ingredients.models import Ingredient
from .forms import RecipeSearchForm

# TESTS FOR RECIPE MODEL 
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

# TESTS FOR RECIPE SEARCH FORM
class RecipeFormTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.user = User.objects.create_user(username='testuser', password='12345')
    ing1 = Ingredient.objects.create(name='Ingredient1')
    ing2 = Ingredient.objects.create(name='Ingredient2')

    cls.recipe = Recipe.objects.create(
      name='Test Recipe',
      cooking_time = 10,
      difficulty = 'easy'
    )
    cls.recipe.ingredients.set([ing1, ing2])
  
  def test_recipe_search_form_valid_data(self):
    form_data = {'recipe_name': 'Test'}
    form = RecipeSearchForm(data=form_data)
    self.assertTrue(form.is_valid())
  
  def test_recipe_search_form_empty_data(self):
    form = RecipeSearchForm(data={})
    self.assertTrue(form.is_valid())
  
  def test_recipe_search_form_field_max_length(self):
    form_data = {'recipe_name': 'A' * 201}
    form = RecipeSearchForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('recipe_name', form.errors)

# TESTS FOR RECIPE SEARCH VIEW 
class RecipeSearchViewTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.user = User.objects.create_user(username='testuser', password='12345')

    ingredients = [Ingredient.objects.create(name=f'Ingredient{i}') for i in range (2)]
    for i in range(15):
      recipe = Recipe.objects.create(
        name=f'Test Recipe {i}',
        cooking_time=10.0 + i,
        difficulty='medium'
      )
      recipe.ingredients.set(ingredients)

  def setUp(self):
    self.client = Client()

  def test_search_view_redirect_if_not_logged_in(self):
    response = self.client.get(reverse('recipes:search'))
    self.assertEqual(response.status_code, 302)
    self.assertTrue(response.url.startswith('/login'))

  def test_search_view_logged_in_status(self):
    self.client.login(username='testuser', password='12345')
    response = self.client.get(reverse('recipes:search'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'recipes/recipes_search.html')

  def test_search_view_returns_recipes(self):
    self.client.login(username='testuser', password='12345')
    response = self.client.post(reverse('recipes:search'), {'recipe_name': 'Test'})
    self.assertContains(response, 'Test Recipe')
  
  def test_search_view_empty_search_returns_all(self):
    self.client.login(username='testuser', password='12345')
    response = self.client.post(reverse('recipes:search'), {'recipe_name': ''})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Test Recipe 0')
    self.assertContains(response, 'Test Recipe 14')