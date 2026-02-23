from django.db import models
from ingredients.models import Ingredient
from django.shortcuts import reverse

difficulty_choices = (
  ('easy', 'Easy'),
  ('medium', 'Medium'),
  ('intermediate', 'Intermediate'),
  ('hard', 'Hard')
)

class Recipe(models.Model):
  name = models.CharField(max_length=120)
  ingredients = models.ManyToManyField(Ingredient)
  cooking_time = models.FloatField(
    help_text='in minutes',
    verbose_name = 'cooking_time'
  )
  difficulty = models.CharField(
    max_length=12,
    choices=difficulty_choices,
    default='intermediate'
  )
  pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')

  def calculate_difficulty(self):
    ingredient_count = self.ingredients.count()
    if self.cooking_time < 10 and ingredient_count < 4:
      return "Easy"
    elif self.cooking_time < 10 and ingredient_count >= 4:
      return "Medium"
    elif self.cooking_time >= 10 and ingredient_count < 4:
      return "Intermediate"
    else:
      return "Hard"

  def get_absolute_url(self):
    return reverse ('recipes:detail', kwargs={'pk': self.pk})

  def __str__(self):
    return str(self.name)
