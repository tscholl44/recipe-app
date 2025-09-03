from django.db import models

# Create your models here.
class Recipe(models.Model):
    recipe_id= models.CharField(max_length=120)
    name= models.TextField()
    ingredients= models.TextField()
    cooking_time= models.IntegerField()
    difficulty= models.CharField(max_length=20)


    def __str__(self):
        return str(self.name)