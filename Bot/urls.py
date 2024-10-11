from django.urls import path
from . import views

urlpatterns = [
    path('', views.breevs, name='breevs'),
    # path('rankings/', views.rankings, name="rankings"),
    # path('/play', views.play, name='play'),
    # path('wallet', views.wallet, name='wallet'),
]