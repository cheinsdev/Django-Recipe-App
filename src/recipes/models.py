from django.db import models
from ingredients.models import Ingredient

difficulty_choices = (
  ('easy', 'Easy'),
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

  def __str__(self):
    return str(self.name)
