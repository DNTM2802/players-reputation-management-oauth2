from django.urls import path

from . import views

urlpatterns = [
    path('matchmake/', views.matchmake, name='matchmake'),
    path('room/<str:room_id>/', views.room, name='room'),
    path('game/', views.match_manager, name='game'),

]
