from django.urls import path

from . import views

urlpatterns = [
    path('', views.leaderboard, name='leaderboard'),
    path('api/leaderboard', views.get_puppers, name='leaderboard_api'),
]
