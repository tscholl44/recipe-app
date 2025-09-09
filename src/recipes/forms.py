from django import forms
from .models import Recipe

class RecipeSearchForm(forms.Form):
    DIFFICULTY_CHOICES = [
        ('', 'Any Difficulty'),
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    recipe_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by recipe name...',
            'class': 'form-control'
        })
    )
    
    ingredients = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by ingredients...',
            'class': 'form-control'
        })
    )
    
    cooking_time_min = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Min time (minutes)',
            'class': 'form-control'
        })
    )
    
    cooking_time_max = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Max time (minutes)',
            'class': 'form-control'
        })
    )
    
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )