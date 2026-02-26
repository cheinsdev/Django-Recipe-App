from django import forms
from .models import Recipe, Ingredient

CHART__CHOICES = (
  ('#1', 'Bar Chart'),
  ('#2', 'Pie Chart'),
  ('#3', 'Line Chart')
)

class RecipeSearchForm(forms.Form):
  recipe_name = forms.CharField(max_length=120, required=False)
  chart_type = forms.ChoiceField(choices=CHART__CHOICES, required=False)

class RecipeForm(forms.ModelForm):
  class Meta:
    model = Recipe
    fields = ['name', 'ingredients', 'cooking_time', 'pic']
    widgets = {
      'ingredients': forms.CheckboxSelectMultiple()
    }

class IngredientForm(forms.ModelForm):
  class Meta:
    model = Ingredient
    fields = ['name']