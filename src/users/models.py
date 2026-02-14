from django.db import models

class User(models.Model):
  username = models.CharField(max_length=55)

  def __str__(self):
    return str(self.username)