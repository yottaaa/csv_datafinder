from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='hello'),
    path('<str:keyword>/', views.index, name='search'),
]