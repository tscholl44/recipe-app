from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from .models import Recipe
from .forms import RecipeSearchForm

def recipes_home(request):
    return render(request, 'recipes/recipes_home.html')

class RecipesListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'

class RecipesDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipes_detail.html'

@login_required
def recipes_list(request):
    form = RecipeSearchForm(request.GET or None)
    recipes = Recipe.objects.all()
    
    # Apply search filters
    if form.is_valid():
        recipe_name = form.cleaned_data.get('recipe_name')
        ingredients = form.cleaned_data.get('ingredients')
        cooking_time_min = form.cleaned_data.get('cooking_time_min')
        cooking_time_max = form.cleaned_data.get('cooking_time_max')
        difficulty = form.cleaned_data.get('difficulty')
        
        if recipe_name:
            recipes = recipes.filter(name__icontains=recipe_name)
        
        if ingredients:
            # Split ingredients by comma and search for each
            ingredient_terms = [term.strip() for term in ingredients.split(',')]
            ingredient_query = Q()
            for term in ingredient_terms:
                ingredient_query |= Q(ingredients__icontains=term)
            recipes = recipes.filter(ingredient_query)
        
        if cooking_time_min is not None:
            recipes = recipes.filter(cooking_time__gte=cooking_time_min)
        
        if cooking_time_max is not None:
            recipes = recipes.filter(cooking_time__lte=cooking_time_max)
        
        if difficulty:
            recipes = recipes.filter(difficulty=difficulty)
    
    # Generate charts if there are results
    charts = {}
    if recipes.exists():
        charts = generate_charts(recipes)
    
    context = {
        'recipes': recipes,
        'form': form,
        'charts': charts,
        'total_results': recipes.count()
    }
    
    return render(request, 'recipes/recipes_list.html', context)

def generate_charts(recipes_queryset):
    # Convert QuerySet to DataFrame
    recipes_data = list(recipes_queryset.values(
        'name', 'cooking_time', 'difficulty', 'id'
    ))
    
    if not recipes_data:
        return {}
    
    df = pd.DataFrame(recipes_data)
    
    charts = {}
    
    # 1. Pie Chart - Cooking Time Distribution
    charts['pie_chart'] = create_cooking_time_pie_chart(df)
    
    # 2. Bar Chart - Difficulty Distribution
    charts['bar_chart'] = create_difficulty_bar_chart(df)
    
    # 3. Line Chart - Recipe Count by Cooking Time Range
    charts['line_chart'] = create_cooking_time_line_chart(df)
    
    return charts

def create_cooking_time_pie_chart(df):
    # Categorize cooking times
    def categorize_time(time):
        if time <= 15:
            return 'Quick (≤15 min)'
        elif time <= 30:
            return 'Medium (16-30 min)'
        elif time <= 60:
            return 'Long (31-60 min)'
        else:
            return 'Very Long (>60 min)'
    
    df['time_category'] = df['cooking_time'].apply(categorize_time)
    time_counts = df['time_category'].value_counts()
    
    plt.figure(figsize=(10, 8))
    colors = ['#ff6b35', '#e85a14', '#ff9f80', '#cc4400']
    
    plt.pie(time_counts.values, labels=time_counts.index, autopct='%1.1f%%',
            startangle=90, colors=colors)
    plt.title('Recipe Distribution by Cooking Time', fontsize=16, fontweight='bold')
    
    # Convert to base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return chart_data

def create_difficulty_bar_chart(df):
    difficulty_counts = df['difficulty'].value_counts()
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(difficulty_counts.index, difficulty_counts.values, 
                   color=['#90EE90', '#FFD700', '#FF6347'])
    
    plt.title('Recipe Distribution by Difficulty Level', fontsize=16, fontweight='bold')
    plt.xlabel('Difficulty Level', fontsize=12)
    plt.ylabel('Number of Recipes', fontsize=12)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom')
    
    plt.grid(axis='y', alpha=0.3)
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return chart_data

def create_cooking_time_line_chart(df):
    # Create cooking time ranges
    time_ranges = range(0, int(df['cooking_time'].max()) + 10, 10)
    range_counts = []
    range_labels = []
    
    for i in range(len(time_ranges) - 1):
        start = time_ranges[i]
        end = time_ranges[i + 1]
        count = len(df[(df['cooking_time'] >= start) & (df['cooking_time'] < end)])
        range_counts.append(count)
        range_labels.append(f'{start}-{end-1}')
    
    plt.figure(figsize=(12, 6))
    plt.plot(range_labels, range_counts, marker='o', linewidth=2, 
             markersize=8, color='#ff6b35')
    plt.fill_between(range_labels, range_counts, alpha=0.3, color='#ff6b35')
    
    plt.title('Recipe Count by Cooking Time Range', fontsize=16, fontweight='bold')
    plt.xlabel('Cooking Time Range (minutes)', fontsize=12)
    plt.ylabel('Number of Recipes', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return chart_data
