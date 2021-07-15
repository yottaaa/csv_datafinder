from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<str:pk>/', views.dataView, name='data-view'),
    path('delete/<str:pk>/', views.dataDelete, name='data-delete'),
]