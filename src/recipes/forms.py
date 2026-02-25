from django import forms

CHART__CHOICES = (
  ('#1', 'Bar Chart'),
  ('#2', 'Pie Chart'),
  ('#3', 'Line Chart')
)

class RecipeSearchForm(forms.Form):
  recipe_name = forms.CharField(max_length=120, required=False)
  chart_type = forms.ChoiceField(choices=CHART__CHOICES, required=False)