from django.urls import path #type: ignore
from . import views

urlpatterns = [
    path('nearestStudio/', views.nearest_std, name='nearest_std'),
]
