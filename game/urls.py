from django.urls import path
from .views import home, predict, play, history, dashboard, leaderboard

urlpatterns = [
    path('', home, name='home'),
    path('predict/', predict, name='predict'),
    path('play/', play, name='play'),
    path('history/', history, name='history'),
    path('history/', history, name='history'),
    path('dashboard/', dashboard, name='dashboard'),
    path('leaderboard/', leaderboard, name='leaderboard'),
]