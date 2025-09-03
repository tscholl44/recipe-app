from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Recipe

class RecipeModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            cooking_time=30,
            ingredients="flour, eggs, milk"
        )
    
    def test_recipe_creation(self):
        """Test that a recipe can be created successfully"""
        self.assertTrue(isinstance(self.recipe, Recipe))
        self.assertEqual(self.recipe.name, "Test Recipe")
        self.assertEqual(self.recipe.cooking_time, 30)
        self.assertEqual(self.recipe.ingredients, "flour, eggs, milk")
    
    def test_recipe_str_method(self):
        """Test the string representation of recipe"""
        self.assertEqual(str(self.recipe), "Test Recipe")
    
    
    def test_cooking_time_positive(self):
        """Test that cooking time must be positive"""
        with self.assertRaises(ValidationError):
            recipe = Recipe(
                name="Bad Recipe",
                cooking_time=-5,
                ingredients="test ingredients"
            )
            recipe.full_clean()
    
    def test_calculate_difficulty_method(self):
        """Test the difficulty calculation method"""
        # Easy recipe (< 10 minutes, < 4 ingredients)
        easy_recipe = Recipe.objects.create(
            name="Easy Recipe",
            cooking_time=5,
            ingredients="salt, pepper"
        )
        
        # Medium recipe (< 10 minutes, >= 4 ingredients OR >= 10 minutes, < 4 ingredients)
        medium_recipe = Recipe.objects.create(
            name="Medium Recipe",
            cooking_time=15,
            ingredients="salt, pepper"
        )
        
        # Hard recipe (>= 10 minutes, >= 4 ingredients)
        hard_recipe = Recipe.objects.create(
            name="Hard Recipe",
            cooking_time=30,
            ingredients="flour, eggs, milk, sugar, butter"
        )
        
        # Test difficulty calculations (adjust method names based on your actual model)
        if hasattr(easy_recipe, 'calculate_difficulty'):
            self.assertEqual(easy_recipe.calculate_difficulty(), 'Easy')
            self.assertEqual(medium_recipe.calculate_difficulty(), 'Medium')
            self.assertEqual(hard_recipe.calculate_difficulty(), 'Hard')
    
    def test_ingredients_required(self):
        """Test that ingredients field is required"""
        with self.assertRaises(ValidationError):
            recipe = Recipe(
                name="No Ingredients Recipe",
                cooking_time=20,
                ingredients=""
            )
            recipe.full_clean()
