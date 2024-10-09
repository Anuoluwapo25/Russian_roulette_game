from django.urls import path
from . import views

urlpatterns = [
    path('breevs/', views.breevs, name='breevs'),
]