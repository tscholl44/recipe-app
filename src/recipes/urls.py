from django.urls import path
from .views import recipes_home, RecipesListView, RecipesDetailView, recipes_list

app_name = 'recipes' 

urlpatterns = [
   path('', recipes_home, name='recipes_home'),
   path("recipes/", recipes_list, name="recipes_list"),  # Changed to function-based view
   path("recipes/<pk>", RecipesDetailView.as_view(), name="recipes_detail"),
]