from django.db import models

# Create your models here.
class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'), 
        ('Hard', 'Hard'),
    ]
    
    name = models.TextField()
    ingredients = models.TextField()
    cooking_time = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, blank=True)
    pic = models.ImageField(upload_to="recipes", default="no_picture.jpeg")

    def save(self, *args, **kwargs):
        # Auto-calculate difficulty if not set
        if not self.difficulty:
            ingredient_count = len([i.strip() for i in self.ingredients.split(',') if i.strip()])
            if self.cooking_time < 30 and ingredient_count < 5:
                self.difficulty = 'Easy'
            elif self.cooking_time < 60 and ingredient_count < 10:
                self.difficulty = 'Medium'
            else:
                self.difficulty = 'Hard'
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)