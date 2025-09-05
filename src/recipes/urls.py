from django.urls import path
from .views import recipes_home, RecipesListView, RecipesDetailView

app_name = 'recipes' 

urlpatterns = [
   path('', recipes_home, name='recipes_home'),
   path("recipes/", RecipesListView.as_view(), name="recipes_list"),
   path("recipes/<pk>", RecipesDetailView.as_view(), name="recipes_detail"),
]