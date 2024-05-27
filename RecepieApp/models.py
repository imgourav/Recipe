from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Recipes(models.Model):
  User = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True)
  recipe_name = models.CharField(max_length=100)
  recipe_description = models.TextField()
  recipe_image = models.ImageField(upload_to="recipes")




